# 📐 BaseFormatTemplate

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Version-1.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Architecture-ABC%20Abstract-orange.svg" alt="ABC">
  <img src="https://img.shields.io/badge/Forward%20Message-Supported-brightgreen.svg" alt="Forward Message">
  <img src="https://img.shields.io/badge/NcatBot-Plugin-purple.svg" alt="NcatBot">
</p>

> ✨ NcatBot 官方标准插件模板 - 基于 ABC 抽象类的消息字段一键访问

---

## 🌍 语言选择 / Language Selection

- [🇨🇳 中文文档](#-这是什么)
- [🇺🇸 English Documentation](#-what-is-this)

---

## 🇨🇳 中文文档

---

## 📖 这是什么？

这是 **NcatBot 官方标准插件模板**，基于 ABC 抽象类设计，一键获取所有消息字段。

**以前需要写 50 行代码，现在只需 3 行：**

| ❌ 以前 | ✅ 现在 |
|-----------|--------|
| 手动时间格式化 | 自动格式化时间 |
| 手动字典翻译 | 自动中文翻译 |
| 手动提取图片 | 自动解析消息链 |
| 用变量存数据 | 一个对象全部搞定 |
| 不支持合并转发 | 递归解析多层嵌套 |

---

## 🚀 5 秒快速上手

### 第一步：导入
```python
from lottery import LotteryData
```

### 第二步：初始化
```python
# 只需传入 event 即可！
data = LotteryData(event)
```

### 第三步：获取数据
```python
# 直接用点语法调用！
user_id = data.sender_info.get_user_id()
user_name = data.sender_info.get_user_name()
text_content = data.message_info.get_text_content()
group_name = data.group_info.get_group_name()
```

---

## 📋 抽象类字段参考

### ⏰ 时间信息
**用法:** `data.time_info.方法名()`

| 你想获取的信息 | 方法 | 示例 |
|---------------|--------|---------|
| 格式化时间 | `get_formatted_time()` | `2024-01-15 14:30:00` |
| 时间戳 | `get_timestamp()` | `1705299600` |

---

### 📱 基本信息
**用法:** `data.basic_info.方法名()`

| 你想获取的信息 | 方法 | 示例 |
|---------------|--------|---------|
| 机器人 QQ 号 | `get_self_id()` | `123456789` |
| 平台 | `get_platform()` | `QQ` |
| 事件类型 | `get_post_type()` | `消息` |
| 消息类型 | `get_message_type()` | `群聊` |
| 子类型 | `get_sub_type()` | `普通` |

---

### 👥 群组信息
**用法:** `data.group_info.方法名()`

| 你想获取的信息 | 方法 | 示例 |
|---------------|--------|---------|
| 群号 | `get_group_id()` | `987654321` |
| 群名 | `get_group_name()` | `Python 交流群` |

---

### 💬 消息信息 ✨ 新增合并转发支持
**用法:** `data.message_info.方法名()`

| 你想获取的信息 | 方法 | 示例 |
|---------------|--------|---------|
| 消息 ID | `get_message_id()` | `-2147483647` |
| 消息序号 | `get_message_seq()` | `1234` |
| 真实 ID | `get_real_id()` | `1234` |
| 真实序号 | `get_real_seq()` | `1234` |
| 文字内容 | `get_text_content()` | `Hello World` |
| 图片链接列表 | `get_image_urls()` | `["http://xxx.jpg", ...]` |
| 图片数量 | `get_image_count()` | `3` |
| **是否包含合并转发** | `has_forward_message()` | `True` / `False` |
| **合并转发消息数** | `get_forward_count()` | `3` |
| **处理合并转发消息** | `process_forward_message(msg)` | 返回格式化字符串 |
| **处理节点消息** | `process_node_message(node, depth)` | 递归解析嵌套消息 |

> 💡 **提示：** 空内容自动返回 `"无"`，无需 None 判断！

> 🔥 **特别支持：多层嵌套合并转发**
> 
> 无论嵌套多少层的合并转发消息，都会自动递归解析，正确显示发送者、内容和图片。
>
> 示例效果：
> ```
> 【合并转发消息】
> ── 消息 1 ──
>   发送者: E学奇G (2678966)
>   └── 嵌套消息:
>     发送者: E学奇G (2678966)
>     内容: 我是第一个合并的第1个消息
> ```

---

### 👤 发送者信息
**用法:** `data.sender_info.方法名()`

| 你想获取的信息 | 方法 | 示例 |
|---------------|--------|---------|
| 用户 QQ 号 | `get_user_id()` | `10001` |
| 昵称 | `get_nickname()` | `小明` |
| 群名片 | `get_card()` | `班长小明` |
| 群角色 | `get_role()` | `群主` / `管理员` / `成员` |
| 性别 | `get_sex()` | `男` / `女` / `未知` |
| 显示名称 | `get_user_name()` | 优先群名片，其次昵称 |

> 💡 **提示：** 空群名片自动返回 `"无"`！

---

## 💪 完整示例

### 示例 1：简单抽奖
```python
from lottery import LotteryData

@registrar.on_group_command("抽奖")
async def lottery_command(event):
    # 1. 初始化 - 一行获取所有数据
    data = LotteryData(event)
    
    # 2. 获取你需要的字段
    participant_id = data.sender_info.get_user_id()
    participant_name = data.sender_info.get_user_name()
    group_id = data.group_info.get_group_id()
    join_time = data.time_info.get_formatted_time()
    
    # 3. 编写业务逻辑
    await event.reply(f"🎊 恭喜 {participant_name}！于 {join_time} 成功参与")
```

### 示例 2：处理合并转发消息
```python
data = LotteryData(event)

# 检测是否包含合并转发
if data.message_info.has_forward_message():
    print(f"检测到合并转发，共 {data.message_info.get_forward_count()} 条")
    print(f"完整内容：{data.message_info.get_text_content()}")
```

### 示例 3：遍历图片
```python
data = LotteryData(event)

# 获取所有图片链接并遍历
for i, image_url in enumerate(data.message_info.get_image_urls(), 1):
    print(f"第 {i} 张图片：{image_url}")
```

---

## 📁 项目结构（标准 GitHub 结构）

```
BaseFormatTemplate/
├── 📄 README.md               👈 本文档（中英文双语）
├── 📄 manifest.toml           NcatBot 插件配置文件
├── 📄 main.py                 插件主入口
├── 📄 saveMessage.py            消息保存工具
│
└── 📂 lottery/                核心数据封装模块
│   ├── 📄 __init__.py               模块导出
│   ├── 📄 lottery_data.py         🎁 主入口类（你需要的）
│   ├── 📄 lottery_factory.py      🏭 工厂类（高级用法）
│   │
│   ├── 📐 抽象接口层
│   │   ├── abc_time_info.py          时间信息接口
│   │   ├── abc_basic_info.py       基本信息接口
│   │   ├── abc_group_info.py       群组信息接口
│   │   ├── abc_message_info.py     消息信息接口（含合并转发）
│   │   └── abc_sender_info.py      发送者信息接口
│   │
│   └── ⚙️ 具体实现层
│       ├── time_info.py              时间信息实现
│       ├── basic_info.py           基本信息实现
│       ├── group_info.py           群组信息实现
│       ├── message_info.py       消息信息实现（递归解析嵌套）
│       └── sender_info.py          发送者信息实现
│
└── 📂 __pycache__/              Python 缓存（自动生成）
```

---

## ❓ 常见问题

### Q: 如何新增字段？
A: 非常简单！
1. 在对应的 `lottery/abc_xxx.py` 接口中添加 `@abstractmethod`
2. 在对应的 `lottery/xxx.py` 类中编写实现

### Q: 如何修改翻译？
A: 打开对应 `lottery/xxx.py` 文件，修改顶部的 `_XX_MAP` 字典即可。

### Q: 抽象类是什么？我需要懂吗？
A: **不需要！** 你只需要知道用 `.get_xxx()` 获取数据即可。
> 抽象类就像插座标准，你只要会插电器就行，不需要懂里面的电路怎么接。

### Q: 合并转发最多支持几层嵌套？
A: 理论上无限层！采用递归解析，只要内存足够可以处理任意深度。
> 实际使用中 QQ 一般最多 3-5 层嵌套，完全够用。

---

## 🏆 设计优势

| 特性 | 说明 |
|---------|-------------|
| ✅ 接口隔离 | 面向接口编程 |
| ✅ 单一职责 | 一个文件 = 一件事 |
| ✅ 工厂模式 | 透明替换实现 |
| ✅ 类型提示 | IDE 完美自动补全 |
| ✅ 递归解析 | 多层嵌套合并转发 |
| ✅ 向下兼容 | 旧代码无需改动 |

---

---

## 🇺🇸 English Documentation

---

## 📖 What is this?

This is the **official standard plugin template for NcatBot**, based on ABC abstract classes for one-click access to all message fields.

**What used to require 50 lines of code now takes only 3 lines:**

| ❌ Before | ✅ Now |
|-----------|--------|
| Manual time formatting | Auto formatted time |
| Manual dictionary translation | Auto Chinese translation |
| Manual image extraction | Auto message chain parsing |
| Store data in variables | One object for everything |
| No forward message support | Recursive multi-layer nesting |

---

## 🚀 5 Second Quick Start

### Step 1: Import
```python
from lottery import LotteryData
```

### Step 2: Initialize
```python
# Just pass the event, that's all!
data = LotteryData(event)
```

### Step 3: Get your data
```python
# Just use dot notation!
user_id = data.sender_info.get_user_id()
user_name = data.sender_info.get_user_name()
text_content = data.message_info.get_text_content()
group_name = data.group_info.get_group_name()
```

---

## 📋 Abstract Class Field Reference

### ⏰ Time Info
**Usage:** `data.time_info.method_name()`

| What you want | Method | Example |
|---------------|--------|---------|
| Formatted time | `get_formatted_time()` | `2024-01-15 14:30:00` |
| Timestamp | `get_timestamp()` | `1705299600` |

---

### 📱 Basic Info
**Usage:** `data.basic_info.method_name()`

| What you want | Method | Example |
|---------------|--------|---------|
| Bot QQ ID | `get_self_id()` | `123456789` |
| Platform | `get_platform()` | `QQ` |
| Post Type | `get_post_type()` | `消息` |
| Message Type | `get_message_type()` | `群聊` |
| Sub Type | `get_sub_type()` | `普通` |

---

### 👥 Group Info
**Usage:** `data.group_info.method_name()`

| What you want | Method | Example |
|---------------|--------|---------|
| Group ID | `get_group_id()` | `987654321` |
| Group Name | `get_group_name()` | `Python Community` |

---

### 💬 Message Info ✨ Forward Message Support
**Usage:** `data.message_info.method_name()`

| What you want | Method | Example |
|---------------|--------|---------|
| Message ID | `get_message_id()` | `-2147483647` |
| Message Sequence | `get_message_seq()` | `1234` |
| Real ID | `get_real_id()` | `1234` |
| Real Sequence | `get_real_seq()` | `1234` |
| Text Content | `get_text_content()` | `Hello World` |
| Image URL List | `get_image_urls()` | `["http://xxx.jpg", ...]` |
| Image Count | `get_image_count()` | `3` |
| **Has Forward Msg** | `has_forward_message()` | `True` / `False` |
| **Forward Msg Count** | `get_forward_count()` | `3` |
| **Process Forward Msg** | `process_forward_message(msg)` | Returns formatted string |
| **Process Node Msg** | `process_node_message(node, depth)` | Recursively parse nested |

> 💡 **Tip:** Empty content automatically returns `"无"`, no need for None checks!

> 🔥 **Feature: Multi-layer Nested Forward**
> 
> No matter how many layers of nested forward messages, they will be automatically and recursively parsed, correctly displaying sender, content and images.
>
> Example output:
> ```
> 【Combined Forward Message】
> ── Message 1 ──
>   Sender: E学奇G (2678966)
>   └── Nested Message:
>     Sender: E学奇G (2678966)
>     Content: I'm nested message 1
> ```

---

### 👤 Sender Info
**Usage:** `data.sender_info.method_name()`

| What you want | Method | Example |
|---------------|--------|---------|
| User QQ ID | `get_user_id()` | `10001` |
| Nickname | `get_nickname()` | `小明` |
| Group Card | `get_card()` | `班长小明` |
| Group Role | `get_role()` | `群主` / `管理员` / `成员` |
| Gender | `get_sex()` | `男` / `女` / `未知` |
| Display Name | `get_user_name()` | Group card first, then nickname |

> 💡 **Tip:** Empty group card automatically returns `"无"`!

---

## 💪 Complete Examples

### Example 1: Simple Lottery
```python
from lottery import LotteryData

@registrar.on_group_command("lottery")
async def lottery_command(event):
    # 1. Initialize - get all data in one line
    data = LotteryData(event)
    
    # 2. Get the fields you need
    participant_id = data.sender_info.get_user_id()
    participant_name = data.sender_info.get_user_name()
    group_id = data.group_info.get_group_id()
    join_time = data.time_info.get_formatted_time()
    
    # 3. Write your business logic
    await event.reply(f"🎊 Congratulations {participant_name}! Joined at {join_time}")
```

### Example 2: Handle Forward Message
```python
data = LotteryData(event)

# Detect forward message
if data.message_info.has_forward_message():
    print(f"Forward detected, {data.message_info.get_forward_count()} messages total")
    print(f"Full content: {data.message_info.get_text_content()}")
```

### Example 3: Iterate Images
```python
data = LotteryData(event)

# Get all image URLs and loop through them
for i, image_url in enumerate(data.message_info.get_image_urls(), 1):
    print(f"Image #{i}: {image_url}")
```

---

## 📁 Project Structure (Standard GitHub Structure)

```
BaseFormatTemplate/
├── 📄 README.md               👈 This documentation (Bilingual)
├── 📄 manifest.toml           NcatBot Plugin Configuration
├── 📄 main.py                 Plugin Entry Point
├── 📄 saveMessage.py            Message Save Utility
│
└── 📂 lottery/                Core Data Encapsulation Module
│   ├── 📄 __init__.py               Module Exports
│   ├── 📄 lottery_data.py         🎁 Main Entry (You need this)
│   ├── 📄 lottery_factory.py      🏭 Factory Class (Advanced)
│   │
│   ├── 📐 Abstract Interface Layer
│   │   ├── abc_time_info.py          Time Info Interface
│   │   ├── abc_basic_info.py       Basic Info Interface
│   │   ├── abc_group_info.py       Group Info Interface
│   │   ├── abc_message_info.py     Message Info Interface
│   │   └── abc_sender_info.py      Sender Info Interface
│   │
│   └── ⚙️ Implementation Layer
│       ├── time_info.py              Time Info Implementation
│       ├── basic_info.py           Basic Info Implementation
│       ├── group_info.py           Group Info Implementation
│       ├── message_info.py       Message Info Implementation
│       └── sender_info.py          Sender Info Implementation
│
└── 📂 __pycache__/              Python Cache (Auto-generated)
```

---

## ❓ FAQ

### Q: How do I add new fields?
A: Very simple!
1. Add an `@abstractmethod` in the corresponding `lottery/abc_xxx.py` interface
2. Write the implementation in the corresponding `lottery/xxx.py` class

### Q: How to change the translations?
A: Open the corresponding `lottery/xxx.py` file and modify the `_XX_MAP` dictionary at the top.

### Q: What are abstract classes? Do I need to understand?
A: **NO!** You just need to know how to use `.get_xxx()` to get data.
> Abstract classes are like electrical outlet standards. You just need to know how to plug things in, not how the wiring works.

### Q: How many nesting layers are supported for forward messages?
A: Theoretically unlimited! Uses recursive parsing, can handle any depth as long as memory allows.
> In practice, QQ usually has at most 3-5 layers of nesting, which is more than enough.

---

## 🏆 Design Benefits

| Feature | Explanation |
|---------|-------------|
| ✅ Interface Segregation | Interface-based programming |
| ✅ Single Responsibility | One file = One job |
| ✅ Factory Pattern | Swap implementations transparently |
| ✅ Type Hints | IDE autocompletion works |
| ✅ Recursive Parsing | Multi-layer nested forward |
| ✅ Backward Compatible | No changes to old code |

---
