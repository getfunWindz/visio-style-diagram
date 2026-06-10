---
name: visio-style-diagram
description: |
  Generate Visio-style software engineering diagrams via draw.io Desktop.
  Use when user asks for: Visio风格图 / 数据库ER图 / 实体关系图 / 类图 / 架构图 /
  draw.io图 / 软件工程图 / 数据库设计图 / 系统部署图 / 数据流图 / UML图.
  Requires draw.io Desktop installed at C:\Program Files\draw.io\draw.io.
---

# Visio-Style Diagram Generator

Generate Visio-style software engineering diagrams via **draw.io Desktop**.
Outputs `.drawio` (editable XML) + `.png` (max 1200px wide).

**All generated files go into a `diagram/` subfolder** for centralized management.

## Visual Specification

Match this style exactly (researched from real Visio screenshots):

```
Canvas background: #EBEBEB (light gray, Visio canvas)
Entity body:       #FFFFFF (white), thin #DCDCDC border
Entity header:     #C2CFF2 (light pastel blue), bold black text
Field text:        #444444 (dark gray), 9px
PK field:          bold (#000000), no color highlighting
Separators:        #E8E8E8, 1px, between field rows
Connectors:        1pt solid #999999, orthogonal routing
Cardinality:       #555555 bold, text label near endpoint
Label style:       italic, centered on line, white label bg
```

**DO NOT use**: gradients, shadows, rounded corners, colored fills (except header), dark borders, circles around cardinality markers.

## Prerequisites

1. draw.io Desktop installed: `C:\Program Files\draw.io\draw.io`
2. Python 3.10+ with `xml.sax.saxutils` (stdlib, no extra install)

## Core Workflow

```
User request → Python script (EntityLayout engine) → .drawio XML → draw.io CLI → .png
Output goes to: <project>/diagram/<subdir>/
```

### Step 1: Generate draw.io XML

Write a Python script using the **EntityLayout engine** that:
1. Registers entity boxes with auto-sizing and collision detection
2. Connects entities via obstacle-aware orthogonal routing
3. Validates all bounding boxes have zero overlap before export

**Entity HTML structure** (one line in XML `value` attribute):

```python
'<table>'
'<tr><td style="background-color:#C2CFF2;text-align:center;font-weight:bold;font-size:11px;padding:4px;" colspan="2">EntityName</td></tr>'
'<tr><td style="border-top:1px solid #E8E8E8;font-size:9px;padding:3px 6px;" colspan="2">field_name</td></tr>'
'<tr><td style="border-top:1px solid #E8E8E8;font-size:9px;padding:3px 6px;" colspan="2"><b>pk_field</b></td></tr>'
'</table>'
```

**CRITICAL XML escaping**: All double quotes `"` inside the HTML value must be escaped as `&quot;`. Use:
```python
import xml.sax.saxutils as xesc
def esc(s): return xesc.escape(str(s), {'"': '&quot;'})
```

### Step 2: Export to PNG

```powershell
& "C:\Program Files\draw.io\draw.io" --export --format png --width 1200 --border 16 --output diagram\out.png diagram\input.drawio
```

Output constraints:
- Max width: **1200px** (`--width 1200`)
- Height: auto (draw.io crops to content)
- All outputs in `diagram/` subfolder

### Step 3: Open in draw.io (optional)

User can open `.drawio` files in draw.io GUI to adjust, add shapes, or re-export.

## CJK Entity Height Formula

draw.io renders Chinese/Japanese text ~15% taller than Latin at the same point size.
Use these constants for all CJK diagrams:

```python
HEADER_H = 28      # header row (11px bold CJK text + 4px pad*2)
ROW_H = 20         # each field row (9px CJK text + 3px pad*2 + 1px border + buffer)
ENTITY_W = 190     # default entity width
COL_GAP = 60       # min px between columns
ROW_GAP = 70       # min px between rows in same column

def calc_h(fields):
    return HEADER_H + len(fields) * ROW_H + 4
```

## ⚠️ Critical: Collision-Free Layout

Connector lines **must not** cross through other entity boxes, and entity boxes **must not** overlap. Follow these rules:

### Rule 1: Pre-compute Y positions

Do not use fixed gaps. Compute Y positions from actual entity heights:

```python
def column_y(heights, gap=ROW_GAP):
    ys = [20]
    for h in heights[:-1]:
        ys.append(ys[-1] + h + gap)
    return ys
```

### Rule 2: Use explicit port positions

Every connector must specify `exitX/exitY` (source port) and `entryX/entryY` (target port):

| Port values | Meaning |
|-------------|---------|
| `sx=1 sy=0.5` | Right side center (default for left→right) |
| `tx=0 ty=0.5` | Left side center (default for left→right) |
| `sx=0.5 sy=1, tx=0.5 ty=0` | Bottom→Top (vertical chain) |
| `sx=1 sy=0.5, tx=1 ty=0.5` | Right→Right (detour around obstacles) |

### Rule 3: Obstacle-aware routing with waypoints

The routing algorithm:
1. Collects all entity bounding boxes as obstacles
2. Tries 2-bend path (right, then up/down, then left)
3. If blocked, tries 3-bend (up/down through a clear horizontal aisle)
4. If still blocked, tries 4-bend big detour
5. Validates the path doesn't intersect any obstacle

### Rule 4: Row-aligned column grid

For multi-column diagrams, align entities by row index. Compute the tallest entity in each row across all columns, then use that height for Y spacing:

```python
# Compute row Y positions
row_heights = []
for ri in range(max_rows):
    max_h = max(calc_h(col[ri][1]) for col in cols if ri < len(col))
    row_heights.append(max_h)
ys = column_y(row_heights)
```

### Rule 5: Validate before export

Always call `validate()` which checks every entity pair for bounding box overlap:

```python
issues = ly.validate()
for i in issues:
    print(i)   # prints "OVERLAP: "A" <-> "B" (XxYpx)" if any
```

## Example Implementation

Below is the complete **EntityLayout engine** template. Copy and adapt for each project.

```python
"""draw.io Visio-style diagram — EntityLayout engine (collision-free)."""
import os, subprocess
import xml.sax.saxutils as xesc

OUT = r'output_directory\diagram'   # all files go to diagram/
DRAWIO = r'C:\Program Files\draw.io\draw.io'

CID = [1]
def nid():
    CID[0] += 1; return str(CID[0])
def esc(s):
    return xesc.escape(str(s), {'"': '&quot;'})

# CJK-optimized constants
HEADER_H = 28
ROW_H = 20
ENTITY_W = 190
COL_GAP = 60
ROW_GAP = 70

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

def column_y(heights, gap=ROW_GAP):
    ys = [20]
    for h in heights[:-1]:
        ys.append(ys[-1] + h + gap)
    return ys

class EntityLayout:
    def __init__(self):
        self.entities = []   # [(eid, name, (x,y,w,h))]
        self.cells = []
        self._map = {}

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
            if not txt: continue
            ci = nid()
            self.cells.append(
                '<mxCell id="' + ci + '" value="' + esc(txt) + '" '
                'style="text;html=1;fontSize=10;fontStyle=1;fontColor=#555555;'
                'align=center;verticalAlign=middle;" vertex="1" connectable="0" parent="1">')
            self.cells.append(
                '    <mxGeometry x="' + str(ox) + '" y="-14" width="24" height="16" '
                'relative="1" as="geometry"/>')
            self.cells.append('  </mxCell>')

    @staticmethod
    def _line_hits(x1, y1, x2, y2, r):
        rx, ry, rw, rh = r
        if x1 == x2:  # vertical
            if not (rx <= x1 <= rx + rw): return False
            return not (max(y1, y2) <= ry or min(y1, y2) >= ry + rh)
        if y1 == y2:  # horizontal
            if not (ry <= y1 <= ry + rh): return False
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
        """Obstacle-avoiding orthogonal route with 2/3/4-bend strategies."""
        if not obs:
            return []
        ro = max(r[0] + r[2] for r in obs) + 80
        to = min(r[1] for r in obs) - 60
        bo = max(r[1] + r[3] for r in obs) + 60
        # 2-bend
        for my in [ny, ey, (ey + ny) / 2, to + 30, bo - 30]:
            p = [(ex, ey), (ro, my), (nx, ny)]
            if self._path_ok(p, obs):
                return [(ro, my)]
        # 3-bend
        for my in [to, bo, (to + bo) / 2]:
            for mx in [ex, nx, ro]:
                p = [(ex, ey), (ex, my), (mx, my), (nx, ny)]
                if self._path_ok(p, obs):
                    return [(ex, my), (mx, my)]
        # 4-bend
        p = [(ex, ey), (ex, to), (ro, to), (ro, ny), (nx, ny)]
        if self._path_ok(p, obs): return [(ex, to), (ro, to), (ro, ny)]
        p = [(ex, ey), (ex, bo), (ro, bo), (ro, ny), (nx, ny)]
        if self._path_ok(p, obs): return [(ex, bo), (ro, bo), (ro, ny)]
        return [(ro, ey), (ro, ny)]

    def validate(self):
        """Check all entity pairs for bounding box overlap."""
        issues = []
        for i, (_, n1, r1) in enumerate(self.entities):
            for j, (_, n2, r2) in enumerate(self.entities):
                if i >= j: continue
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
        return dst

# ── Example usage ──────────────────────────────────────────

def example_vertical_chain():
    """Vertical chain with auto-computed Y positions."""
    ly = EntityLayout()
    names = ['Parent', 'Child', 'GrandChild']
    fields_list = [
        ['id(PK)', 'field1'],
        ['id(PK)', 'parent_id(FK)', 'field2'],
        ['id(PK)', 'child_id(FK)'],
    ]
    pks = [{'id(PK)'}, {'id(PK)'}, {'id(PK)'}]
    heights = [calc_h(f) for f in fields_list]
    ys = column_y(heights, gap=50)
    ids = [ly.add_entity(200, ys[i], names[i], fields_list[i], pks[i])
           for i in range(3)]
    for i in range(2):
        ly.add_connector(ids[i], ids[i+1], c1='1', c2='n',
                         sx=0.5, sy=1, tx=0.5, ty=0)
    for i in ly.validate():
        print(i)
    ly.export('example', 'vertical-chain')

def example_column_grid():
    """Column grid with row-aligned Y positions."""
    ly = EntityLayout()
    cols = [
        [('A', ['id(PK)', 'a_val'], {'id(PK)'}),
         ('B', ['id(PK)', 'b_val'], {'id(PK)'})],
        [('C', ['id(PK)', 'c_val', 'c_extra'], {'id(PK)'}),
         ('D', ['id(PK)', 'd_val'], {'id(PK)'}),
         ('E', ['id(PK)', 'e_val'], {'id(PK)'})],
    ]
    max_rows = max(len(c) for c in cols)
    row_h = [max(calc_h(c[ri][1]) for c in cols if ri < len(c))
             for ri in range(max_rows)]
    ys = column_y(row_h)
    placed = {}
    for ci, col in enumerate(cols):
        for ri, (name, fields, pk) in enumerate(col):
            eid = ly.add_entity(30 + ci * 350, ys[ri], name, fields, pk)
            placed[(ci, ri)] = eid
    for ci, col in enumerate(cols):
        for ri in range(len(col) - 1):
            ly.add_connector(placed[(ci, ri)], placed[(ci, ri+1)],
                             sx=0.5, sy=1, tx=0.5, ty=0)
    for i in ly.validate(): print(i)
    ly.export('example', 'column-grid')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    example_vertical_chain()
    example_column_grid()
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|------|
| PNG is blank (all white) | Unescaped `"` in HTML value attribute | Ensure ALL `"` in HTML → `&quot;` via `esc()` |
| PNG is blank (0 non-white pixels) | Multi-line XML value attribute | Join HTML table to ONE line in `value="..."` |
| Entity boxes overlap | Fixed gap doesn't account for varying entity heights | Use `calc_h()` + `column_y()` to compute positions from actual heights |
| Connector line passes through entity | No waypoints or wrong port positions | Obstacle routing auto-generates waypoints; check obstacles list |
| Text is cut off in entity box | Height formula too small for CJK text | Use `HEADER_H=28, ROW_H=20` for CJK content |
| Export fails silently | draw.io CLI needs display | Run once in GUI to test; use `--no-sandbox` if needed |

## Diagram Types

The same HTML-table approach adapts to any software engineering diagram:

- **ER/Data diagrams**: entities as tables → fields as rows → connectors as relationships
- **UML Class diagrams**: class box = table header (stereotype) + attributes + methods
- **Architecture diagrams**: component = table with header (name) + rows (endpoints/ports)
- **Flowcharts**: use regular `rounded=1` rectangles (not tables) connected by edges
- **Deployment diagrams**: nodes as tables, artifacts as child rows

## Layout Pattern Reference

Choose the right layout pattern based on relationship topology:

| Pattern | Positioning method | When to use |
|---------|--------------------|-------------|
| **Vertical chain** | `column_y()` with fixed x | Sequential 1→1→n relationships |
| **Left-to-right fan** | Manual y-offsets, center target | Two+ sources connect to same target |
| **Dual lane** | Two `column_y()` chains at diff y | Two independent paths with shared source+target |
| **Column grid** | Row-aligned via `max_rows` + `column_y()` | Global ER diagrams with 8+ tables |
| **Hub-and-spoke** | Manual placement around center | Star topology |

## Visual Style Reference

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

## Dependencies

- **draw.io Desktop** (free): https://github.com/jgraph/drawio-desktop/releases
- **Python 3.10+** (stdlib only: `os`, `subprocess`, `xml.sax.saxutils`)
- **No pip packages required**
