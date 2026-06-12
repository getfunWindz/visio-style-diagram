"""Generate all 7 software engineering diagrams for 商家管理系统."""
import os, subprocess
import xml.sax.saxutils as xesc

OUT = os.path.join(r'C:\Users\getfunWindz\Desktop\一\虚无主义\作业', 'diagram')
DRAWIO = r'C:\Program Files\draw.io\draw.io.exe'

CID = [1]
def nid():
    CID[0] += 1; return str(CID[0])
def esc(s):
    return xesc.escape(str(s), {'"': '&quot;'})

HEADER_H = 28
ROW_H = 20
ROW_GAP = 70
COL_GAP = 80

def calc_h(fields):
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

def simple_box_html(title, content_lines=None, color='#C2CFF2'):
    rows = [
        '<tr><td style="background-color:' + color + ';text-align:center;'
        'font-weight:bold;font-size:11px;padding:6px;" colspan="2">'
        + esc(title) + '</td></tr>'
    ]
    if content_lines:
        for line in content_lines:
            rows.append(
                '<tr><td style="border-top:1px solid #E8E8E8;'
                'font-size:9px;padding:3px 6px;text-align:center;" colspan="2">'
                + esc(line) + '</td></tr>')
    return '<table>' + ''.join(rows) + '</table>'

def column_y(heights, gap=ROW_GAP):
    ys = [30]
    for h in heights[:-1]:
        ys.append(ys[-1] + h + gap)
    return ys

class EntityLayout:
    def __init__(self):
        self.entities = []
        self.cells = []
        self._map = {}
        self._parent_map = {}  # child_id -> parent_id (for swimlane containment)
        self._pool_bounds = {}  # pool_id -> (x, y, w, h, header_size) for vertical pools

    def add_custom_box(self, x, y, name, html, w=190, h=None, style_extra='', parent='1'):
        eid = nid()
        sty = ('whiteSpace=wrap;html=1;rounded=0;fillColor=#FFFFFF;'
               'strokeColor=#DCDCDC;fontColor=#444444;fontSize=9;' + style_extra)
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(html) + '" '
            'style="' + sty + '" vertex="1" parent="' + parent + '">')
        if h is None:
            h = 60
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_swimlane(self, x, y, w, h, label, color='#E8F0FE', header_size=50, horizontal=True):
        """Add a pool / swimlane container.
        horizontal=True: horizontal band (swimlane shape), header on LEFT.
        horizontal=False: vertical pool — two rectangles (body + header label)."""
        if horizontal:
            eid = nid()
            sty = ('swimlane;whiteSpace=wrap;html=1;startSize=' + str(header_size) + ';'
                   'horizontal=1;fillColor=' + color + ';strokeColor=#B0B0B0;'
                   'strokeWidth=1;container=1;collapsible=0;fontSize=11;fontStyle=1;')
            self.cells.append(
                '<mxCell id="' + eid + '" value="' + esc(label) + '" '
                'style="' + sty + '" vertex="1" parent="1">')
            self.cells.append(
                '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
                'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
            self.cells.append('  </mxCell>')
            rect = (x, y, w, h)
            self.entities.append((eid, label, rect))
            self._map[eid] = rect
            return eid
        else:
            # Vertical pool body: tall rounded rectangle (container)
            body_id = nid()
            bsty = ('rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=' + color + ';'
                    'strokeColor=#888888;strokeWidth=1;container=1;collapsible=0;')
            self.cells.append(
                '<mxCell id="' + body_id + '" value="" '
                'style="' + bsty + '" vertex="1" parent="1">')
            self.cells.append(
                '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
                'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
            self.cells.append('  </mxCell>')
            # Header: rounded bar at the top, same color & width
            head_id = nid()
            hsty = ('rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=' + color + ';'
                    'strokeColor=#888888;strokeWidth=1;fontSize=11;fontStyle=1;'
                    'verticalAlign=middle;align=center;')
            self.cells.append(
                '<mxCell id="' + head_id + '" value="' + esc(label) + '" '
                'style="' + hsty + '" vertex="1" parent="1">')
            self.cells.append(
                '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
                'width="' + str(w) + '" height="' + str(header_size) + '" as="geometry"/>')
            self.cells.append('  </mxCell>')
            rect = (x, y, w, h)
            self.entities.append((body_id, label, rect))
            self._map[body_id] = rect
            self._pool_bounds[body_id] = (x, y, w, h, header_size)  # track for containment
            return body_id

    def add_uml_initial_node(self, x, y, size=16, parent='1', parent_x=0, parent_y=0):
        """UML Activity initial node: solid filled black circle.
        Arrow flows FROM this node to the first action."""
        eid = nid()
        rx = x - parent_x
        ry = y - parent_y
        self.cells.append(
            '<mxCell id="' + eid + '" value="" '
            'style="ellipse;html=1;shape=ellipse;fillColor=#000000;'
            'strokeColor=#000000;strokeWidth=1;" vertex="1" parent="' + parent + '">')
        self.cells.append(
            '    <mxGeometry x="' + str(rx) + '" y="' + str(ry) + '" '
            'width="' + str(size) + '" height="' + str(size) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        abs_rect = (x, y, size, size)
        self.entities.append((eid, 'Start', abs_rect))
        self._map[eid] = abs_rect
        if parent != '1':
            self._parent_map[eid] = parent
        return eid

    def add_uml_final_node(self, x, y, size=26, parent='1', parent_x=0, parent_y=0):
        """UML Activity final node: thick outer ring + solid inner dot (bullseye).
        x, y are absolute positions. Arrow flows TO this node."""
        eid = nid()
        rx = x - parent_x
        ry = y - parent_y
        # Outer ring: white fill, thick black stroke
        outer_style = ('ellipse;html=1;shape=ellipse;fillColor=#FFFFFF;'
                       'strokeColor=#000000;strokeWidth=3;')
        self.cells.append(
            '<mxCell id="' + eid + '" value="" '
            'style="' + outer_style + '" vertex="1" parent="' + parent + '">')
        self.cells.append(
            '    <mxGeometry x="' + str(rx) + '" y="' + str(ry) + '" '
            'width="' + str(size) + '" height="' + str(size) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        # Inner dot: solid black filled circle, smaller, centered inside outer
        inner_size = size // 2
        inner_rx = rx + (size - inner_size) // 2
        inner_ry = ry + (size - inner_size) // 2
        inner_style = ('ellipse;html=1;shape=ellipse;fillColor=#000000;'
                       'strokeColor=#000000;strokeWidth=1;')
        self.cells.append(
            '<mxCell id="' + nid() + '" value="" '
            'style="' + inner_style + '" vertex="1" parent="' + parent + '">')
        self.cells.append(
            '    <mxGeometry x="' + str(inner_rx) + '" y="' + str(inner_ry) + '" '
            'width="' + str(inner_size) + '" height="' + str(inner_size) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        abs_rect = (x, y, size, size)
        self.entities.append((eid, 'End', abs_rect))
        self._map[eid] = abs_rect
        if parent != '1':
            self._parent_map[eid] = parent
        return eid

    def add_label_in_lane(self, lane_id, lane_x, lane_y, x_rel, y_rel, w, h,
                           text, font_size=11, bold=False, color='#333333'):
        """Add a borderless text label inside a swimlane.
        Positions (x_rel, y_rel) are relative to the swimlane's top-left.
        The label has no stroke/fill — the swimlane container provides the visual frame.
        The label is automatically clamped to stay within the pool's content area
        (below the header for vertical pools)."""
        eid = nid()
        # Clamp: ensure label stays within pool bounds
        bounds = self._pool_bounds.get(lane_id)
        if bounds:
            px, py, pw, ph, hs = bounds
            # Content area: offset by header height, with padding
            pad = 6
            content_top = py + hs + pad
            content_bot = py + ph - pad
            # Convert absolute pool pos to compute valid rel range
            min_y_rel = hs + pad  # below header
            max_y_rel = ph - pad - h  # above pool bottom
            y_rel = max(min_y_rel, min(y_rel, max_y_rel))
            # Clamp x too
            min_x_rel = pad
            max_x_rel = pw - pad - w
            x_rel = max(min_x_rel, min(x_rel, max_x_rel))
            abs_x = px + x_rel
            abs_y = py + y_rel
        fw = 'font-weight:bold;' if bold else ''
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(text) + '" '
            'style="text;html=1;fontSize=' + str(font_size) + ';' + fw
            + 'fontColor=' + color + ';align=center;verticalAlign=middle;'
            'noLabel=0;" vertex="1" parent="' + lane_id + '">')
        self.cells.append(
            '    <mxGeometry x="' + str(x_rel) + '" y="' + str(y_rel) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (abs_x, abs_y, w, h)
        self.entities.append((eid, text, rect))
        self._map[eid] = rect
        self._parent_map[eid] = lane_id  # track parent for obstacle exclusion
        return eid

    def add_entity(self, x, y, name, fields, pk_set=None, w=190):
        pk = pk_set or set()
        h = calc_h(fields)
        html = entity_html(name, fields, pk)
        eid = nid()
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

    def add_connector(self, src, dst, label='', c1='', c2='',
                      sx=1, sy=0.5, tx=0, ty=0.5, style_extra=''):
        sr = self._map[src]
        dr = self._map[dst]
        ex = sr[0] + sx * sr[2]
        ey = sr[1] + sy * sr[3]
        nx = dr[0] + tx * dr[2]
        ny = dr[1] + ty * dr[3]
        excluded = {src, dst}
        # Exclude parent containers (swimlanes) for child labels
        for e in (src, dst):
            p = self._parent_map.get(e)
            if p is not None:
                excluded.add(p)
        obstacles = [r for e, _, r in self.entities if e not in excluded]
        wpts = self._route(ex, ey, nx, ny, obstacles)

        eid = nid()
        lbl = esc(label) if label else ''
        style = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                 'strokeColor=#999999;strokeWidth=1;fontSize=10;'
                 'fontColor=#444444;fontStyle=2;'
                 'labelBackgroundColor=#FFFFFF;endArrow=classic;endFill=1;'
                 'exitX={};exitY={};entryX={};entryY={};').format(sx, sy, tx, ty)
        style += style_extra
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + lbl + '" style="' + style
            + '" edge="1" parent="1" source="' + src + '" target="' + dst + '">')
        if wpts:
            pts = ''.join('        <mxPoint x="{}" y="{}"/>\n'.format(x, y) for x, y in wpts)
            self.cells.append('    <mxGeometry relative="1" as="geometry">\n' + pts + '    </mxGeometry>')
        else:
            self.cells.append('    <mxGeometry relative="1" as="geometry"/>')
        self.cells.append('  </mxCell>')

        # Cardinality labels — placed outside entity boxes
        # For source: port is ON box, label goes FURTHER OUT from box
        # For target: port is ON box, label goes FURTHER OUT from box
        for txt, is_src, px, py in [(c1, True, sx, sy), (c2, False, tx, ty)]:
            if not txt: continue
            if is_src:  # port on source box → go further away from box
                ox = 18 if px >= 0.5 else -18
                oy = 16 if py >= 0.5 else -16
            else:       # port on target box → go further away from box
                ox = -18 if px <= 0.5 else 18
                oy = -16 if py <= 0.5 else 16
            ci = nid()
            self.cells.append(
                '<mxCell id="' + ci + '" value="' + esc(txt) + '" '
                'style="text;html=1;fontSize=10;fontStyle=1;fontColor=#555555;'
                'align=center;verticalAlign=middle;" vertex="1" connectable="0" parent="1">')
            self.cells.append(
                '    <mxGeometry x="' + str(ox) + '" y="' + str(oy) + '" width="24" height="16" '
                'relative="1" as="geometry"/>')
            self.cells.append('  </mxCell>')

    MARGIN = 12  # px clearance around every entity

    @classmethod
    def _inflate(cls, r):
        """Expand rectangle r by MARGIN in all directions."""
        rx, ry, rw, rh = r
        return (rx - cls.MARGIN, ry - cls.MARGIN, rw + 2 * cls.MARGIN, rh + 2 * cls.MARGIN)

    @classmethod
    def _seg_hits(cls, p1, p2, r):
        """Check if axis-aligned segment (p1→p2) hits inflated rectangle r."""
        x1, y1 = p1; x2, y2 = p2
        rx, ry, rw, rh = cls._inflate(r)
        if x1 == x2:  # vertical
            if not (rx <= x1 <= rx + rw): return False
            return not (max(y1, y2) <= ry or min(y1, y2) >= ry + rh)
        if y1 == y2:  # horizontal
            if not (ry <= y1 <= ry + rh): return False
            return not (max(x1, x2) <= rx or min(x1, x2) >= rx + rw)
        return False  # diagonal — should not happen

    @classmethod
    def _path_ok(cls, full_path, obs):
        for i in range(len(full_path) - 1):
            for r in obs:
                if cls._seg_hits(full_path[i], full_path[i+1], r):
                    return False
        return True

    def _expand(self, pts):
        """Convert sparse waypoints to full axis-aligned path.
        Tries both bend orientations (horizontal-first and vertical-first)."""
        result = [pts[0]]
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]; x2, y2 = pts[i+1]
            if x1 != x2 and y1 != y2:
                result.append((x2, y1))  # horizontal first
            result.append(pts[i+1])
        return result

    def _expand_alt(self, pts):
        """Same as _expand but vertical-first for diagonal segments."""
        result = [pts[0]]
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]; x2, y2 = pts[i+1]
            if x1 != x2 and y1 != y2:
                result.append((x1, y2))  # vertical first
            result.append(pts[i+1])
        return result

    def _simple_path(self, pts, obs):
        """Return axis-aligned waypoints if either bend orientation is clear."""
        for expand in (self._expand, self._expand_alt):
            full = expand(pts)
            if self._path_ok(full, obs):
                return full[1:-1]
        return None

    def _find_aisle_y(self, x1, x2, obs, near_y=None, step=8):
        """Scan for a Y where a horizontal line x1→x2 is obstacle-free.
        Uses inflated rectangles for margin."""
        if not obs: return (near_y or 0)
        xL, xR = min(x1, x2), max(x1, x2)
        m = self.MARGIN
        blocks = []
        for rx, ry, rw, rh in obs:
            rx -= m; ry -= m; rw += 2 * m; rh += 2 * m  # inflate
            if rx < xR and rx + rw > xL:
                blocks.append((ry, ry + rh))
        if not blocks:
            return (near_y or 0)

        y_min = min(b[0] for b in blocks)
        y_max = max(b[1] for b in blocks)

        def clear_at(y):
            for yt, yb in blocks:
                if yt < y < yb:
                    return False
            return True

        candidates = set()
        if near_y is not None:
            for dy in range(0, max(int(y_max - y_min + 40), 200), step):
                for y in (near_y + dy, near_y - dy):
                    if y_min - 40 <= y <= y_max + 40:
                        candidates.add(round(y))
        for y in range(int(y_min) - 40, int(y_max) + 40, step):
            candidates.add(y)
        for yt, yb in blocks:
            candidates.add(yt - 2)
            candidates.add(yb + 2)
        # also try midpoints of clear gaps between blocks
        sorted_b = sorted(blocks)
        for i in range(len(sorted_b) - 1):
            gap_mid = (sorted_b[i][1] + sorted_b[i+1][0]) / 2
            candidates.add(round(gap_mid))

        best_y = None; best_dist = float('inf')
        ref = near_y if near_y is not None else 0
        for y in candidates:
            if clear_at(y):
                d = abs(y - ref)
                if d < best_dist:
                    best_dist = d
                    best_y = y
        if best_y is not None:
            return best_y
        return y_max + 20

    def _simple_path(self, pts, obs):
        """Return full axis-aligned path if all segments clear."""
        full = self._expand(pts)
        if self._path_ok(full, obs):
            return full[1:-1]  # waypoints only
        return None

    def _route(self, ex, ey, nx, ny, obs):
        if not obs: return []

        ro = max(r[0] + r[2] for r in obs) + 120
        lo = min(r[0] for r in obs) - 120
        xL, xR = min(ex, nx), max(ex, nx)
        m = self.MARGIN
        y_min = min(r[1] for r in obs) - 40 - m
        y_max = max(r[1] + r[3] for r in obs) + 40 + m

        # ── Strategy 1: direct horizontal (same Y) ──
        if ey == ny:
            p = self._simple_path([(ex, ey), (nx, ny)], obs)
            if p is not None: return p

        # ── Strategy 2: direct L-shape (one bend) ──
        for pts in [[(ex, ey), (ex, ny), (nx, ny)],
                     [(ex, ey), (nx, ey), (nx, ny)]]:
            p = self._simple_path(pts, obs)
            if p is not None: return p

        # ── Strategy 3: 2-bend via right-side margin, varied intermediate Y ──
        for my in [ny, ey, (ey + ny) / 2]:
            p = self._simple_path([(ex, ey), (ro, my), (nx, ny)], obs)
            if p is not None: return p

        # ── Strategy 4: 2-bend via left-side margin, varied intermediate Y ──
        for my in [ny, ey, (ey + ny) / 2]:
            p = self._simple_path([(ex, ey), (lo, my), (nx, ny)], obs)
            if p is not None: return p

        # ── Strategy 5: 3-bend through a clear horizontal aisle ──
        aisle_y = self._find_aisle_y(xL, xR, obs, near_y=(ey + ny) / 2)
        for ay in [aisle_y, (ey + ny) / 2, (y_min + y_max) / 2, y_min + 20, y_max - 20]:
            p = self._simple_path([(ex, ey), (ex, ay), (nx, ay), (nx, ny)], obs)
            if p is not None: return p

        # ── Strategy 6: 3-bend via right margin, horizontal through aisle ──
        for ay in [aisle_y, (ey + ny) / 2, y_min + 30, y_max - 30]:
            p = self._simple_path([(ex, ey), (ro, ey), (ro, ay), (nx, ay), (nx, ny)], obs)
            if p is not None: return p

        # ── Strategy 7: 3-bend via left margin, horizontal through aisle ──
        for ay in [aisle_y, (ey + ny) / 2, y_min + 30, y_max - 30]:
            p = self._simple_path([(ex, ey), (lo, ey), (lo, ay), (nx, ay), (nx, ny)], obs)
            if p is not None: return p

        # ── Strategy 8: 4-bend big detour around all obstacles ──
        for ay in [y_min, y_max]:
            p = self._simple_path([(ex, ey), (ex, ay), (ro, ay), (ro, ny), (nx, ny)], obs)
            if p is not None: return p
        for ay in [y_min, y_max]:
            p = self._simple_path([(ex, ey), (ex, ay), (lo, ay), (lo, ny), (nx, ny)], obs)
            if p is not None: return p

        # ── Fallback: try both margins with both bend orientations ──
        for p in [[(ex, ey), (ro, ey), (ro, ny), (nx, ny)],
                    [(ex, ey), (ro, ey), (ro, ny), (nx, ny)],
                    [(ex, ey), (lo, ey), (lo, ny), (nx, ny)],
                    [(ex, ey), (lo, ey), (lo, ny), (nx, ny)]]:
            for expand in (self._expand, self._expand_alt):
                full = expand(p)
                if self._path_ok(full, obs):
                    return full[1:-1]
        # Last resort (may still overlap)
        return self._expand([(ex, ey), (ro, ey), (ro, ny), (nx, ny)])[1:-1]

    def validate(self):
        issues = []
        eids = [e[0] for e in self.entities]
        for i, (eid1, n1, r1) in enumerate(self.entities):
            for j, (eid2, n2, r2) in enumerate(self.entities):
                if i >= j: continue
                # Skip parent-child overlaps (e.g., swimlane contains its labels)
                if self._parent_map.get(eid1) == eid2 or self._parent_map.get(eid2) == eid1:
                    continue
                x1, y1, w1, h1 = r1; x2, y2, w2, h2 = r2
                if not (x1 + w1 <= x2 or x1 >= x2 + w2
                        or y1 + h1 <= y2 or y1 >= y2 + h2):
                    dx = max(0, min(x1 + w1 - x2, x2 + w2 - x1))
                    dy = max(0, min(y1 + h1 - y2, y2 + h2 - y1))
                    issues.append(f'  OVERLAP: "{n1}" <-> "{n2}" ({dx}x{dy}px)')
        return issues

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

    def export(self, subdir, name):
        d = os.path.join(OUT, subdir)
        os.makedirs(d, exist_ok=True)
        src = os.path.join(d, name + '.drawio')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(self.to_xml())
        dst = src.replace('.drawio', '.png')
        subprocess.run(
            [DRAWIO, '--export', '--format', 'png', '--width', '1200',
             '--border', '16', '--output', dst, src],
            capture_output=True, timeout=30)
        sz = os.path.getsize(dst)
        print(f'  {os.path.basename(dst)} ({sz} bytes)')
        return dst


# ════════════════════════════════════════════════════════════
# Diagram 1: 系统上下文图 (System Context Diagram)
# ════════════════════════════════════════════════════════════
def diagram_1_context():
    """System context with 4 user roles surrounding the system."""
    ly = EntityLayout()

    # Central system
    sys_h = calc_h(['前台商城功能', '后台管理功能'])
    sys = ly.add_custom_box(290, 140, '商家管理系统',
        simple_box_html('商家管理系统', ['前台商城 · 后台管理', 'Vue3 + Django 前后端分离']),
        w=260, h=80, style_extra='rounded=1;arcSize=10;fillColor=#E8F0FE;strokeColor=#4488FF;fontSize=12;')

    # 4 roles around the system
    # Top-left: 普通用户
    ul = ly.add_custom_box(30, 30, '普通用户',
        simple_box_html('普通用户', ['浏览商品', '加入购物车', '下单购买', '查看订单']),
        w=180, h=110)

    # Bottom-left: 商家
    bl = ly.add_custom_box(30, 260, '商家',
        simple_box_html('商家', ['查看/修改商家信息', '管理自有商品', '提交业务申请']),
        w=180, h=100)

    # Top-right: 高级商家
    ur = ly.add_custom_box(620, 30, '高级商家',
        simple_box_html('高级商家', ['普通商家全部权限', '商品上架/下架', '提交权限升级申请']),
        w=180, h=110)

    # Bottom-right: 系统管理员
    br = ly.add_custom_box(620, 260, '系统管理员',
        simple_box_html('系统管理员', ['审核业务申请', '管理所有商家/商品', '系统维护', '用户管理']),
        w=180, h=110)

    # Connectors from roles to system
    ly.add_connector(ul, sys, label='访问商城', sx=1, sy=0.5, tx=0, ty=0.3)
    ly.add_connector(bl, sys, label='管理经营', sx=1, sy=0.5, tx=0, ty=0.7)
    ly.add_connector(sys, ur, label='提供增值', sx=1, sy=0.3, tx=0, ty=0.5)
    ly.add_connector(sys, br, label='系统运维', sx=1, sy=0.7, tx=0, ty=0.5)

    for i in ly.validate():
        print(i)
    ly.export('01-system-context', 'system-context')


# ════════════════════════════════════════════════════════════
# Diagram 2: 业务审核活动图 (Business Review Activity with Swimlanes)
# ════════════════════════════════════════════════════════════
def diagram_2_review_flow():
    """Business review activity diagram (UML 2.5 Activity Diagram) with
    vertical swimlanes (partitions), UML initial node (solid circle) and final node."""
    ly = EntityLayout()

    # ── Layout constants ──
    # Three vertical lanes side by side: Merchant | Admin | System
    lane_w = 240       # each lane width
    lane_h = 520       # lane height (taller than wide = vertical pool)
    lane_top = 80      # header area at top
    head_h = 50        # vertical lane header height
    gap = 20
    x0 = 40            # left edge of first lane

    # Colors per role
    role_colors = [
        ('商家 (Merchant)', '#FFF3CD'),
        ('管理员 (Admin)', '#E8F0FE'),
        ('系统 (System)', '#D4EDDA'),
    ]

    lane_ids = []
    for i, (name, color) in enumerate(role_colors):
        x = x0 + i * (lane_w + gap)
        lid = ly.add_swimlane(x, lane_top, lane_w, lane_h, name,
                               color=color, header_size=head_h, horizontal=False)
        lane_ids.append(lid)

    # ── UML Initial Node (solid circle) — inside Merchant lane, below header ──
    init_center_x = x0 + 60 + 70  # align with label center
    init = ly.add_uml_initial_node(init_center_x - 8, lane_top + head_h + 20, 16,
                                    parent=lane_ids[0], parent_x=x0, parent_y=lane_top)

    # ── Activity labels (bold, borderless) inside each vertical lane ──
    # Merchant lane (index 0)
    m_submit = ly.add_label_in_lane(lane_ids[0], x0, lane_top,
                                     60, 100, 140, 36, '提交申请', bold=True, color='#8B6914')

    # Admin lane (index 1)
    a_review = ly.add_label_in_lane(lane_ids[1], x0 + lane_w + gap, lane_top,
                                     60, 80, 140, 36, '审核申请', bold=True, color='#1A5C8A')
    a_decision = ly.add_label_in_lane(lane_ids[1], x0 + lane_w + gap, lane_top,
                                       60, 180, 140, 36, '审核通过？', bold=True, color='#8B6914')

    # System lane (index 2)
    s_process = ly.add_label_in_lane(lane_ids[2], x0 + 2 * (lane_w + gap), lane_top,
                                      60, 80, 140, 36, '自动执行业务', bold=True, color='#1A6B1A')
    s_reject = ly.add_label_in_lane(lane_ids[2], x0 + 2 * (lane_w + gap), lane_top,
                                     60, 180, 140, 36, '驳回申请', bold=True, color='#A52A2A')
    s_end = ly.add_label_in_lane(lane_ids[2], x0 + 2 * (lane_w + gap), lane_top,
                                   80, 380, 100, 36, '流程结束', bold=False, color='#666666')

    # ── UML Final Node (bullseye) — inside System lane, well above pool bottom ──
    sys_x = x0 + 2 * (lane_w + gap)
    sys_y = lane_top
    final = ly.add_uml_final_node(sys_x + lane_w // 2 - 13, sys_y + lane_h - 50,
                                   26, parent=lane_ids[2], parent_x=sys_x, parent_y=sys_y)

    # ── Decision label ──
    ci = nid()
    ly.cells.append(
        '<mxCell id="' + ci + '" value="根据审核结果判断" '
        'style="text;html=1;fontSize=9;fontColor=#888888;fontStyle=2;'
        'align=center;verticalAlign=middle;" vertex="1" connectable="0" parent="1">')
    ly.cells.append(
        '    <mxGeometry x="' + str(x0 + lane_w + gap + 30) + '" y="' + str(lane_top + 155) + '" '
        'width="120" height="16" as="geometry"/>')
    ly.cells.append('  </mxCell>')

    # ── Connectors (clean orthogonal routing) ──
    # Start → 提交申请 (within merchant, top-down)
    ly.add_connector(init, m_submit, label='', sx=0.5, sy=1, tx=0.5, ty=0)
    # 提交申请 → 审核申请 (cross lane: merchant→admin, right→left horizontal)
    ly.add_connector(m_submit, a_review, label='提交申请', sx=1, sy=0.5, tx=0, ty=0.5)
    # 审核申请 → 审核通过？ (within admin, top-down)
    ly.add_connector(a_review, a_decision, label='审核完成', sx=0.5, sy=1, tx=0.5, ty=0)
    # 审核通过? YES → 自动执行业务 (cross lane: admin→system, right→left horizontal)
    ly.add_connector(a_decision, s_process, label='通过', sx=1, sy=0.3, tx=0, ty=0.3)
    # 审核通过? NO → 驳回申请 (cross lane: admin→system, right→left horizontal, lower)
    ly.add_connector(a_decision, s_reject, label='驳回', sx=1, sy=0.7, tx=0, ty=0.7)
    # 自动执行业务 → 流程结束 (within system, top-down)
    ly.add_connector(s_process, s_end, label='执行完成', sx=0.5, sy=1, tx=0.5, ty=0)
    # 驳回申请 → 流程结束 (within system, top-down)
    ly.add_connector(s_reject, s_end, label='', sx=0.5, sy=1, tx=0.5, ty=0)
    # 流程结束 → Final Node (within system, top-down)
    ly.add_connector(s_end, final, label='', sx=0.5, sy=1, tx=0.5, ty=0)

    for i in ly.validate():
        print(i)
    ly.export('02-review-activity', 'review-activity')


# ════════════════════════════════════════════════════════════
# Diagram 3: 系统分层架构图 (System Layered Architecture)
# ════════════════════════════════════════════════════════════
def diagram_3_layered_arch():
    """4-layer architecture stack with components."""
    ly = EntityLayout()

    layers = [
        ('表现层 (Presentation Layer)', '#C2CFF2',
         ['Vue3 + Element Plus + Pinia', '商城界面 (用户端)  |  管理界面 (管理端)', 'Axios HTTP 通信 · 路由守卫 · 状态管理']),
        ('业务逻辑层 (Business Logic Layer)', '#D4EDDA',
         ['Django REST Framework · ViewSet · Serializer', '权限校验 · 业务审核 · 订单处理', 'RESTful API 接口封装 · 统一异常处理']),
        ('数据访问层 (Data Access Layer)', '#FFF3CD',
         ['Django ORM · Model 定义', '数据查询/过滤/排序 · 事务管理', 'django-filter 多条件筛选']),
        ('数据存储层 (Data Storage Layer)', '#F8D7DA',
         ['MySQL 5.7 · utf8mb4', '用户/角色/商家/商品/订单 数据表', 'PyMySQL 数据库驱动 · 外键约束']),
    ]

    x, w_total = 30, 800
    current_y = 30
    ids = []
    for title, color, lines in layers:
        html = simple_box_html(title, lines, color=color)
        h = HEADER_H + len(lines) * ROW_H + 4
        eid = ly.add_custom_box(x, current_y, title, html, w=w_total, h=h,
                                style_extra='rounded=0;fillColor=#FFFFFF;strokeColor=' + color[1:] + ';strokeWidth=2;')
        ids.append(eid)
        current_y += h + 4

    # Vertical arrows between layers
    for i in range(len(ids) - 1):
        ly.add_connector(ids[i], ids[i+1], label='', c1='', c2='',
                         sx=0.5, sy=1, tx=0.5, ty=0)

    for i in ly.validate():
        print(i)
    ly.export('03-layered-architecture', 'layered-architecture')


# ════════════════════════════════════════════════════════════
# Diagram 4: 系统技术架构图 (System Technology Architecture)
# ════════════════════════════════════════════════════════════
def diagram_4_tech_arch():
    """3-column technology stack diagram."""
    ly = EntityLayout()

    # 3 columns: Frontend, Backend, Database
    col_w = 250
    x0, x1, x2 = 30, 350, 670

    # Frontend column
    fe_html = simple_box_html('前端技术栈 (Frontend)', [
        'Vue 3 (Composition API)',
        'Pinia (状态管理)',
        'Element Plus (UI组件)',
        'Vite (构建工具)',
        'Axios (HTTP请求)',
        'TypeScript',
        'Vue Router (路由管理)',
    ], color='#C2CFF2')
    fe_id = ly.add_custom_box(x0, 30, '前端技术栈', fe_html, w=col_w, h=200)

    # Backend column
    be_html = simple_box_html('后端技术栈 (Backend)', [
        'Django 4.2 (MTV框架)',
        'Django REST Framework',
        'SimpleJWT (用户认证)',
        '自定义权限校验',
        'Django ORM (数据持久化)',
        '统一异常处理',
        'django-filter (过滤)',
    ], color='#D4EDDA')
    be_id = ly.add_custom_box(x1, 30, '后端技术栈', be_html, w=col_w, h=200)

    # Database column
    db_html = simple_box_html('数据层 (Data Layer)', [
        'MySQL 5.7',
        'utf8mb4 字符集',
        '外键约束',
        '索引优化',
        'PyMySQL 驱动',
        'Django 迁移机制',
        '数据备份/恢复',
    ], color='#FFF3CD')
    db_id = ly.add_custom_box(x2, 30, '数据层', db_html, w=col_w, h=200)

    # Data flow arrows
    ly.add_connector(fe_id, be_id, label='HTTP JSON (RESTful API)', sx=1, sy=0.3, tx=0, ty=0.3)
    ly.add_connector(be_id, fe_id, label='响应数据', sx=0, sy=0.7, tx=1, ty=0.7)

    ly.add_connector(be_id, db_id, label='ORM 读写', sx=1, sy=0.5, tx=0, ty=0.5)

    for i in ly.validate():
        print(i)
    ly.export('04-tech-architecture', 'tech-architecture')


# ════════════════════════════════════════════════════════════
# Diagram 5: 系统部署架构图 (System Deployment Architecture)
# ════════════════════════════════════════════════════════════
def diagram_5_deployment():
    """Deployment topology: Browser → Vite → Django → MySQL."""
    ly = EntityLayout()

    # Browser
    browser = ly.add_custom_box(30, 80, '浏览器 (Browser)',
        simple_box_html('浏览器 (Browser)', ['Chrome 90+ / Edge 90+', '用户访问入口']),
        w=170, h=80, style_extra='rounded=1;arcSize=8;')

    # Vite Dev Server
    vite = ly.add_custom_box(300, 80, 'Vite 开发服务器',
        simple_box_html('Vite 开发服务器', ['端口: 5173', '静态资源响应', '/api/* 代理转发']),
        w=190, h=100, style_extra='rounded=1;arcSize=8;fillColor=#E8F0FE;')

    # Django App Server
    django = ly.add_custom_box(600, 80, 'Django 应用服务器',
        simple_box_html('Django 应用服务器', ['端口: 8000', 'RESTful API 处理', 'DRF ViewSet 业务逻辑']),
        w=190, h=100, style_extra='rounded=1;arcSize=8;fillColor=#D4EDDA;')

    # MySQL
    mysql = ly.add_custom_box(890, 80, 'MySQL 数据库',
        simple_box_html('MySQL 5.7', ['端口: 3306', '数据持久化存储']),
        w=170, h=80, style_extra='rounded=1;arcSize=8;fillColor=#FFF3CD;')

    # Connectors
    ly.add_connector(browser, vite, label='HTTP 请求页面', sx=1, sy=0.5, tx=0, ty=0.4)
    ly.add_connector(vite, browser, label='返回页面/组件', sx=0, sy=0.6, tx=1, ty=0.6)
    ly.add_connector(vite, django, label='代理 /api/* 请求', sx=1, sy=0.5, tx=0, ty=0.4)
    ly.add_connector(django, vite, label='JSON 响应数据', sx=0, sy=0.6, tx=1, ty=0.6)
    ly.add_connector(django, mysql, label='ORM 数据库读写', sx=1, sy=0.5, tx=0, ty=0.5)

    for i in ly.validate():
        print(i)
    ly.export('05-deployment', 'deployment-architecture')


# ════════════════════════════════════════════════════════════
# Diagram 6: 系统功能模块结构图 (System Module Structure)
# ════════════════════════════════════════════════════════════
def diagram_6_module_tree():
    """Tree structure of system modules."""
    ly = EntityLayout()

    # Root
    root = ly.add_custom_box(250, 20, '商家管理系统',
        simple_box_html('商家管理系统', ['前后端分离 · B/S 架构']),
        w=300, h=70, style_extra='rounded=1;arcSize=8;fillColor=#C2CFF2;strokeColor=#8888FF;strokeWidth=2;fontSize=12;')

    # Frontend modules (left)
    fe_boxes = [
        (40, 150, 220, 60, '前台用户模块', '#E8F0FE', '商城首页 · 商品浏览'),
        (40, 250, 220, 60, '购物车模块', '#E8F0FE', '添加 · 修改 · 删除 · 结算'),
        (40, 350, 220, 60, '订单管理模块', '#E8F0FE', '下单 · 状态查询 · 支付'),
    ]
    fe_ids = []
    for x, y, w, h, title, color, desc in fe_boxes:
        eid = ly.add_custom_box(x, y, title,
            simple_box_html(title, [desc] if desc else None, color=color),
            w=w, h=h, style_extra='rounded=1;arcSize=6;')
        fe_ids.append(eid)

    # Backend modules (right)
    be_boxes = [
        (560, 150, 220, 60, '用户权限管理', '#D4EDDA', '注册登录 · JWT · 角色分级'),
        (560, 250, 220, 60, '商家/商品管理', '#D4EDDA', 'CRUD · 图片上传 · 状态控制'),
        (560, 350, 220, 60, '业务审核管理', '#D4EDDA', '申请提交 · 审批 · 自动执行'),
        (560, 450, 220, 60, '系统维护模块', '#D4EDDA', '操作日志 · 用户管理 · 反馈'),
    ]
    be_ids = []
    for x, y, w, h, title, color, desc in be_boxes:
        eid = ly.add_custom_box(x, y, title,
            simple_box_html(title, [desc] if desc else None, color=color),
            w=w, h=h, style_extra='rounded=1;arcSize=6;')
        be_ids.append(eid)

    # Connectors: root → each module
    for eid in fe_ids:
        ly.add_connector(root, eid, sx=0.3, sy=1, tx=0.5, ty=0)
    for i, eid in enumerate(be_ids):
        ly.add_connector(root, eid, sx=0.7, sy=1, tx=0.5, ty=0)

    # Labels for the two branches
    ci = nid()
    ly.cells.append(
        '<mxCell id="' + ci + '" value="前台商城端" '
        'style="text;html=1;fontSize=10;fontStyle=2;fontColor=#555555;'
        'align=center;verticalAlign=middle;" vertex="1" connectable="0" parent="1">')
    ly.cells.append(
        '    <mxGeometry x="90" y="110" width="90" height="20" as="geometry"/>')
    ly.cells.append('  </mxCell>')

    ci = nid()
    ly.cells.append(
        '<mxCell id="' + ci + '" value="后台管理端" '
        'style="text;html=1;fontSize=10;fontStyle=2;fontColor=#555555;'
        'align=center;verticalAlign=middle;" vertex="1" connectable="0" parent="1">')
    ly.cells.append(
        '    <mxGeometry x="620" y="110" width="90" height="20" as="geometry"/>')
    ly.cells.append('  </mxCell>')

    for i in ly.validate():
        print(i)
    ly.export('06-module-structure', 'module-structure')


# ════════════════════════════════════════════════════════════
# Diagram 7: 系统整体E-R图 (Global E-R Diagram)
# ════════════════════════════════════════════════════════════
def diagram_7_global_er():
    """Complete ER diagram with all entities and relationships."""
    ly = EntityLayout()
    W = 200
    X = [20, 280, 540, 800, 1060]

    # Define all entities per column
    cols = [
        [  # col 0: Permission & User
            ('sys_role (角色)',
             ['role_id(PK)', 'code(角色编码)', 'name(角色名称)'],
             {'role_id(PK)'}),
            ('sys_user (用户)',
             ['id(PK)', 'username(用户名)', 'password(密码)', 'role_id(FK)',
              'merchant_id(FK)', 'status(状态)', 'date_joined(注册时间)'],
             {'id(PK)'}),
            ('sys_maintenance_feedback (维护反馈)',
             ['feedback_id(PK)', 'user_id(FK)', 'content(内容)',
              'status(状态)', 'created_time(创建时间)'],
             {'feedback_id(PK)'}),
        ],
        [  # col 1: Merchant & Category
            ('mer_merchant (商家)',
             ['merchant_id(PK)', 'merchant_name(商家名称)',
              'merchant_number(商家编号)', 'merchant_status(状态)',
              'created_time(创建时间)'],
             {'merchant_id(PK)'}),
            ('mer_category (商品分类)',
             ['category_id(PK)', 'name(分类名称)', 'parent_id(FK,自关联)'],
             {'category_id(PK)'}),
            ('mer_apply (业务申请)',
             ['apply_id(PK)', 'merchant_id(FK)', 'type(申请类型)',
              'content(申请内容)', 'status(状态)', 'created_time(提交时间)',
              'review_time(审核时间)'],
             {'apply_id(PK)'}),
        ],
        [  # col 2: Goods
            ('mer_goods (商品)',
             ['goods_id(PK)', 'merchant_id(FK)', 'category_id(FK)',
              'name(商品名称)', 'description(描述)', 'price(单价)',
              'stock(库存)', 'status(状态)', 'created_time(创建时间)'],
             {'goods_id(PK)'}),
        ],
        [  # col 3: Cart
            ('trade_cart (购物车)',
             ['cart_id(PK)', 'user_id(FK,唯一)'],
             {'cart_id(PK)'}),
            ('trade_cart_item (购物车项目)',
             ['item_id(PK)', 'cart_id(FK)', 'goods_id(FK)',
              'quantity(数量)'],
             {'item_id(PK)'}),
        ],
        [  # col 4: Order
            ('trade_order (订单)',
             ['order_id(PK)', 'user_id(FK)', 'total_amount(总金额)',
              'status(状态)', 'created_time(下单时间)'],
             {'order_id(PK)'}),
            ('trade_order_item (订单明细)',
             ['item_id(PK)', 'order_id(FK)', 'goods_id(FK)',
              'quantity(数量)', 'price(单价)'],
             {'item_id(PK)'}),
        ],
    ]

    max_rows = max(len(c) for c in cols)
    row_heights = []
    for ri in range(max_rows):
        max_h = 0
        for c in cols:
            if ri < len(c):
                h = calc_h(c[ri][1])
                max_h = max(max_h, h)
        row_heights.append(max_h)

    ys = column_y(row_heights, gap=120)

    placed = {}
    for ci, col in enumerate(cols):
        for ri, (name, fields, pk) in enumerate(col):
            eid = ly.add_entity(X[ci], ys[ri], name, fields, pk, w=W)
            placed[(ci, ri)] = eid

    # Intra-column vertical connections
    # col 0: role → user, user → feedback
    ly.add_connector(placed[(0, 0)], placed[(0, 1)], label='属于', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)
    ly.add_connector(placed[(0, 1)], placed[(0, 2)], label='提交', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)

    # col 1: merchant → category, merchant → apply
    ly.add_connector(placed[(1, 0)], placed[(1, 1)], label='拥有', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)
    ly.add_connector(placed[(1, 0)], placed[(1, 2)], label='提交', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)

    # col 3: cart → cart_item
    ly.add_connector(placed[(3, 0)], placed[(3, 1)], label='包含', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)

    # col 4: order → order_item
    ly.add_connector(placed[(4, 0)], placed[(4, 1)], label='包含', c1='1', c2='n',
                     sx=0.5, sy=1, tx=0.5, ty=0)

    # Inter-column horizontal connections
    # user → merchant (N:1)
    ly.add_connector(placed[(0, 1)], placed[(1, 0)], label='关联商家', c1='n', c2='1')
    # merchant → goods (1:N)
    ly.add_connector(placed[(1, 0)], placed[(2, 0)], label='发布', c1='1', c2='n')
    # category → goods (1:N)
    ly.add_connector(placed[(1, 1)], placed[(2, 0)], label='分类', c1='1', c2='n',
                     sx=1, sy=0.5, tx=0, ty=0.5)
    # user → cart (1:1)
    ly.add_connector(placed[(0, 1)], placed[(3, 0)], label='拥有', c1='1', c2='1')
    # goods → cart_item (1:N)
    ly.add_connector(placed[(2, 0)], placed[(3, 1)], label='被加入', c1='1', c2='n',
                     sx=1, sy=0.5, tx=0, ty=0.5)
    # user → order (1:N)
    ly.add_connector(placed[(0, 1)], placed[(4, 0)], label='提交', c1='1', c2='n')
    # goods → order_item (1:N)
    ly.add_connector(placed[(2, 0)], placed[(4, 1)], label='被购买', c1='1', c2='n',
                     sx=1, sy=0.5, tx=0, ty=0.5)

    for i in ly.validate():
        print(i)
    ly.export('07-global-er', 'global-er')


# ════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)

    diagrams = [
        (diagram_1_context, '1. 系统上下文图 (System Context)'),
        (diagram_2_review_flow, '2. 业务审核活动图 (Review Activity)'),
        (diagram_3_layered_arch, '3. 系统分层架构图 (Layered Architecture)'),
        (diagram_4_tech_arch, '4. 系统技术架构图 (Tech Architecture)'),
        (diagram_5_deployment, '5. 系统部署架构图 (Deployment)'),
        (diagram_6_module_tree, '6. 系统功能模块结构图 (Module Structure)'),
        (diagram_7_global_er, '7. 系统整体E-R图 (Global ER)'),
    ]
    for fn, name in diagrams:
        print(f'=== {name} ===')
        fn()
    print('\nAll diagrams generated successfully!')
