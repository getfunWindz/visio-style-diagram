---
name: visio-style-diagram
description: |
  Generate Visio-style software engineering diagrams via draw.io Desktop.
  Use when user asks for: Visio风格图 / 数据库ER图 / 实体关系图 / 类图 / 架构图 /
  draw.io图 / 软件工程图 / 数据库设计图 / 系统部署图 / 数据流图 / DFD /
  程序流程图 / N-S盒图 / Nassi-Shneiderman / 盒图 / UML图 / UML用例图 /
  UML状态图 / UML时序图 / 用例图 / 状态图 / 时序图 / 活动图 / 泳道图 /
  跨职能流程图 / 软件工程图规范.
  Requires draw.io Desktop installed at C:\Program Files\draw.io\draw.io.
---

# Visio-Style Diagram Generator

Generate Visio-style software engineering diagrams via **draw.io Desktop**.
Outputs `.drawio` (editable XML) + `.png` (max 1200px wide).

**Skill files:**
- `SKILL.md` — this file (skill instruction)
- `README.md` — full Chinese documentation with API reference
- `examples/er_diagram.py` — complete runnable ER diagram generating script (5 diagrams)

**All generated files go into a `diagram/` subfolder** for centralized management.

## 软件工程规范约束 (Software Engineering Standards)

生成的图必须遵守以下软件工程各阶段的图规范。这些规范源自软件工程标准教材，定义了每种图的元素符号、连接规则和语义约束。

### 1. 数据流图 (DFD) 规范

| 元素 | 符号 | 含义 | 约束 |
|------|------|------|------|
| **外部实体 (External Entity)** | 矩形（正方形/长方形） | 系统外的人、组织、系统（数据的源点/终点） | 必须位于图的边缘；同一实体可重复出现（加斜线标记） |
| **加工 (Process)** | 圆角矩形 或 圆形/椭圆 | 对数据的处理/变换 | 必须有编号（如 1, 1.1, 2.3）；必须有输入数据流和输出数据流 |
| **数据流 (Data Flow)** | 带箭头直线 | 数据的流动方向 | 必须有名称；箭头指向数据流动方向；不能直接从外部实体到外部实体 |
| **数据存储 (Data Store)** | 双横线 / 开口矩形 | 数据的存储 | 必须有名称；必须通过数据流与加工连接 |

**DFD 分层原则**:
- 顶层图（上下文图）：1个加工代表整个系统
- 0层图：将顶层加工分解为若干子加工
- 子图：继续分解，每个加工编号保持父子关系（如 2.1, 2.2）

### 2. N-S盒图 (Nassi-Shneiderman) 规范

| 结构 | 表示 | 约束 |
|------|------|------|
| **顺序** | 从上到下排列的矩形块 | 每个框一个语句 |
| **选择 (IF-THEN-ELSE)** | 上部条件 + 左下THEN块 + 右下ELSE块 | 条件用横线分隔，真假分支用三角分隔 |
| **多分支 (CASE)** | 条件 + N个分支列 | 每个条件值一个执行列 |
| **循环 (WHILE-DO)** | 顶部条件 + 循环体框 | 条件为真时重复执行 |
| **循环 (DO-UNTIL)** | 循环体框 + 底部条件 | 条件为假时继续重复 |

### 3. 程序流程图 / 系统流程图 规范

| 符号 | 名称 | 用途 |
|------|------|------|
| 圆角矩形 | 起止框 (Start/End) | 程序的开始和结束 |
| 矩形 | 处理框 (Process) | 一般处理操作 |
| 菱形 | 判断框 (Decision) | 条件判断，一个入口两个以上出口 |
| 平行四边形 | 数据框 (Data I/O) | 数据输入/输出 |
| 箭头 | 流线 (Flow Line) | 控制流方向 |

**结构化程序设计约束**: 一个入口、一个出口、无死循环、无死语句。

### 4. UML用例图 规范

| 元素 | 符号 | 含义 |
|------|------|------|
| **参与者 (Actor)** | 火柴人形 | 与系统交互的角色（人或外部系统） |
| **用例 (Use Case)** | 椭圆 | 系统提供的功能单元 |
| **系统边界 (System Boundary)** | 矩形框，内含系统名 | 系统范围 |
| **关联** | 实线 | 参与者与用例的关系 |
| **泛化** | 空心三角箭头实线 | 参与者/用例的继承关系 |
| **包含 <<include>>** | 虚线箭头，指向被包含用例 | 一个用例必然包含另一个用例的行为 |
| **扩展 <<extend>>** | 虚线箭头，指向被扩展用例 | 一个用例可选的扩展行为 |

### 5. UML状态图 规范

| 元素 | 符号 | 含义 |
|------|------|------|
| **初始状态** | 实心圆 | 状态机的起点 |
| **最终状态** | 圆圈内嵌实心圆点（牛眼） | 状态机的终点 |
| **状态 (State)** | 圆角矩形 | 对象在生命周期内的一个状态 |
| **转换 (Transition)** | 箭头，标注 [监护条件] | 事件触发下的状态变化 |
| **选择 (Choice)** | 菱形，分支上用 [guard] | 条件分支 |

### 6. UML时序图 规范

| 元素 | 符号 | 含义 |
|------|------|------|
| **角色/对象** | 火柴人(角色) / 矩形(对象) | 交互的参与方 |
| **生命线 (Lifeline)** | 垂直虚线 | 对象在时间轴上的存在 |
| **控制焦点 (Activation)** | 窄矩形在生命线上 | 对象执行操作的时间段 |
| **同步消息** | 实线 + 实心箭头 | 发送者等待返回后继续 |
| **异步消息** | 实线 + 开放箭头 | 发送者不等待继续执行 |
| **返回消息** | 虚线 + 开放箭头 | 从调用返回 |
| **自关联消息** | 半闭合矩形 + 箭头 | 对象内部方法调用自身 |

### 7. E-R图 规范

| 元素 | 符号 | 含义 |
|------|------|------|
| **实体 (Entity)** | 矩形，框内写实体名 | 现实世界中的独立对象 |
| **属性 (Attribute)** | 椭圆，连到实体 | 描述实体的特征 |
| **关系 (Relationship)** | 菱形，连到实体 | 实体间的联系（1:1 / 1:N / M:N） |
| **主键 (Primary Key)** | 实体名下划线/加粗属性 | 唯一标识实体的属性 |

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

## 数据流图 (Data Flow Diagram / DFD)

实现软件工程规范中的DFD，支持外部实体、加工、数据存储、数据流四种基本元素。

### DFD 元素符号规范

| 元素 | draw.io 形状 | 颜色 |
|------|-------------|------|
| 外部实体 (External Entity) | 圆角矩形，内部标签 | 填充 #FFF3CD，边框 #DCDCDC |
| 加工 (Process) | 圆形 / 椭圆，中央编号+名称 | 填充 #FFFFFF，边框 #999999 |
| 数据存储 (Data Store) | 开口矩形 / 双横线 | 填充 #F5F5F5，边框 #DCDCDC |
| 数据流 (Data Flow) | 带标签箭头 | 线色 #666666，字号 9px |

### API

#### `add_dfd_external(x, y, w, h, name)`

添加外部实体（数据源点/终点）。矩形形状，位于图边缘。

```python
eid = ly.add_dfd_external(30, 200, 120, 40, '用户')
```

#### `add_dfd_process(x, y, size, name, pid)`

添加加工（数据处理）。圆形/椭圆，内部显示编号+名称。

| Param | Description |
|-------|-------------|
| `pid` | 加工编号，如 `'1'`, `'1.1'`, `'2.3'` |

```python
pid = ly.add_dfd_process(200, 200, 80, '验证登录', '1')
```

#### `add_dfd_store(x, y, w, h, name)`

添加数据存储。开口矩形形状。

```python
sid = ly.add_dfd_store(350, 200, 120, 50, '用户表')
```

#### `add_dfd_flow(src, dst, label, sx=1, sy=0.5, tx=0, ty=0.5)`

添加数据流（带箭头直线）。

```python
ly.add_dfd_flow(eid, pid, '登录请求', sx=1, sy=0.5, tx=0, ty=0.5)
ly.add_dfd_flow(pid, sid, '写入用户信息', sx=1, sy=0.5, tx=0, ty=0.5)
```

## 程序流程图 / 系统流程图

实现软件工程规范中的程序流程图基本符号。

### 流程图标准符号

| 方法 | 形状 | 说明 |
|------|------|------|
| `add_flow_start_end(x, y, w, h, label)` | 圆角矩形 | 开始/结束 |
| `add_flow_process(x, y, w, h, label)` | 矩形 | 处理操作 |
| `add_flow_decision(x, y, size, label)` | 菱形 | 条件判断 |
| `add_flow_data(x, y, w, h, label)` | 平行四边形 | 数据输入/输出 |
| `add_flow_arrow(src, dst, label='')` | 实线箭头 | 控制流 |

### 结构化编程约束

流程图必须遵循：一个入口、一个出口、无死循环、无死语句。

```python
start = ly.add_flow_start_end(200, 20, 120, 40, '开始')
input_step = ly.add_flow_data(200, 90, 140, 40, '输入n')
proc = ly.add_flow_process(200, 160, 120, 40, 'sum=0,i=1')
dec = ly.add_flow_decision(200, 240, 80, 'i<=n?')
proc2 = ly.add_flow_process(130, 320, 120, 40, 'sum+=i,i++')

ly.add_flow_arrow(start, input_step)
ly.add_flow_arrow(input_step, proc)
ly.add_flow_arrow(proc, dec)
ly.add_flow_arrow(dec, proc2, label='是', sx=0.5, sy=1, tx=1, ty=0)
# sy=1 → bottom, target tx=1 ty=0.5 → right side of proc2
```

## N-S盒图 (Nassi-Shneiderman Box Diagram)

实现结构化程序设计中的N-S盒图。所有控制结构在一个大框内，用嵌套矩形表示。

| 方法 | 结构 | 说明 |
|------|------|------|
| `add_ns_box(x, y, w, h)` | 外框 | 程序的大框 |
| `add_ns_sequence(x, y, w, h, label)` | 顺序框 | 从上到下执行 |
| `add_ns_ifelse(x, y, w, h, condition, then_label, else_label)` | IF-THEN-ELSE | 选择结构 |
| `add_ns_while(x, y, w, h, condition, body)` | WHILE-DO | 当型循环 |
| `add_ns_until(x, y, w, h, condition, body)` | DO-UNTIL | 直到型循环 |

### API

#### `add_ns_box(x, y, w, h)`

外框容器，程序范围。

```python
ly.add_ns_box(50, 50, 400, 300)
```

#### `add_ns_ifelse(x, y, w, h, condition, then_label, else_label)`

IF-THEN-ELSE 结构。条件用三角区域分隔，左上为真分支，右下为假分支。

```python
ly.add_ns_ifelse(60, 60, 380, 80, 'x>0?', 'then: positive', 'else: negative')
```

#### `add_ns_while(x, y, w, h, condition, body)`

WHILE-DO 循环结构。条件在顶部，循环体在下方。

```python
ly.add_ns_while(60, 160, 380, 120, 'i<=n?', 'sum+=i; i++')
```

#### `add_ns_until(x, y, w, h, condition, body)`

DO-UNTIL 循环结构。循环体在上方，条件在底部。

```python
ly.add_ns_until(60, 300, 380, 100, 'i>n?', 'sum+=i; i++')
```

## UML用例图 (Use Case Diagram)

实现UML用例图规范。支持参与者和用例之间的4种关系。

### 用例图元素符号

| 元素 | 形状 | 说明 |
|------|------|------|
| Actor | 火柴人形（圆形头+三角形身） | `add_uml_actor()` |
| Use Case | 椭圆 | `add_uml_use_case()` |
| System Boundary | 矩形框 | `add_uml_system_boundary()` |
| 关联 | 实线 | `add_uml_assoc()` |
| 泛化 | 空心三角实线 | `add_uml_generalize()` |
| 包含 <<include>> | 虚线箭头 + `<<include>>` 标签 | `add_uml_include()` |
| 扩展 <<extend>> | 虚线箭头 + `<<extend>>` 标签 | `add_uml_extend()` |

### API

#### `add_uml_actor(x, y, size, name)`

火柴人形参与者。圆头（圆形） + 身体+双腿（三角形线框）。

```python
actor = ly.add_uml_actor(50, 200, 40, '用户')
```

#### `add_uml_use_case(x, y, w, h, name)`

椭圆形状的用例。

```python
uc1 = ly.add_uml_use_case(180, 180, 120, 50, '登录')
uc2 = ly.add_uml_use_case(180, 260, 120, 50, '注册')
```

#### `add_uml_system_boundary(x, y, w, h, name)`

系统边界矩形框，框内顶部显示系统名。

```python
sb = ly.add_uml_system_boundary(150, 100, 300, 300, '在线商城系统')
```

#### 关系API

```python
# 关联 (Association) — 实线
ly.add_uml_assoc(actor, uc1)

# 泛化 (Generalization) — 实线 + 空心三角
ly.add_uml_generalize(uc_child, uc_parent)

# 包含 (Include) — 虚线 + <<include>>
ly.add_uml_include(uc1, uc2)

# 扩展 (Extend) — 虚线 + <<extend>>
ly.add_uml_extend(uc_base, uc_extension)
```

## UML状态图 (State Machine Diagram)

按照UML规范支持状态机元素。

### 元素

| 元素 | 方法 | 说明 |
|------|------|------|
| 初始状态 | `add_uml_initial_node()` | 实心圆 |
| 状态 | `add_uml_state()` | 圆角矩形，分上中下三区 |
| 转换 | `add_uml_transition()` | 箭头 + 事件/监护条件标签 |
| 选择 | `add_uml_choice()` | 菱形，条件分支 |
| 最终状态 | `add_uml_final_node()` | 牛眼 |

### API

#### `add_uml_state(x, y, w, h, name)`

圆角矩形状态框。内部显示状态名。

```python
s1 = ly.add_uml_state(180, 80, 160, 50, '待审核')
s2 = ly.add_uml_state(180, 200, 160, 50, '已通过')
```

#### `add_uml_transition(src, dst, label, guard='', ...)`

带事件名和监护条件 `[guard]` 的转换箭头。

```python
ly.add_uml_transition(s1, s2, '审核通过', guard='金额<10000')
# 箭头上显示: 审核通过 [金额<10000]
```

#### `add_uml_choice(x, y, size)`

选择/分支菱形。

```python
ch = ly.add_uml_choice(260, 150, 60)
ly.add_uml_transition(s1, ch, '', guard='')
ly.add_uml_transition(ch, s2, '', guard='[通过]')
ly.add_uml_transition(ch, s3, '', guard='[驳回]')
```

## UML时序图 (Sequence Diagram)

按照UML时序图规范实现交互图元素。

### 元素符号

| 元素 | 方法 | 形状 |
|------|------|------|
| 角色 | `add_seq_actor()` | 火柴人 |
| 对象 | `add_seq_object()` | 矩形，标注 `object:Class` |
| 生命线 | `add_seq_lifeline()` | 垂直虚线 |
| 激活条 | `add_seq_activation()` | 窄矩形 |
| 同步消息 | `add_seq_sync()` | 实线+实心箭头 |
| 异步消息 | `add_seq_async()` | 实线+开放箭头 |
| 返回消息 | `add_seq_return()` | 虚线+开放箭头 |
| 自调用 | `add_seq_self()` | 半闭合矩形+箭头 |

### API

#### `add_seq_actor(x, y, size, name)`

生命线顶部的火柴人角色。下方自动延伸虚线生命线。

```python
user = ly.add_seq_actor(80, 30, 30, '用户')
```

#### `add_seq_object(x, y, w, h, name, class_name='')`

生命线顶部的对象矩形。`name` 和 `class_name` 组合为 `name:ClassName` 的标注形式。

```python
svr = ly.add_seq_object(250, 30, 140, 40, 'loginService', 'LoginService')
db = ly.add_seq_object(450, 30, 120, 40, '', 'Database')
```

#### `add_seq_lifeline(x, y_top, y_bottom)`

垂直虚线生命线。

```python
ly.add_seq_lifeline(80, 70, 500)  # 从 y=70 到 y=500
```

#### `add_seq_activation(x, y, w, h)`

生命线上的窄矩形激活条（控制焦点）。

```python
ly.add_seq_activation(250, 120, 14, 120)  # 在x=250处，从y=120到y=240
```

#### 消息API

```python
# 同步消息 — 实线实心箭头
ly.add_seq_sync(src_x, src_y, dst_x, dst_y, label)
# 异步消息 — 实线开放箭头
ly.add_seq_async(src_x, src_y, dst_x, dst_y, label)
# 返回消息 — 虚线开放箭头
ly.add_seq_return(src_x, src_y, dst_x, dst_y, label)
# 自关联消息
ly.add_seq_self(obj_x, obj_y, label)
```

## UML活动图 (Activity Diagram) & 泳道图 (Swimlane)

Per the OMG UML 2.5 specification, activity diagrams use these shape conventions:

| Element | Notation | draw.io shape |
|---------|----------|---------------|
| **Initial Node** | Solid filled circle | `add_uml_initial_node()` |
| **Final Node** | Solid circle inside hollow outer circle (bullseye) | `add_uml_final_node()` |
| **Action** | Rounded rectangle | `add_custom_box(..., style_extra='rounded=1;arcSize=8;')` |
| **Decision / Merge** | Diamond | Diamond shape or text label with branching connectors |
| **Control Flow** | Solid line arrow | `add_connector()` with default arrow |
| **Partition (Swimlane)** | Vertical or horizontal container | `add_swimlane(horizontal=False)` for vertical lanes |

### `add_uml_initial_node(x, y, size=16, parent='1', parent_x=0, parent_y=0)`

UML Initial Node — solid black filled circle. Place at the start of the activity flow, inside a swimlane.

| Param | Description |
|-------|-------------|
| `parent` | Swimlane ID to contain this node |
| `parent_x`, `parent_y` | Absolute position of parent (for coordinate conversion) |

```python
start = ly.add_uml_initial_node(merchant_x + pool_w//2 - 8, merchant_y + head_h + 20, 16,
                                 parent=lane_id, parent_x=merchant_x, parent_y=merchant_y)
```

### `add_uml_final_node(x, y, size=22, parent='1', parent_x=0, parent_y=0)`

UML Final Node — solid black circle with thick outer ring (bullseye). Place at the end of the flow, optionally inside a swimlane.

| Param | Description |
|-------|-------------|
| `parent` | Swimlane ID if inside a lane |
| `parent_x`, `parent_y` | Absolute position of parent lane (for coordinate conversion) |

```python
final = ly.add_uml_final_node(abs_x, abs_y, 22, parent=lane_id,
                               parent_x=lane_x, parent_y=lane_y)
```

## Swimlane (Cross-Functional Flowchart / UML Partition)

Swimlanes group activities by responsible role, like Visio's cross-functional flowchart or UML 2.5 activity partitions.

The draw.io swimlane shape supports two orientations:
- **Horizontal** (`horizontal=True`, default): uses `swimlane` draw.io shape, header on the left, content to the right, lanes stack vertically
- **Vertical** (`horizontal=False`): renders as two rounded rectangles (pool body + header bar at top). Tall pool (height > width) with role label in the header, lanes sit side by side. This corresponds to BPMN vertical pools or UML activity partitions.

### Visual Layout (Vertical Pools)

```
┌──────────────────┬──────────────────┬──────────────────┐
│  商家 (Merchant) │ 管理员 (Admin)   │   系统 (System)  │
│  ┌───────┐      │                  │                  │
│  │  ●    │      │                  │                  │  ← UML Initial
│  ├───────┤      │                  │                  │
│  │提交申请│──────│→ ┌───────┐      │                  │
│  └───────┘      │  │审核申请│      │                  │
│                 │  ├───────┤      │                  │
│                 │  │审核通过│      │                  │
│                 │  │  ？   │      │                  │
│                 │  └─┬──┬──┘      │                  │
│                 │    │  │         │                  │
│                 │ 通过│  │驳回    │                  │
│                 │    │  └─────────│→┌───────┐       │
│                 │    │            │ │驳回申请│       │
│                 │    │            │ ├───────┤       │
│                 │    └────────────│→│自动执行│       │
│                 │                 │ ├───────┤       │
│                 │                 │ │流程结束│       │
│                 │                 │ ├───────┤       │
│                 │                 │ │   ◎   │       │  ← UML Final
│                 │                 │ └───────┘       │
└──────────────────┴──────────────────┴──────────────────┘
```

### EntityLayout API for Swimlanes

### Visual Layout

```
┌─────────────────────────────────────────────────────────┐
│ 商家 (Merchant)                                          │  ← swimlane, colored header band
│  ┌──────────────┐                                        │
│  │  提交申请     │   ← borderless text label in lane     │
│  └─────┬────────┘                                        │
│        │ (arrow crosses lane boundary)                   │
├────────┼────────────────────────────────────────────────┤
│ 管理员 (Admin)                                           │  ← different lane
│  ┌──────┴──────────┐  ┌──────────────┐                  │
│  │  审核申请        │→│  审核通过？   │                  │
│  └─────────────────┘  └──────┬───────┘                  │
│                              │                           │
├──────────────────────────────┼──────────────────────────┤
│ 系统 (System)                                          │
│                  ┌───────────┴───────────┐              │
│                  │  自动执行业务 / 驳回   │              │
│                  └───────────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

### EntityLayout API for Swimlanes

#### `add_swimlane(x, y, w, h, label, color='#E8F0FE', header_size=50, horizontal=True)`

Creates a swimlane container (UML 2.5 partition / BPMN pool).

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `x`, `y` | int | — | Absolute top-left position |
| `w`, `h` | int | — | Width and height of the swimlane |
| `label` | str | — | Role name displayed in header |
| `color` | str | `'#E8F0FE'` | Fill color (e.g., `'#FFF3CD'` for yellow) |
| `header_size` | int | `50` | Width (horizontal) or height (vertical) of the header band |
| `horizontal` | bool | `True` | `True` = band (header left); `False` = vertical pool (header top, lanes side-by-side) |

**Returns**: entity ID

- Use `horizontal=True` for standard swimlane diagrams (lanes stacked top-to-bottom).
- Use `horizontal=False` for UML activity diagram partitions / BPMN vertical pools (lanes placed left-to-right, each taller than wide).

**Returns**: entity ID (for connectors and labels)

```python
# Three horizontal swimlanes stack vertically (horizontal=True, default)
lane_w = 900; lane_h = 110; gap = 8
merchant = ly.add_swimlane(30, 30, lane_w, lane_h, '商家 (Merchant)', color='#FFF3CD')
admin    = ly.add_swimlane(30, 30+lane_h+gap, lane_w, lane_h, '管理员 (Admin)', color='#E8F0FE')
system   = ly.add_swimlane(30, 30+2*(lane_h+gap), lane_w, lane_h, '系统 (System)', color='#D4EDDA')

# Three vertical pools side by side (horizontal=False)
x0 = 40; lane_w = 240; lane_h = 520; gap = 20
merchant = ly.add_swimlane(x0, 80, lane_w, lane_h, '商家 (Merchant)',
                            color='#FFF3CD', header_size=50, horizontal=False)
admin    = ly.add_swimlane(x0+lane_w+gap, 80, lane_w, lane_h, '管理员 (Admin)',
                            color='#E8F0FE', header_size=50, horizontal=False)
system   = ly.add_swimlane(x0+2*(lane_w+gap), 80, lane_w, lane_h, '系统 (System)',
                            color='#D4EDDA', header_size=50, horizontal=False)
```

#### `add_label_in_lane(lane_id, lane_x, lane_y, x_rel, y_rel, w, h, text, font_size=11, bold=False, color='#333333')`

Adds a **borderless text label** inside a swimlane. The label has no visible rectangle outline; its visual boundary is the parent swimlane's container.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `lane_id` | str | — | Entity ID of the swimlane from `add_swimlane()` |
| `lane_x`, `lane_y` | int | — | Absolute position of the swimlane (for auto-computing absolute position) |
| `x_rel`, `y_rel` | int | — | Position RELATIVE to the swimlane's top-left |
| `w`, `h` | int | — | Size of the text label's clickable area |
| `text` | str | — | Display text |
| `font_size` | int | `11` | Font size in px |
| `bold` | bool | `False` | Bold text |
| `color` | str | `'#333333'` | Text color |

**Important**: Labels inside swimlanes are **borderless** — they have no `strokeColor` or `fillColor`. Their visual "frame" is the swimlane container itself. The EntityLayout still tracks their absolute bounding box for obstacle-aware connector routing.

Labels are **automatically clamped** to stay within the pool's content area (below the header, above the bottom, and within horizontal padding). This ensures all entities remain inside their parent swimlane.

Use the `parent` parameter on `add_uml_initial_node()` and `add_uml_final_node()` to keep start/end circles inside a pool, with `parent_x/parent_y` being the pool's absolute position for coordinate conversion.

```python
m1 = ly.add_label_in_lane(merchant, 30, 30, 80, 35, 140, 36,
                           '提交申请', bold=True, color='#8B6914')
a1 = ly.add_label_in_lane(admin, 30, 148, 320, 35, 140, 36,
                           '审核申请', bold=True, color='#1A5C8A')
```

#### Connectors Between Swimlanes

Connectors between labels in different swimlanes work exactly like normal connectors. The routing algorithm treats the lane containers as obstacles (if needed) and routes around them.

```python
# Cross-lane connector (merchant → admin)
ly.add_connector(m1, a1, label='提交', sx=1, sy=0.5, tx=0, ty=0.5)
# Within-lane connector (admin → admin)
ly.add_connector(a1, a2, label='审核完成', sx=1, sy=0.5, tx=0, ty=0.5)
```

### UML Activity Diagram Example (Vertical Swimlanes)

```python
def activity_diagram_example():
    """UML activity diagram with 3 vertical pools and initial/final nodes."""
    ly = EntityLayout()
    x0, lane_w, lane_h, gap = 40, 240, 520, 20
    head_h = 50

    # Three vertical lanes side by side
    merchant = ly.add_swimlane(x0, 80, lane_w, lane_h, '商家 (Merchant)',
                                color='#FFF3CD', header_size=head_h, horizontal=False)
    admin = ly.add_swimlane(x0+lane_w+gap, 80, lane_w, lane_h, '管理员 (Admin)',
                             color='#E8F0FE', header_size=head_h, horizontal=False)
    system = ly.add_swimlane(x0+2*(lane_w+gap), 80, lane_w, lane_h, '系统 (System)',
                              color='#D4EDDA', header_size=head_h, horizontal=False)

    # UML Initial Node (solid circle) — above merchant lane
    init = ly.add_uml_initial_node(x0 + lane_w//2 - 9, 80 - 36, 18)

    # Borderless activity labels inside each lane
    m1 = ly.add_label_in_lane(merchant, x0, 80, 60, 80, 140, 36,
                               '提交申请', bold=True, color='#8B6914')
    a1 = ly.add_label_in_lane(admin, x0+lane_w+gap, 80, 60, 80, 140, 36,
                               '审核申请', bold=True, color='#1A5C8A')
    a2 = ly.add_label_in_lane(admin, x0+lane_w+gap, 80, 60, 180, 140, 36,
                               '审核通过？', bold=True, color='#8B6914')
    s1 = ly.add_label_in_lane(system, x0+2*(lane_w+gap), 80, 60, 80, 140, 36,
                               '自动执行业务', bold=True, color='#1A6B1A')
    s2 = ly.add_label_in_lane(system, x0+2*(lane_w+gap), 80, 60, 380, 80, 36,
                               '流程结束', bold=False, color='#666666')

    # UML Final Node (bullseye) — inside system lane bottom
    sys_x = x0 + 2*(lane_w+gap)
    final = ly.add_uml_final_node(sys_x + lane_w//2 - 11, 80 + lane_h - 30,
                                   22, parent=system, parent_x=sys_x, parent_y=80)
    # Connectors
    ly.add_connector(init, m1, sx=0.5, sy=1, tx=0.5, ty=0)
    ly.add_connector(m1, a1, label='提交', sx=1, sy=0.5, tx=0, ty=0.5)
    ly.add_connector(a1, a2, label='审核完成', sx=0.5, sy=1, tx=0.5, ty=0)
    ly.add_connector(a2, s1, label='通过', sx=1, sy=1, tx=0.5, ty=0)
    ly.add_connector(s1, s2, label='执行完成', sx=0.5, sy=1, tx=0.5, ty=0)
    ly.add_connector(s2, final, sx=0.5, sy=1, tx=0.5, ty=0)
    ly.export('uml-activity', 'review-activity')
```

### Validation Note

The `validate()` method will skip parent-child overlaps (labels inside swimlanes, final nodes inside lanes) automatically. These are expected and harmless.

## Example Implementation

Below is the complete **EntityLayout engine** template including all diagram type APIs. Copy and adapt for each project.

```python
"""draw.io Visio-style diagram — EntityLayout engine (collision-free, SE standards)."""
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

    # ── DFD (数据流图) ─────────────────────────────────

    def add_dfd_external(self, x, y, w, h, name):
        """外部实体 — 圆角矩形，浅黄填充"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(name) + '" '
            'style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;'
            'fillColor=#FFF3CD;strokeColor=#DCDCDC;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_dfd_process(self, x, y, size, name, pid):
        """加工 — 圆形/椭圆，编号+名称"""
        eid = nid()
        label = pid + '\\n' + name
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" '
            'style="ellipse;whiteSpace=wrap;html=1;'
            'fillColor=#FFFFFF;strokeColor=#999999;fontSize=9;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(size) + '" height="' + str(size) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, size, size)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_dfd_store(self, x, y, w, h, name):
        """数据存储 — 开口矩形（双侧竖线）"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(name) + '" '
            'style="shape=partialRectangle;whiteSpace=wrap;html=1;'
            'fillColor=#F5F5F5;strokeColor=#DCDCDC;fontSize=9;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_dfd_flow(self, src, dst, label='',
                     sx=1, sy=0.5, tx=0, ty=0.5):
        """数据流箭头"""
        return self.add_connector(src, dst, label=label,
                                  sx=sx, sy=sy, tx=tx, ty=ty)

    # ── 程序流程图 ─────────────────────────────────────

    def add_flow_start_end(self, x, y, w, h, label):
        """开始/结束 — 圆角矩形"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" '
            'style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;'
            'fillColor=#FFFFFF;strokeColor=#333333;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, label, rect))
        self._map[eid] = rect
        return eid

    def add_flow_process(self, x, y, w, h, label):
        """处理框 — 矩形"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" '
            'style="whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=#FFFFFF;strokeColor=#333333;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, label, rect))
        self._map[eid] = rect
        return eid

    def add_flow_decision(self, x, y, size, label):
        """判断框 — 菱形"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" '
            'style="rhombus;whiteSpace=wrap;html=1;'
            'fillColor=#FFFFFF;strokeColor=#333333;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(size) + '" height="' + str(size) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, size, size)
        self.entities.append((eid, label, rect))
        self._map[eid] = rect
        return eid

    def add_flow_data(self, x, y, w, h, label):
        """数据框 — 平行四边形"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" '
            'style="shape=parallelogram;whiteSpace=wrap;html=1;'
            'fillColor=#FFFFFF;strokeColor=#333333;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, label, rect))
        self._map[eid] = rect
        return eid

    def add_flow_arrow(self, src, dst, label='',
                       sx=0.5, sy=1, tx=0.5, ty=0):
        """控制流箭头"""
        return self.add_connector(src, dst, label=label,
                                  sx=sx, sy=sy, tx=tx, ty=ty)

    # ── N-S盒图 ────────────────────────────────────────

    def add_ns_box(self, x, y, w, h):
        """N-S外框容器"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="" '
            'style="whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=none;strokeColor=#333333;strokeWidth=2;" '
            'vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, 'ns_box', rect))
        self._map[eid] = rect
        return eid

    def add_ns_ifelse(self, x, y, w, h, condition, then_label, else_label):
        """IF-THEN-ELSE 选择结构"""
        eid = nid()
        html = (
            '<table><tr><td style="text-align:center;font-size:10px;'
            'border-bottom:1px solid #333333;padding:2px;" colspan="2">'
            + esc(condition) + '</td></tr>'
            '<tr><td style="width:50%;text-align:center;font-size:9px;'
            'border-right:1px solid #333333;padding:4px;">'
            + esc(then_label) + '</td>'
            '<td style="width:50%;text-align:center;font-size:9px;'
            'padding:4px;">' + esc(else_label) + '</td></tr></table>'
        )
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(html) + '" '
            'style="whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=none;strokeColor=#333333;fontSize=10;" '
            'vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, 'ns_ifelse', rect))
        self._map[eid] = rect
        return eid

    def add_ns_while(self, x, y, w, h, condition, body):
        """WHILE-DO 循环结构（条件+循环体）"""
        eid = nid()
        html = (
            '<table><tr><td style="text-align:center;font-size:9px;'
            'border-bottom:1px solid #333333;padding:4px;">'
            'WHILE ' + esc(condition) + '</td></tr>'
            '<tr><td style="text-align:center;font-size:9px;'
            'padding:8px;">' + esc(body) + '</td></tr></table>'
        )
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(html) + '" '
            'style="whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=none;strokeColor=#333333;fontSize=10;" '
            'vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, 'ns_while', rect))
        self._map[eid] = rect
        return eid

    def add_ns_until(self, x, y, w, h, condition, body):
        """DO-UNTIL 循环结构（循环体+底部条件）"""
        eid = nid()
        html = (
            '<table><tr><td style="text-align:center;font-size:9px;'
            'padding:8px;">' + esc(body) + '</td></tr>'
            '<tr><td style="text-align:center;font-size:9px;'
            'border-top:1px solid #333333;padding:4px;">'
            'UNTIL ' + esc(condition) + '</td></tr></table>'
        )
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(html) + '" '
            'style="whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=none;strokeColor=#333333;fontSize=10;" '
            'vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, 'ns_until', rect))
        self._map[eid] = rect
        return eid

    # ── UML用例图 ──────────────────────────────────────

    def add_uml_actor(self, x, y, size, name):
        """参与者 — 火柴人"""
        eid = nid()
        # Circle head + triangle body + name label
        head_r = size // 3
        cx = x + size // 2
        body_top = y + head_r * 2 + 2
        # circle head
        self.cells.append(
            '<mxCell id="' + nid() + '" value="" style="ellipse;'
            'fillColor=#333333;strokeColor=#333333;html=1;" '
            'vertex="1" parent="1">'
            '<mxGeometry x="' + str(cx - head_r) + '" y="' + str(y) + '" '
            'width="' + str(head_r * 2) + '" height="' + str(head_r * 2) + '" '
            'as="geometry"/></mxCell>')
        # body line (triangle path)
        body_w = size // 2
        self.cells.append(
            '<mxCell id="' + nid() + '" value="" style="shape=triangle;'
            'perimeter=trianglePerimeter;fillColor=#333333;'
            'strokeColor=#333333;html=1;" vertex="1" parent="1">'
            '<mxGeometry x="' + str(cx - body_w // 2) + '" y="' + str(body_top) + '" '
            'width="' + str(body_w) + '" height="' + str(size) + '" '
            'as="geometry"/></mxCell>')
        # name label below
        label_id = nid()
        self.cells.append(
            '<mxCell id="' + label_id + '" value="' + esc(name) + '" '
            'style="text;html=1;fontSize=10;fontColor=#333333;'
            'align=center;verticalAlign=top;" '
            'vertex="1" connectable="0" parent="1">'
            '<mxGeometry x="' + str(x - 20) + '" y="' + str(y + size + head_r + 4) + '" '
            'width="' + str(size + 40) + '" height="20" as="geometry"/></mxCell>')
        rect = (x, y, size, size + head_r + 24)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_uml_use_case(self, x, y, w, h, name):
        """用例 — 椭圆"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(name) + '" '
            'style="ellipse;whiteSpace=wrap;html=1;'
            'fillColor=#FFFFFF;strokeColor=#333333;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_uml_system_boundary(self, x, y, w, h, name):
        """系统边界 — 矩形框，顶部显示系统名"""
        eid = nid()
        html = (
            '<table><tr><td style="text-align:center;font-size:11px;'
            'font-weight:bold;padding:4px;">' + esc(name) + '</td></tr></table>'
        )
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(html) + '" '
            'style="whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=none;strokeColor=#666666;strokeWidth=2;'
            'fontSize=10;fontColor=#333333;dashed=0;" '
            'vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_uml_assoc(self, src, dst, label=''):
        """关联 — 实线"""
        return self.add_custom_edge(src, dst, label=label,
                                    end_arrow='none', dashed=False)

    def add_uml_generalize(self, src, dst):
        """泛化 — 实线+空心三角"""
        return self.add_custom_edge(src, dst, label='',
                                    end_arrow='block', end_fill=0, dashed=False)

    def add_uml_include(self, src, dst):
        """包含 <<include>> — 虚线箭头"""
        return self.add_custom_edge(src, dst, label='<<include>>',
                                    end_arrow='open', dashed=True)

    def add_uml_extend(self, src, dst):
        """扩展 <<extend>> — 虚线箭头"""
        return self.add_custom_edge(src, dst, label='<<extend>>',
                                    end_arrow='open', dashed=True)

    # ── UML状态图 ──────────────────────────────────────

    def add_uml_state(self, x, y, w, h, name):
        """状态 — 圆角矩形"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(name) + '" '
            'style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;'
            'fillColor=#FFFFFF;strokeColor=#333333;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_uml_choice(self, x, y, size):
        """选择 — 菱形"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="" '
            'style="rhombus;whiteSpace=wrap;html=1;'
            'fillColor=#FFFFFF;strokeColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(size) + '" height="' + str(size) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, size, size)
        self.entities.append((eid, 'choice', rect))
        self._map[eid] = rect
        return eid

    def add_uml_transition(self, src, dst, label='', guard='',
                           sx=1, sy=0.5, tx=0, ty=0.5):
        """转换 — 带监护条件 [guard] 的箭头"""
        full_label = label
        if guard:
            full_label = label + ' [' + guard + ']' if label else '[' + guard + ']'
        return self.add_connector(src, dst, label=full_label,
                                  sx=sx, sy=sy, tx=tx, ty=ty)

    # ── UML时序图 ──────────────────────────────────────

    def add_seq_actor(self, x, y, size, name):
        """时序图角色 — 火柴人+生命线"""
        eid = nid()
        head_r = size // 3
        cx = x + size // 2
        body_top = y + head_r * 2 + 2
        self.cells.append(
            '<mxCell id="' + nid() + '" value="" style="ellipse;'
            'fillColor=#333333;strokeColor=#333333;" vertex="1" parent="1">'
            '<mxGeometry x="' + str(cx - head_r) + '" y="' + str(y) + '" '
            'width="' + str(head_r * 2) + '" height="' + str(head_r * 2) + '" '
            'as="geometry"/></mxCell>')
        self.cells.append(
            '<mxCell id="' + nid() + '" value="" style="shape=triangle;'
            'fillColor=#333333;strokeColor=#333333;" vertex="1" parent="1">'
            '<mxGeometry x="' + str(cx - size//4) + '" y="' + str(body_top) + '" '
            'width="' + str(size // 2) + '" height="' + str(size) + '" '
            'as="geometry"/></mxCell>')
        label_id = nid()
        self.cells.append(
            '<mxCell id="' + label_id + '" value="' + esc(name) + '" '
            'style="text;html=1;fontSize=10;fontColor=#333333;'
            'align=center;" vertex="1" connectable="0" parent="1">'
            '<mxGeometry x="' + str(x - 20) + '" y="' + str(y + size + head_r + 2) + '" '
            'width="' + str(size + 40) + '" height="20" as="geometry"/></mxCell>')
        rect = (x, y, size, size + head_r + 22)
        self.entities.append((eid, name, rect))
        self._map[eid] = rect
        return eid

    def add_seq_object(self, x, y, w, h, name, class_name=''):
        """时序图对象矩形"""
        eid = nid()
        label = name
        if class_name:
            label = name + ':' + class_name if name else ':' + class_name
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" '
            'style="whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=#FFFFFF;strokeColor=#333333;fontSize=10;'
            'fontColor=#333333;" vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, label, rect))
        self._map[eid] = rect
        return eid

    def add_seq_lifeline(self, x, y_top, y_bottom):
        """生命线 — 垂直虚线"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="" style="'
            'line;strokeColor=#999999;strokeWidth=1;dashed=1;html=1;" '
            'vertex="1" connectable="0" parent="1">'
            '<mxGeometry x="' + str(x) + '" y="' + str(y_top) + '" '
            'width="1" height="' + str(y_bottom - y_top) + '" as="geometry"/>'
            '</mxCell>')

    def add_seq_activation(self, x, y, w, h):
        """激活条 — 窄矩形"""
        eid = nid()
        self.cells.append(
            '<mxCell id="' + eid + '" value="" style="'
            'whiteSpace=wrap;html=1;rounded=0;'
            'fillColor=#FFFFFF;strokeColor=#333333;" vertex="1" parent="1">'
            '<mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>'
            '</mxCell>')

    def add_seq_sync(self, x1, y1, x2, y2, label=''):
        """同步消息 — 实线+实心箭头"""
        return self._add_seq_message(x1, y1, x2, y2, label,
                                     dashed=False, end_arrow='classic')

    def add_seq_async(self, x1, y1, x2, y2, label=''):
        """异步消息 — 实线+开放箭头"""
        return self._add_seq_message(x1, y1, x2, y2, label,
                                     dashed=False, end_arrow='open')

    def add_seq_return(self, x1, y1, x2, y2, label=''):
        """返回消息 — 虚线+开放箭头"""
        return self._add_seq_message(x1, y1, x2, y2, label,
                                     dashed=True, end_arrow='open')

    def add_seq_self(self, x, y, label=''):
        """自关联消息 — 半闭合矩形"""
        eid = nid()
        style = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                 'strokeColor=#333333;strokeWidth=1;fontSize=9;'
                 'fontColor=#444444;endArrow=classic;endFill=1;')
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" style="' + style
            + '" edge="1" parent="1">'
            '<mxGeometry relative="1" as="geometry">'
            '<mxPoint x="' + str(x) + '" y="' + str(y) + '"/>'
            '<mxPoint x="' + str(x + 30) + '" y="' + str(y) + '"/>'
            '<Array as="points">'
            '<mxPoint x="' + str(x + 30) + '" y="' + str(y - 30) + '"/>'
            '</Array>'
            '</mxGeometry></mxCell>')

    def _add_seq_message(self, x1, y1, x2, y2, label, dashed, end_arrow):
        eid = nid()
        dash_str = 'dashed=1;' if dashed else ''
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(label) + '" style="'
            'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
            'strokeColor=#333333;strokeWidth=1;fontSize=9;fontColor=#444444;'
                + dash_str +
            'endArrow=' + end_arrow + ';endFill=1;"'
            ' edge="1" parent="1">'
            '<mxGeometry relative="1" as="geometry">'
            '<mxPoint x="' + str(x1) + '" y="' + str(y1) + '"/>'
            '<mxPoint x="' + str(x2) + '" y="' + str(y2) + '"/>'
            '</mxGeometry></mxCell>')

    # ── UML活动图初始/结束节点 ──────────────────────────

    def add_uml_initial_node(self, x, y, size=16,
                             parent='1', parent_x=0, parent_y=0):
        """UML Initial Node — solid black filled circle"""
        eid = nid()
        abs_x = x + parent_x
        abs_y = y + parent_y
        self.cells.append(
            '<mxCell id="' + eid + '" value="" style="ellipse;'
            'fillColor=#000000;strokeColor=#000000;html=1;" '
            'vertex="1" parent="' + parent + '">'
            '<mxGeometry x="' + str(abs_x) + '" y="' + str(abs_y) + '" '
            'width="' + str(size) + '" height="' + str(size) + '" '
            'as="geometry"/></mxCell>')
        rect = (abs_x, abs_y, size, size)
        self.entities.append((eid, 'initial', rect))
        self._map[eid] = rect
        return eid

    def add_uml_final_node(self, x, y, size=22,
                           parent='1', parent_x=0, parent_y=0):
        """UML Final Node — solid circle inside hollow outer circle (bullseye)"""
        eid = nid()
        abs_x = x + parent_x
        abs_y = y + parent_y
        self.cells.append(
            '<mxCell id="' + eid + '" value="" style="ellipse;'
            'fillColor=#000000;strokeColor=#000000;html=1;" '
            'vertex="1" parent="' + parent + '">'
            '<mxGeometry x="' + str(abs_x + 3) + '" y="' + str(abs_y + 3) + '" '
            'width="' + str(size - 6) + '" height="' + str(size - 6) + '" '
            'as="geometry"/></mxCell>')
        outer = nid()
        self.cells.append(
            '<mxCell id="' + outer + '" value="" style="ellipse;'
            'fillColor=none;strokeColor=#000000;strokeWidth=3;html=1;" '
            'vertex="1" parent="' + parent + '">'
            '<mxGeometry x="' + str(abs_x) + '" y="' + str(abs_y) + '" '
            'width="' + str(size) + '" height="' + str(size) + '" '
            'as="geometry"/></mxCell>')
        rect = (abs_x, abs_y, size, size)
        self.entities.append((eid, 'final', rect))
        self._map[eid] = rect
        return eid

    # ── 泳道图 ─────────────────────────────────────────

    def add_swimlane(self, x, y, w, h, label,
                     color='#E8F0FE', header_size=50, horizontal=True):
        """Swimlane container (UML 2.5 partition / BPMN pool)"""
        eid = nid()
        if horizontal:
            shape = 'swimlane;startSize=' + str(header_size) + ';'
            html = '<b>' + esc(label) + '</b>'
        else:
            shape = 'swimlane;startSize=' + str(header_size) + ';horizontal=0;'
            html = esc(label)
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(html) + '" '
            'style="' + shape + 'whiteSpace=wrap;html=1;'
            'fillColor=' + color + ';strokeColor=#DCDCDC;'
            'fontSize=11;fontColor=#333333;" '
            'vertex="1" parent="1">')
        self.cells.append(
            '    <mxGeometry x="' + str(x) + '" y="' + str(y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('  </mxCell>')
        rect = (x, y, w, h)
        self.entities.append((eid, label, rect))
        self._map[eid] = rect
        return eid

    def add_label_in_lane(self, lane_id, lane_x, lane_y,
                          x_rel, y_rel, w, h, text,
                          font_size=11, bold=False, color='#333333'):
        """Borderless text label inside a swimlane"""
        eid = nid()
        abs_x = lane_x + x_rel
        abs_y = lane_y + y_rel
        style = ('text;html=1;fontSize=' + str(font_size) + ';'
                 'fontColor=' + color + ';fontStyle=' + ('4' if bold else '0') + ';'
                 'align=center;verticalAlign=middle;')
        self.cells.append(
            '<mxCell id="' + eid + '" value="' + esc(text) + '" '
            'style="' + style + '" vertex="1" connectable="0" parent="1">')
        self.cells.append(
            '  <mxGeometry x="' + str(abs_x) + '" y="' + str(abs_y) + '" '
            'width="' + str(w) + '" height="' + str(h) + '" as="geometry"/>')
        self.cells.append('</mxCell>')
        rect = (abs_x, abs_y, w, h)
        self.entities.append((eid, text, rect))
        self._map[eid] = rect
        return eid

    # ── 连接器路由 ─────────────────────────────────────

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

    def add_custom_edge(self, src, dst, label='',
                        end_arrow='classic', end_fill=1, dashed=False,
                        sx=1, sy=0.5, tx=0, ty=0.5):
        """Custom edge with configurable arrow type and dash style."""
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
        dash_style = 'dashed=1;' if dashed else ''
        style = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                 'strokeColor=#999999;strokeWidth=1;fontSize=10;'
                 'fontColor=#444444;fontStyle=2;labelBackgroundColor=#FFFFFF;'
                 + dash_style +
                 'endArrow=' + end_arrow + ';endFill=' + str(end_fill) + ';'
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
        return eid

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
- **数据流图 (DFD)**: external entities → processes → data stores → data flows
- **程序流程图**: start/end → process → decision → data I/O → control flows
- **N-S盒图**: sequence → IF-THEN-ELSE → WHILE-DO → DO-UNTIL in nested boxes
- **UML类图**: class box = table header (stereotype) + attributes + methods
- **UML用例图**: actor → use case → system boundary → 4 relationship types
- **UML状态图**: initial state → states → transitions with guards → final state
- **UML时序图**: actor/object → lifeline → activation → sync/async/return messages
- **Architecture diagrams**: component = table with header (name) + rows (endpoints/ports)
- **Flowcharts / Activity diagrams**: use `add_swimlane()` for Visio-style cross-functional lanes, then place borderless text labels with `add_label_in_lane()`
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
| **Swimlane (horizontal)** | `add_swimlane(horizontal=True)` | Flowchart activities by role, lanes stacked top→bottom |
| **Swimlane (vertical pool)** | `add_swimlane(horizontal=False)` | UML activity partitions / BPMN pools, lanes placed left→right |
| **UML Activity** | vertical pools + initial/final nodes | UML 2.5 activity diagrams with solid circle start/end |
| **DFD分层** | External entities on edges, processes in center, top→bottom | 数据流图多层分解 |
| **程序流程图** | Top-to-bottom with decision diamonds | 算法/过程逻辑描述 |
| **N-S盒图** | Nested rectangles in one box | 结构化程序设计 |
| **UML用例图** | Actors outside boundary, use cases inside | 系统功能需求建模 |
| **UML状态图** | Initial→states→choice→final top-to-bottom | 对象生命周期建模 |
| **UML时序图** | Objects across top, messages top→down | 对象间交互时序 |

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

## Local Files

| File | Description |
|------|-------------|
| `README.md` | Full Chinese documentation with API reference, examples, troubleshooting |
| `examples/er_diagram.py` | Runnable script that generates 5 ER diagrams (run: `python examples/er_diagram.py`) |

## Dependencies

- **draw.io Desktop** (free): https://github.com/jgraph/drawio-desktop/releases
- **Python 3.10+** (stdlib only: `os`, `subprocess`, `xml.sax.saxutils`)
- **No pip packages required**

---

**GitHub**: https://github.com/getfunWindz/visio-style-diagram
