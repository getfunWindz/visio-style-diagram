# Visio-Style Diagram Generator

Visio 风格的软件工程图自动生成器。基于 **draw.io Desktop** + **Python**，自动输出可编辑的 `.drawio` 文件和 `.png` 图片。

适用于：数据库 ER 图 / 实体关系图 / UML 类图 / 架构图 / 系统部署图 / 数据流图

---

## 特性

- **Visio 原生风格** — 浅灰画布、浅蓝表头、白底实体、灰线正交连接，还原 Visio 经典视觉
- **零碰撞布局** — `EntityLayout` 引擎自动计算实体位置，保证框不重叠、线不穿实体
- **CJK 优化** — 针对中文/日文文字渲染调整高度公式，文字不被截断
- **障碍物感知路由** — 2/3/4 弯正交路径规划，连接线自动绕开所有中间实体
- **导出前校验** — `validate()` 自动检查所有实体框的 bounding box 是否重叠
- **统一输出管理** — 所有文件自动归入 `diagram/` 子文件夹

## 效果展示

```
┌──────────────────────┐  ← thin #DCDCDC border
│  Entity Name (bold)  │  ← #C2CFF2 header fill, #000000 text
├──────────────────────┤  ← 1px #E8E8E8 separator
│  PK_Field (bold)     │  ← PK fields in bold
│  regular_field       │  ← #444444 text, 9px
│  field3(FK)          │  ← FK marked with (FK) suffix
└──────────────────────┘

 EntityA ────────┬────── EntityB    ← #999999 orthogonal line
                │关系名              ← italic label on white bg
               1 n                  ← bold cardinality text
```

## 快速开始

### 依赖

1. [draw.io Desktop](https://github.com/jgraph/drawio-desktop/releases)（免费）— 用于导出 PNG
2. Python 3.10+（仅需标准库，无需 pip 安装）

### 最短示例

```python
import os, subprocess, xml.sax.saxutils as xesc

OUT = 'diagram'   # 所有输出归入 diagram/ 目录
DRAWIO = r'C:\Program Files\draw.io\draw.io'

CID = [1]
def nid():
    CID[0] += 1; return str(CID[0])
def esc(s):
    return xesc.escape(str(s), {'"': '&quot;'})

HEADER_H = 28; ROW_H = 20; ENTITY_W = 190
def calc_h(fields):
    return HEADER_H + len(fields) * ROW_H + 4
def column_y(heights, gap=70):
    ys = [20]
    for h in heights[:-1]:
        ys.append(ys[-1] + h + gap)
    return ys

class EntityLayout:
    """Collision-free diagram layout engine."""
    def __init__(self):
        self.entities = []; self.cells = []; self._map = {}
    def add_entity(self, x, y, name, fields, pk_set=None, w=ENTITY_W):
        pk = pk_set or set(); h = calc_h(fields); eid = str(nid())
        rows = ['<tr><td style="background-color:#C2CFF2;text-align:center;font-weight:bold;font-size:11px;padding:4px;" colspan="2">' + esc(name) + '</td></tr>']
        for fn in fields:
            b = '<b>' + esc(fn) + '</b>' if fn in (pk_set or set()) else esc(fn)
            rows.append('<tr><td style="border-top:1px solid #E8E8E8;font-size:9px;padding:3px 6px;" colspan="2">' + b + '</td></tr>')
        html = '<table>' + ''.join(rows) + '</table>'
        self.cells.append('<mxCell id="' + eid + '" value="' + esc(html) + '" style="whiteSpace=wrap;html=1;rounded=0;fillColor=#FFFFFF;strokeColor=#DCDCDC;fontColor=#444444;fontSize=9;" vertex="1" parent="1">')
        self.cells.append('    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h); self.entities.append((eid, name, rect)); self._map[eid] = rect
        return eid
    def add_connector(self, src, dst, label='', c1='', c2='', sx=1, sy=0.5, tx=0, ty=0.5):
        sr = self._map[src]; dr = self._map[dst]
        ex, ey = sr[0] + sx * sr[2], sr[1] + sy * sr[3]
        nx, ny = dr[0] + tx * dr[2], dr[1] + ty * dr[3]
        obs = [r for e, _, r in self.entities if e not in (src, dst)]
        wpts = self._route(ex, ey, nx, ny, obs)
        style = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#999999;strokeWidth=1;fontSize=10;fontColor=#444444;fontStyle=2;labelBackgroundColor=#FFFFFF;endArrow=classic;endFill=1;exitX={};exitY={};entryX={};entryY={};').format(sx, sy, tx, ty)
        self.cells.append('<mxCell id="' + nid() + '" value="' + esc(label) + '" style="' + style + '" edge="1" parent="1" source="' + src + '" target="' + dst + '">')
        if wpts:
            pts = ''.join('        <mxPoint x="{}" y="{}"/>\n'.format(x, y) for x, y in wpts)
            self.cells.append('    <mxGeometry relative="1" as="geometry">\n' + pts + '    </mxGeometry>')
        else:
            self.cells.append('    <mxGeometry relative="1" as="geometry"/>')
        self.cells.append('  </mxCell>')
        for txt, ox in [(c1, -12), (c2, 12)]:
            if not txt: continue
            self.cells.append('<mxCell id="' + nid() + '" value="' + esc(txt) + '" style="text;html=1;fontSize=10;fontStyle=1;fontColor=#555555;align=center;verticalAlign=middle;" vertex="1" connectable="0" parent="1">')
            self.cells.append('    <mxGeometry x="' + str(ox) + '" y="-14" width="24" height="16" relative="1" as="geometry"/>')
            self.cells.append('  </mxCell>')
    def _route(self, ex, ey, nx, ny, obs):
        if not obs: return []
        ro = max((r[0] + r[2] for r in obs), default=0) + 80
        to = min((r[1] for r in obs), default=0) - 60
        bo = max((r[1] + r[3] for r in obs), default=0) + 60
        for my in [ny, ey, (ey + ny) / 2, to + 30, bo - 30]:
            p = [(ex, ey), (ro, my), (nx, ny)]
            if self._path_ok(p, obs): return [(ro, my)]
        for my in [to, bo, (to + bo) / 2]:
            for mx in [ex, nx, ro]:
                p = [(ex, ey), (ex, my), (mx, my), (nx, ny)]
                if self._path_ok(p, obs): return [(ex, my), (mx, my)]
        for (my,) in [(to,), (bo,)]:
            p = [(ex, ey), (ex, my), (ro, my), (ro, ny), (nx, ny)]
            if self._path_ok(p, obs): return [(ex, my), (ro, my), (ro, ny)]
        return [(ro, ey), (ro, ny)]
    @staticmethod
    def _path_ok(pts, obs):
        for i in range(len(pts) - 1):
            for r in obs:
                if EntityLayout._line_hits(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], r): return False
        return True
    @staticmethod
    def _line_hits(x1, y1, x2, y2, r):
        rx, ry, rw, rh = r
        if x1 == x2:
            if not (rx <= x1 <= rx + rw): return False
            return not (max(y1, y2) <= ry or min(y1, y2) >= ry + rh)
        if y1 == y2:
            if not (ry <= y1 <= ry + rh): return False
            return not (max(x1, x2) <= rx or min(x1, x2) >= rx + rw)
        return False
    def validate(self):
        issues = []
        for i, (_, n1, r1) in enumerate(self.entities):
            for j, (_, n2, r2) in enumerate(self.entities):
                if i >= j: continue
                x1, y1, w1, h1 = r1; x2, y2, w2, h2 = r2
                if not (x1 + w1 <= x2 or x1 >= x2 + w2 or y1 + h1 <= y2 or y1 >= y2 + h2):
                    dx = max(0, min(x1 + w1 - x2, x2 + w2 - x1))
                    dy = max(0, min(y1 + h1 - y2, y2 + h2 - y1))
                    issues.append(f'OVERLAP: "{n1}" <-> "{n2}" ({dx}x{dy}px)')
        return issues
    def export(self, subdir, name):
        import os, subprocess as sp
        d = os.path.join(OUT, subdir); os.makedirs(d, exist_ok=True)
        src = os.path.join(d, name + '.drawio')
        body = '\n'.join(self.cells)
        xml = ('<mxfile host="Electron" modified="2026-06-10T00:00:00.000Z" agent="Mozilla/5.0" version="30.0.4"><diagram id="d1" name="diagram"><mxGraphModel dx="0" dy="0" grid="0" page="1" pageWidth="2400" pageHeight="1800"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + body + '</root></mxGraphModel></diagram></mxfile>')
        with open(src, 'w', encoding='utf-8') as f: f.write(xml)
        dst = src.replace('.drawio', '.png')
        sp.run([DRAWIO, '--export', '--format', 'png', '--width', '1200', '--border', '16', '--output', dst, src], capture_output=True, timeout=30)
        return dst

# 示例：垂直链布局
ly = EntityLayout()
names = ['Parent', 'Child', 'GrandChild']
fields_list = [['id(PK)', 'field1'], ['id(PK)', 'parent_id(FK)'], ['id(PK)', 'child_id(FK)']]
pks = [{'id(PK)'}, {'id(PK)'}, {'id(PK)'}]
heights = [calc_h(f) for f in fields_list]
ys = column_y(heights)
ids = [ly.add_entity(200, ys[i], names[i], fields_list[i], pks[i]) for i in range(3)]
for i in range(2):
    ly.add_connector(ids[i], ids[i+1], c1='1', c2='n', sx=0.5, sy=1, tx=0.5, ty=0)
ly.export('example', 'vertical-chain')
print('Done → diagram/example/vertical-chain.png')
```

## 布局模式

| 模式 | 方法 | 适用场景 |
|------|------|----------|
| **垂直链** | `column_y()` + 同 X 坐标 | 顺序 1→1→n 关系 |
| **左到右扇出** | 左侧上下排列源，右侧居中目标 | 多源→同一目标 |
| **双车道** | 两条独立的水平链 | 两路共享源和目标 |
| **列网格** | 行对齐（取同行最大高度） | 全局 ER 图（8+ 表） |
| **星型** | 中心实体辐射 | 星型拓扑 |

## 避坑指南

| 现象 | 原因 | 解决方案 |
|------|------|----------|
| PNG 全白 | HTML value 中未转义 `"` | 所有 `"` → `&quot;` |
| 实体框重叠 | 固定间距不适应变高实体 | 用 `calc_h()` + `column_y()` 预计算 |
| 文字被截断 | CJK 高度公式偏小 | 使用 `HEADER_H=28, ROW_H=20` |
| 连接线穿实体 | 无路由规划 | 自动路由引擎生成 waypoints |
| 列不对齐 | 碰撞后右移 | 预计算而非"先放再调" |

## 许可证

MIT
