"""Collision-free ER diagram generator — EntityLayout engine.
Output goes to diagram/ subfolder for centralized management.
CJK-optimized heights, obstacle-aware routing, auto-layout validation.
"""
import os, subprocess
import xml.sax.saxutils as xesc

OUT = os.path.join(r'C:\Users\getfunWindz\Desktop\一\虚无主义\作业', 'diagram')
DRAWIO = r'C:\Program Files\draw.io\draw.io'

CID = [1]
def nid():
    CID[0] += 1; return str(CID[0])
def esc(s):
    return xesc.escape(str(s), {'"': '&quot;'})

# CJK-optimized: draw.io HTML table renders CJK ~15% taller
HEADER_H = 28
ROW_H = 20
ENTITY_W = 190
COL_GAP = 60        # min px between columns
ROW_GAP = 70        # min px between rows in same column

# ────────────────────────────────────────────────────────────

def calc_h(fields):
    """Entity height in px (CJK-aware)."""
    return HEADER_H + len(fields) * ROW_H + 4

def entity_html(title, fields, pk):
    rows = [
        '<tr><td style="background-color:#C2CFF2;text-align:center;'
        'font-weight:bold;font-size:11px;padding:4px;" colspan="2">'
        + esc(title) + '</td></tr>'
    ]
    for fn in fields:
        ef = esc(fn)
        b = '<b>' + ef + '</b>' if fn in pk else ef
        rows.append(
            '<tr><td style="border-top:1px solid #E8E8E8;'
            'font-size:9px;padding:3px 6px;" colspan="2">' + b + '</td></tr>')
    return '<table>' + ''.join(rows) + '</table>'

# ────────────────────────────────────────────────────────────

class EntityLayout:
    """Layout engine with collision detection and obstacle-aware routing."""

    def __init__(self):
        self.entities = []   # [(eid, name, (x,y,w,h))]
        self.cells = []
        self._map = {}

    # ── entity registration ──

    def add_entity(self, x, y, name, fields, pk_set=None, w=ENTITY_W):
        pk = pk_set or set()
        h = calc_h(fields)
        eid = nid()
        html = entity_html(name, fields, pk)
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(html) + '" '
            'style="whiteSpace=wrap;html=1;rounded=0;fillColor=#FFFFFF;'
            'strokeColor=#DCDCDC;fontColor=#444444;fontSize=9;" '
            'vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    # ── collision-free connector ──

    def add_connector(self, src, dst, label='', c1='', c2='',
                      sx=1, sy=0.5, tx=0, ty=0.5):
        sr = self._map[src]
        dr = self._map[dst]
        ex = sr[0] + sx * sr[2]
        ey = sr[1] + sy * sr[3]
        nx = dr[0] + tx * dr[2]
        ny = dr[1] + ty * dr[3]
        obstacles = [r for e, _, r in self.entities if e not in (src, dst)]
        wpts = self._route(ex, ey, nx, ny, obstacles)

        eid = nid()
        lbl = esc(label) if label else ''
        style = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                 'strokeColor=#999999;strokeWidth=1;fontSize=10;'
                 'fontColor=#444444;fontStyle=2;'
                 'labelBackgroundColor=#FFFFFF;endArrow=classic;endFill=1;'
                 'exitX={};exitY={};entryX={};entryY={};').format(sx, sy, tx, ty)
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + lbl + '" style="' + style
            + '" edge="1" parent="1" source="' + src + '" target="' + dst + '">')
        if wpts:
            pts = ''.join('        <mxPoint x="{}" y="{}"/>\n'.format(x, y) for x, y in wpts)
            self.cells.append('    <mxGeometry relative="1" as="geometry">\n' + pts + '    </mxGeometry>')
        else:
            self.cells.append('    <mxGeometry relative="1" as="geometry"/>')
        self.cells.append('  </mxCell>')

        for txt, ox in [(c1, -12), (c2, 12)]:
            if not txt:
                continue
            ci = nid()
            self.cells.append(
                '<mxCell id="' + ci + '" value="' + esc(txt) + '" '
                'style="text;html=1;fontSize=10;fontStyle=1;fontColor=#555555;'
                'align=center;verticalAlign=middle;" vertex="1" connectable="0" parent="1">')
            self.cells.append(
                '    <mxGeometry x="' + str(ox) + '" y="-14" width="24" height="16" '
                'relative="1" as="geometry"/>')
            self.cells.append('  </mxCell>')

    # ── obstacle-aware orthogonal routing ──

    @staticmethod
    def _line_hits(x1, y1, x2, y2, r):
        rx, ry, rw, rh = r
        if x1 == x2:
            if not (rx <= x1 <= rx + rw):
                return False
            return not (max(y1, y2) <= ry or min(y1, y2) >= ry + rh)
        if y1 == y2:
            if not (ry <= y1 <= ry + rh):
                return False
            return not (max(x1, x2) <= rx or min(x1, x2) >= rx + rw)
        return False

    @staticmethod
    def _path_ok(pts, obs):
        for i in range(len(pts) - 1):
            for r in obs:
                if EntityLayout._line_hits(pts[i][0], pts[i][1],
                                            pts[i+1][0], pts[i+1][1], r):
                    return False
        return True

    def _route(self, ex, ey, nx, ny, obs):
        """Obstacle-avoiding orthogonal route."""
        if not obs:
            return []

        ro = max(r[0] + r[2] for r in obs) + 80
        to = min(r[1] for r in obs) - 60
        bo = max(r[1] + r[3] for r in obs) + 60

        # 2-bend: right, up/down, left
        for my in [ny, ey, (ey + ny) / 2, to + 30, bo - 30]:
            p = [(ex, ey), (ro, my), (nx, ny)]
            if self._path_ok(p, obs):
                return [(ro, my)]

        # 3-bend: up/down, right, up/down
        for my in [to, bo, (to + bo) / 2]:
            for mx in [ex, nx, ro]:
                p = [(ex, ey), (ex, my), (mx, my), (nx, ny)]
                if self._path_ok(p, obs):
                    return [(ex, my), (mx, my)]

        # 4-bend fallback
        p = [(ex, ey), (ex, to), (ro, to), (ro, ny), (nx, ny)]
        if self._path_ok(p, obs):
            return [(ex, to), (ro, to), (ro, ny)]
        p = [(ex, ey), (ex, bo), (ro, bo), (ro, ny), (nx, ny)]
        if self._path_ok(p, obs):
            return [(ex, bo), (ro, bo), (ro, ny)]

        return [(ro, ey), (ro, ny)]

    # ── validation ──

    def validate(self):
        issues = []
        for i, (_, n1, r1) in enumerate(self.entities):
            for j, (_, n2, r2) in enumerate(self.entities):
                if i >= j:
                    continue
                x1, y1, w1, h1 = r1
                x2, y2, w2, h2 = r2
                if not (x1 + w1 <= x2 or x1 >= x2 + w2
                        or y1 + h1 <= y2 or y1 >= y2 + h2):
                    dx = max(0, min(x1 + w1 - x2, x2 + w2 - x1))
                    dy = max(0, min(y1 + h1 - y2, y2 + h2 - y1))
                    issues.append(f'  OVERLAP: "{n1}" <-> "{n2}" ({dx}x{dy}px)')
        return issues

    # ── export ──

    def to_xml(self):
        body = '\n'.join(self.cells)
        return (
            '<mxfile host="Electron" modified="2026-06-10T00:00:00.000Z" '
            'agent="Mozilla/5.0" version="30.0.4">\n'
            '<diagram id="d1" name="diagram">\n'
            '<mxGraphModel dx="0" dy="0" grid="0" page="1" '
            'pageWidth="2400" pageHeight="1800">\n'
            '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
            + body + '\n'
            '</root></mxGraphModel></diagram></mxfile>')

    def save(self, subdir, name):
        d = os.path.join(OUT, subdir)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, name + '.drawio')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_xml())
        return path

    def export(self, subdir, name):
        src = self.save(subdir, name)
        dst = src.replace('.drawio', '.png')
        subprocess.run(
            [DRAWIO, '--export', '--format', 'png', '--width', '1200',
             '--border', '16', '--output', dst, src],
            capture_output=True, timeout=30)
        sz = os.path.getsize(dst)
        print(f'  {os.path.basename(dst)} ({sz} bytes)')
        return dst


# ════════════════════════════════════════════════════════════
# Layout helpers
# ════════════════════════════════════════════════════════════

def column_y(heights, gap=ROW_GAP):
    """Given list of entity heights, return Y positions with gaps."""
    ys = [20]
    for h in heights[:-1]:
        ys.append(ys[-1] + h + gap)
    return ys

# ════════════════════════════════════════════════════════════
# Diagrams
# ════════════════════════════════════════════════════════════

def diagram_41():
    """Entity Attribute: 3 boxes side-by-side (no connectors)."""
    ly = EntityLayout()
    ly.add_entity(40, 40, '商品 (Goods)',
        ['产品编号(PK)', '产品名称', '所属商家(FK)', '品类', '描述',
         '单价', '库存', '上架日期', '产品状态'],
        {'产品编号(PK)'})
    ly.add_entity(360, 40, '订单 (Order)',
        ['订单编号(PK)', '客户编号(FK)', '产品编号(FK)', '购买数量',
         '支付方式', '总金额', '收货地址', '订单状态', '下单时间'],
        {'订单编号(PK)'})
    ly.add_entity(680, 40, '商家 (Artisan)',
        ['商家编号(PK)', '商家名称', '登录密码', '联系人', '电话',
         '入驻日期', '状态'],
        {'商家编号(PK)'})
    for i in ly.validate():
        print(i)
    ly.export('41-entity-attribute', 'entity-attribute')

def diagram_42_1():
    """Merchant review: Admin+Artisan (left) → AuditRecord (right)."""
    ly = EntityLayout()
    h_admin = calc_h(['管理员账号(PK)', '登录密码', '姓名', '角色'])
    h_artisan = calc_h(['商家编号(PK)', '商家名称', '登录密码', '联系人',
                        '电话', '入驻日期', '状态'])
    # Admin + Artisan left column, AuditRecord right, vertically centered
    left_h = h_admin + 70 + h_artisan
    right_h = calc_h(['审核编号(PK)', '商家名称(FK)', '审核员账号(FK)',
                      '审核结果', '备注', '审核时间'])
    audit_y = 40 + (left_h - right_h) // 2
    admin = ly.add_entity(40, 40, '管理员 (Admin)',
        ['管理员账号(PK)', '登录密码', '姓名', '角色'],
        {'管理员账号(PK)'})
    artisan = ly.add_entity(40, 40 + h_admin + 70, '商家 (Artisan)',
        ['商家编号(PK)', '商家名称', '登录密码', '联系人', '电话',
         '入驻日期', '状态'],
        {'商家编号(PK)'})
    audit = ly.add_entity(500, audit_y, '审核记录 (AuditRecord)',
        ['审核编号(PK)', '商家名称(FK)', '审核员账号(FK)', '审核结果',
         '备注', '审核时间'],
        {'审核编号(PK)'})
    ly.add_connector(admin, audit, label='执行审核', c1='1', c2='n',
                     sx=1, sy=0.5, tx=0, ty=0.25)
    ly.add_connector(artisan, audit, label='被审核', c1='1', c2='1',
                     sx=1, sy=0.5, tx=0, ty=0.75)
    for i in ly.validate():
        print(i)
    ly.export('42-partial-er', '42-1-merchant-review')

def diagram_42_2():
    """Product listing: vertical chain with auto-computed Y positions."""
    ly = EntityLayout()
    names = ['商家 (Artisan)', '店铺 (Shop)', '商品 (Goods)', '商品图片 (GoodsImage)']
    fields_list = [
        ['商家编号(PK)', '商家名称', '登录密码', '联系人', '电话', '入驻日期', '状态'],
        ['店铺编号(PK)', '商家编号(FK)', '店铺名称', 'logo', '简介', '开通时间'],
        ['产品编号(PK)', '店铺编号(FK)', '产品名称', '品类', '描述',
         '单价', '库存', '上架日期', '产品状态'],
        ['图片编号(PK)', '产品编号(FK)', '图片URL', '排序号'],
    ]
    pks = [{'商家编号(PK)'}, {'店铺编号(PK)'}, {'产品编号(PK)'}, {'图片编号(PK)'}]
    heights = [calc_h(f) for f in fields_list]
    ys = column_y(heights, gap=50)
    ids = []
    for i, name in enumerate(names):
        eid = ly.add_entity(300, ys[i], name, fields_list[i], pks[i])
        ids.append(eid)
    labels_cards = [('拥有', '1', '1'), ('包含', '1', 'n'), ('展示', '1', 'n')]
    for i, (lbl, c1, c2) in enumerate(labels_cards):
        ly.add_connector(ids[i], ids[i+1], label=lbl, c1=c1, c2=c2,
                         sx=0.5, sy=1, tx=0.5, ty=0)
    for i in ly.validate():
        print(i)
    ly.export('42-partial-er', '42-2-product-listing')

def diagram_42_3():
    """User ordering: dual-lane with pre-computed Y positions."""
    ly = EntityLayout()
    # Top lane: Customer → Collect → Goods
    # Bottom lane: Customer → Order → Goods
    cst_h = calc_h(['客户编号(PK)', '客户昵称', '登录密码', '手机号', '注册日期', '最后登录时间'])
    col_h = calc_h(['客户编号(PK,FK)', '产品编号(PK,FK)', '收藏时间'])
    ord_h = calc_h(['订单编号(PK)', '客户编号(FK)', '产品编号(FK)', '购买数量',
                    '支付方式', '总金额', '收货地址', '订单状态', '下单时间'])
    gds_h = calc_h(['产品编号(PK)', '店铺编号(FK)', '产品名称', '品类', '描述',
                    '单价', '库存', '上架日期', '产品状态'])

    y_top = 40
    y_bot = y_top + max(cst_h, col_h, 250) + 60  # ensure enough gap
    # Goods vertically centered between both lanes
    y_gds = y_top + (y_bot + ord_h//2 - y_top) // 2 - gds_h//2

    cst = ly.add_entity(30, y_top, '消费者 (Customer)',
        ['客户编号(PK)', '客户昵称', '登录密码', '手机号', '注册日期', '最后登录时间'],
        {'客户编号(PK)'})
    col = ly.add_entity(330, y_top, '收藏 (Collect)',
        ['客户编号(PK,FK)', '产品编号(PK,FK)', '收藏时间'],
        {'客户编号(PK,FK)', '产品编号(PK,FK)'})
    ord_ = ly.add_entity(330, y_bot, '订单 (Order)',
        ['订单编号(PK)', '客户编号(FK)', '产品编号(FK)', '购买数量',
         '支付方式', '总金额', '收货地址', '订单状态', '下单时间'],
        {'订单编号(PK)'})
    gds = ly.add_entity(680, y_gds, '商品 (Goods)',
        ['产品编号(PK)', '店铺编号(FK)', '产品名称', '品类', '描述',
         '单价', '库存', '上架日期', '产品状态'],
        {'产品编号(PK)'})
    # Top lane: Customer → Collect
    ly.add_connector(cst, col, label='收藏', c1='1', c2='n')
    ly.add_connector(col, gds, label='被收藏', c1='n', c2='1')
    # Bottom lane: Customer → Order
    ly.add_connector(cst, ord_, label='提交', c1='1', c2='n')
    ly.add_connector(ord_, gds, label='关联', c1='n', c2='1')
    for i in ly.validate():
        print(i)
    ly.export('42-partial-er', '42-3-user-order')

def diagram_43_global():
    """Global ER: 4-column grid with row-based Y alignment."""
    ly = EntityLayout()
    W = 190
    X = [30, 430, 830, 1230]

    # Define column contents: each col = [(name, fields, pk_set), ...]
    # We compute row heights based on tallest entity per logical row
    cols = [
        [  # col 0
            ('管理员 (Admin)', ['管理员账号(PK)', '登录密码', '姓名', '角色'], {'管理员账号(PK)'}),
            ('公告 (Notice)', ['公告编号(PK)', '标题', '内容', '发布时间', '发布人(FK)'], {'公告编号(PK)'}),
        ],
        [  # col 1
            ('商家 (Artisan)', ['商家编号(PK)', '商家名称', '登录密码', '联系人', '电话',
                              '入驻日期', '状态'], {'商家编号(PK)'}),
            ('店铺 (Shop)', ['店铺编号(PK)', '商家编号(FK)', '店铺名称', 'logo', '简介',
                           '开通时间'], {'店铺编号(PK)'}),
            ('审核记录 (AuditRecord)', ['审核编号(PK)', '商家名称(FK)', '审核员账号(FK)',
                                       '审核结果', '备注', '审核时间'], {'审核编号(PK)'}),
        ],
        [  # col 2
            ('商品 (Goods)', ['产品编号(PK)', '店铺编号(FK)', '产品名称', '品类', '描述',
                            '单价', '库存', '上架日期', '产品状态'], {'产品编号(PK)'}),
            ('商品图片 (GoodsImage)', ['图片编号(PK)', '产品编号(FK)', '图片URL', '排序号'],
                                     {'图片编号(PK)'}),
        ],
        [  # col 3
            ('消费者 (Customer)', ['客户编号(PK)', '客户昵称', '登录密码', '手机号',
                                 '注册日期', '最后登录时间'], {'客户编号(PK)'}),
            ('收藏 (Collect)', ['客户编号(PK,FK)', '产品编号(PK,FK)', '收藏时间'],
                              {'客户编号(PK,FK)', '产品编号(PK,FK)'}),
            ('订单 (Order)', ['订单编号(PK)', '客户编号(FK)', '产品编号(FK)', '购买数量',
                            '支付方式', '总金额', '收货地址', '订单状态', '下单时间'], {'订单编号(PK)'}),
        ],
    ]

    # Compute row Y positions based on tallest entity in each row index
    max_rows = max(len(c) for c in cols)
    row_heights = []
    for ri in range(max_rows):
        max_h = 0
        for c in cols:
            if ri < len(c):
                h = calc_h(c[ri][1])
                max_h = max(max_h, h)
        row_heights.append(max_h)

    ys = column_y(row_heights, gap=60)

    # Place entities
    placed = {}
    for ci, col in enumerate(cols):
        for ri, (name, fields, pk) in enumerate(col):
            eid = ly.add_entity(X[ci], ys[ri], name, fields, pk, w=W)
            placed[(ci, ri)] = eid

    # Intra-column vertical connections
    # col 0: Admin → Notice
    ly.add_connector(placed[(0, 0)], placed[(0, 1)], label='发布', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)
    # col 1: Artisan → Shop, Artisan → AuditRecord
    ly.add_connector(placed[(1, 0)], placed[(1, 1)], label='拥有', c1='1', c2='1',
                     sx=0.5, sy=1, tx=0.5, ty=0)
    ly.add_connector(placed[(1, 0)], placed[(1, 2)], label='被审核', c1='1', c2='1',
                     sx=1, sy=0.5, tx=1, ty=0.5)
    # col 2: Goods → GoodsImage
    ly.add_connector(placed[(2, 0)], placed[(2, 1)], label='展示', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)
    # col 3: Customer → Collect, Customer → Order
    ly.add_connector(placed[(3, 0)], placed[(3, 1)], label='收藏', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)
    ly.add_connector(placed[(3, 0)], placed[(3, 2)], label='提交', c1='1', c2='n',
                     sx=1, sy=0.5, tx=1, ty=0.5)

    # Inter-column horizontal connections
    ly.add_connector(placed[(0, 0)], placed[(1, 2)], label='审核', c1='1', c2='n')
    ly.add_connector(placed[(1, 1)], placed[(2, 0)], label='包含', c1='1', c2='n')
    ly.add_connector(placed[(3, 1)], placed[(2, 0)], label='被收藏', c1='n', c2='1')
    ly.add_connector(placed[(3, 2)], placed[(2, 0)], label='关联', c1='n', c2='1')

    for i in ly.validate():
        print(i)
    ly.export('43-global-er', 'global-er')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for fn, name in [
        (diagram_41, 'Entity Attribute (4.1)'),
        (diagram_42_1, 'Partial ER: Merchant Review (4.2.1)'),
        (diagram_42_2, 'Partial ER: Product Listing (4.2.2)'),
        (diagram_42_3, 'Partial ER: User Ordering (4.2.3)'),
        (diagram_43_global, 'Global ER (4.3)'),
    ]:
        print(f'=== {name} ===')
        fn()
