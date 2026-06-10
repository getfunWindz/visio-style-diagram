# Visio-Style Diagram Generator

Visio 风格的软件工程图自动生成器。基于 **draw.io Desktop** + **Python 标准库**，零外部依赖，通过代码定义实体和关系，自动生成可编辑的 `.drawio` 文件和 `.png` 图片。

```
用户需求 → Python 脚本（EntityLayout 引擎）→ .drawio XML → draw.io CLI → .png
                                                        ↓
                                               可在 draw.io GUI 中继续编辑
```

## 适用场景

- **数据库 ER 图** — 实体关系建模、字段定义、主外键标注
- **实体关系图** — 业务数据模型可视化
- **UML 类图** — 类、属性、方法、继承关系
- **架构图** — 系统组件、服务依赖、接口定义
- **系统部署图** — 节点拓扑、模块部署
- **数据流图** — 数据流转、处理节点

## 核心特性

**零碰撞布局** — `EntityLayout` 引擎自动计算实体位置，Bounding Box 零重叠（内置 `validate()` 校验）

**障碍物感知路由** — 2/3/4 弯多策略正交路径规划，连接线自动绕开所有中间实体，不依赖 draw.io 的自动路由

**CJK 文字优化** — 针对中文/日文渲染特性调整高度公式（HEADER_H=28, ROW_H=20），实体框内文字完整可见不截断

**Visio 原生风格** — 浅灰画布(#EBEBEB)、浅蓝表头(#C2CFF2)、白底实体(#FFFFFF)、灰线连接(#999999)，还原 Visio 经典视觉

**导出前校验** — `validate()` 自动遍历所有实体对的 Bounding Box，发现重叠立即告警

**零外部依赖** — 仅需 Python 3.10+ 标准库 + draw.io Desktop（免费），无需 pip 安装任何包

**统一输出管理** — 所有 `*.drawio` 和 `*.png` 自动归入 `diagram/` 子文件夹

## 安装

### 前提条件

1. **draw.io Desktop**（免费）— [GitHub Releases 下载](https://github.com/jgraph/drawio-desktop/releases)
   - 安装后确认路径：`C:\Program Files\draw.io\draw.io`（Windows）
   - Linux/macOS 用户请调整 `DRAWIO` 变量中的路径
2. **Python 3.10+** — 仅需标准库，无需 pip 安装

### 下载

```bash
git clone https://github.com/getfunWindz/visio-style-diagram.git
cd visio-style-diagram
```

或直接复制 `examples/er_diagram.py` 到你的项目中开始使用。

## 快速开始

### 30 秒最短示例

```python
import os, subprocess, xml.sax.saxutils as xesc

OUT = 'diagram'   # 所有输出归入 diagram/ 目录
DRAWIO = r'C:\Program Files\draw.io\draw.io'

CID = [1]
def nid():
    CID[0] += 1; return str(CID[0])
def esc(s):
    return xesc.escape(str(s), {'"': '&quot;'})

HEADER_H = 28; ROW_H = 20; ENTITY_W = 190; ROW_GAP = 70

def calc_h(fields):
    return HEADER_H + len(fields) * ROW_H + 4

def column_y(heights, gap=ROW_GAP):
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
            b = '<b>' + esc(fn) + '</b>' if fn in pk else esc(fn)
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
        for my in [(to,), (bo,)]:
            p = [(ex, ey), (ex, my), (ro, my), (ro, ny), (nx, ny)]
            if self._path_ok(p, obs): return [(ex, my), (ro, my), (ro, ny)]
        return [(ro, ey), (ro, ny)]

    @staticmethod
    def _path_ok(pts, obs):
        for i in range(len(pts) - 1):
            for r in obs:
                if EntityLayout._line_hits(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], r):
                    return False
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
        d = os.path.join(OUT, subdir); os.makedirs(d, exist_ok=True)
        src = os.path.join(d, name + '.drawio')
        body = '\n'.join(self.cells)
        xml = ('<mxfile host="Electron" modified="2026-06-10T00:00:00.000Z" agent="Mozilla/5.0" version="30.0.4">'
               '<diagram id="d1" name="diagram">'
               '<mxGraphModel dx="0" dy="0" grid="0" page="1" pageWidth="2400" pageHeight="1800">'
               '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + body +
               '</root></mxGraphModel></diagram></mxfile>')
        with open(src, 'w', encoding='utf-8') as f: f.write(xml)
        dst = src.replace('.drawio', '.png')
        subprocess.run([DRAWIO, '--export', '--format', 'png', '--width', '1200', '--border', '16', '--output', dst, src],
                       capture_output=True, timeout=30)
        return dst

# ── 示例：垂直链 ──
ly = EntityLayout()
heights = [calc_h(['id(PK)', 'field1']), calc_h(['id(PK)', 'parent_id(FK)']), calc_h(['id(PK)', 'child_id(FK)'])]
ys = column_y(heights)
ids = [ly.add_entity(200, ys[i], n, f, {n.split('(')[0] + '(PK)'}) for i, (n, f) in enumerate([
    ('Parent', ['id(PK)', 'field1']),
    ('Child', ['id(PK)', 'parent_id(FK)']),
    ('GrandChild', ['id(PK)', 'child_id(FK)'])])]
for i in range(2):
    ly.add_connector(ids[i], ids[i+1], c1='1', c2='n', sx=0.5, sy=1, tx=0.5, ty=0)
ly.export('example', 'vertical-chain')
print('Done → diagram/example/vertical-chain.png')
```

运行后 `diagram/example/` 目录下生成 `vertical-chain.drawio`（可编辑）和 `vertical-chain.png`。

## 完整示例

### 1. 垂直链 — 顺序 1→1→n 关系

```
[Parent]   ← 实体1
    ↓ 1→n
[Child]    ← 实体2
    ↓ 1→n
[GrandChild] ← 实体3
```

用于：商品类目层级、组织架构、分类树。

### 2. 左到右扇出 — 两个源连接同一个目标

```
[SourceA] ──┐
             ├── [Target]
[SourceB] ──┘
```

用于：外键关联、审核流程（多个来源对应一个审核记录）。

### 3. 双车道 — 两路共享源和目标

```
上车道: [Customer] ──→ [Collect] ──→ [Goods]
下车道: [Customer] ──→ [Order]   ──→ [Goods]
```

用于：同一源有两条独立路径到达同一目标。

### 4. 列网格 — 多表全局 ER 图

```
Col 0            Col 1            Col 2            Col 3
[Admin]          [Artisan]        [Goods]          [Customer]
   ↓                 ↓                ↓                ↓
[Notice]         [Shop]           [GoodsImage]     [Collect]
                     ↓                                ↓
                [AuditRecord]                      [Order]
```

用于：10+ 表的大型 ER 图，行对齐自动计算。

## API 参考

### `EntityLayout` 类

#### 构造

```python
ly = EntityLayout()
```

#### `add_entity(x, y, name, fields, pk_set=None, w=190)`

添加一个实体框。

| 参数 | 类型 | 说明 |
|------|------|------|
| `x` | int | 左上角 X 坐标 |
| `y` | int | 左上角 Y 坐标 |
| `name` | str | 实体名称（显示在表头） |
| `fields` | list[str] | 字段列表 |
| `pk_set` | set[str] | 主键字段集合（这些字段会加粗） |
| `w` | int | 实体宽度（默认 190） |

**返回值**: 实体 ID（用于后续 `add_connector`）

---

#### `add_connector(src, dst, label='', c1='', c2='', sx=1, sy=0.5, tx=0, ty=0.5)`

在两个实体之间添加连接线。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `src` | str | — | 源实体 ID |
| `dst` | str | — | 目标实体 ID |
| `label` | str | `''` | 关系名称（居中显示在线上） |
| `c1` | str | `''` | 源端基数标注（如 `'1'`, `'n'`） |
| `c2` | str | `''` | 目标端基数标注 |
| `sx` | float | `1` | 源端出口 X (0=左, 0.5=中, 1=右) |
| `sy` | float | `0.5` | 源端出口 Y (0=上, 0.5=中, 1=下) |
| `tx` | float | `0` | 目标入口 X |
| `ty` | float | `0.5` | 目标入口 Y |

**端口位置参考：**

| sx, sy | 位置 | 适用场景 |
|--------|------|----------|
| `1, 0.5` | 右侧中间 | 左→右水平连接（默认） |
| `0.5, 1` | 底部中间 | 上→下垂直连接 |
| `0.5, 0` | 顶部中间 | 下→上垂直连接 |
| `0, 0.5` | 左侧中间 | 右→左反向连接 |
| `1, 0.5` | 右侧中间 → 右侧中间 | 绕行其他实体后回到同列 |

---

#### `export(subdir, name)`

生成 draw.io XML 并导出 PNG。

| 参数 | 类型 | 说明 |
|------|------|------|
| `subdir` | str | 子目录名（如 `'example'`） |
| `name` | str | 文件名（不含扩展名） |

输出: `diagram/<subdir>/<name>.drawio` + `diagram/<subdir>/<name>.png`

---

#### `validate()`

检查所有实体对的 Bounding Box 是否重叠。

**返回值**: `list[str]` — 空列表表示无重叠，非空列表包含重叠描述。

```python
issues = ly.validate()
if issues:
    for i in issues:
        print(i)  # e.g. OVERLAP: "Goods" <-> "Order" (10x5px)
```

### 辅助函数

#### `calc_h(fields)`

计算实体高度（CJK 优化）。

```python
h = calc_h(['id(PK)', 'name', 'description'])
# 返回: 28 + 3 * 20 + 4 = 92
```

#### `column_y(heights, gap=70)`

根据实体高度数组计算 Y 坐标。

```python
heights = [calc_h(f1), calc_h(f2), calc_h(f3)]
ys = column_y(heights, gap=50)
# 返回: [20, 20 + h1 + 50, 20 + h1 + 50 + h2 + 50]
```

### 常量

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `HEADER_H` | `28` | 表头高度（11px CJK 加粗 + padding） |
| `ROW_H` | `20` | 每行字段高度（9px CJK + padding + 边框） |
| `ENTITY_W` | `190` | 实体默认宽度 |
| `COL_GAP` | `60` | 列间距 |
| `ROW_GAP` | `70` | 行间距 |

## 视觉样式定制

### 修改颜色

```python
# 直接在 mxCell style 属性中修改
style = 'fillColor=#FFFFFF;strokeColor=#DCDCDC;'  # 白底灰边框
# 表头颜色在 html 中: background-color:#C2CFF2
# 连接线: strokeColor=#999999
```

### 修改字体

```python
# 表头: font-size=11px;font-weight=bold
# 字段: font-size=9px
# 关系标签: font-size=10px;fontStyle=2 (italic)
```

### 添加阴影/圆角（不推荐）

```python
# 如果确实需要：在 style 中添加 gradient=1;rounded=1;
# 注意这会偏离 Visio 原生风格
```

## 避坑指南

### PNG 导出空白

**原因**: HTML value 属性中的双引号未转义，导致 XML 解析失败。

**解决**: 确保所有 `"` 字符替换为 `&quot;`，使用 `esc()` 函数：

```python
def esc(s):
    return xesc.escape(str(s), {'"': '&quot;'})
```

### 实体框重叠

**原因**: 固定间距（如 GY=150）不适应不同实体高度的变化。9 字段实体高 204px，3 字段实体仅 94px，高度差异导致间距不足。

**解决**: 使用 `calc_h()` + `column_y()` 根据实际高度计算位置，而非硬编码间距。

### 文字被截断

**原因**: draw.io 渲染 CJK 文字比同 pt 数的拉丁文字高约 15%。

**解决**: 使用 CJK 优化常量 `HEADER_H=28, ROW_H=20`，不要用英文场景的 `HEADER_H=24, ROW_H=16`。

### 连接线穿过实体

**原因**: draw.io 的 orthogonal router 不知道其他实体位置，只考虑源和目标。

**解决**: 引擎内置障碍物感知路由，2-bend → 3-bend → 4-bend 逐级尝试。确保 `add_connector` 在实体全部注册完成后调用。

### 列布局不对齐

**原因**: 碰撞检测后自动右移（`_find_clear` 右移策略）会破坏同一列的 X 坐标一致性。

**解决**: 用 `column_y()` 预计算行 Y 位置，保证零重叠同时维持对齐。参考 `examples/er_diagram.py` 中的 `diagram_43_global()`。

## 项目结构

```
visio-style-diagram/
├── README.md                 # 本文档
├── SKILL.md                  # opencode Skill 定义文件
├── examples/
│   └── er_diagram.py         # 完整 ER 图生成脚本
└── .gitignore
```

运行 `examples/er_diagram.py` 后：

```
diagram/
├── 41-entity-attribute/
│   ├── entity-attribute.drawio
│   └── entity-attribute.png
├── 42-partial-er/
│   ├── 42-1-merchant-review.drawio
│   ├── 42-1-merchant-review.png
│   ├── 42-2-product-listing.drawio
│   ├── 42-2-product-listing.png
│   ├── 42-3-user-order.drawio
│   └── 42-3-user-order.png
├── 43-global-er/
│   ├── global-er.drawio
│   └── global-er.png
└── example/
    ├── vertical-chain.drawio
    └── vertical-chain.png
```

## 高级技巧

### 在 draw.io GUI 中继续编辑

生成的 `.drawio` 文件可直接在 draw.io Desktop 中打开：

1. 打开 draw.io Desktop
2. 选择 "Open Existing Diagram" → 选择 `.drawio` 文件
3. 自由拖拽、增删元素
4. File → Export As → PNG 重新导出保持同样的样式

### 批量生成多个图

```python
diagrams = [
    ('er-module-a', diagram_a),
    ('er-module-b', diagram_b),
    ('global-er', diagram_global),
]
for name, fn in diagrams:
    print(f'Generating {name}...')
    fn()
```

### 自定义实体宽度

```python
ly.add_entity(x, y, 'LongNameEntity', fields, w=250)  # 宽实体
```

## 与同类工具对比

| 特性 | 本项目 | draw.io UI 手动画 | PlantUML | dbdiagram.io |
|------|--------|-------------------|----------|--------------|
| 编程生成 | ✅ Python | ❌ 手动拖拽 | ✅ DSL | ❌ Web UI |
| Visio 风格 | ✅ 原生 | 需手动调 | ❌ 默认不同 | ❌ 默认不同 |
| 碰撞检测 | ✅ 内置 | ❌ 手动检查 | ❌ N/A | ❌ 手动检查 |
| 障碍路由 | ✅ 自动 | ✅ 手动调线 | ❌ 可能交叉 | ❌ 可能交叉 |
| CJK 优化 | ✅ | ✅ | ⚠️ 需配置 | ✅ |
| 可编辑输出 | ✅ .drawio | ✅ .drawio | ❌ .png 不可编辑 | ❌ 导出图片 |
| 外部依赖 | ❌ 无 | draw.io | Graphviz | 无 |

## 许可证

MIT

---

**Visio-Style Diagram Generator** — 用代码画 Visio 风格图，零碰撞、免调试、可编辑。
