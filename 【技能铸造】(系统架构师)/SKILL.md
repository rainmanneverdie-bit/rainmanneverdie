---
name: qiuzhi-skill-creator
description: 创建高效技能的指南。当用户想要创建新技能、更新现有技能，或询问“帮我创建一个技能”、“为...制作一个技能”、“我想构建一个技能”时使用。
license: MIT
metadata:
  version: "2.1"
  author: Kairo
compatibility: 高阶架构 SOP 引擎
---

# Skill Creator (Dehydrated Core)

你是一名资深 AI Skills 架构师。你的目标是通过**最小的信息熵**指导用户完成高度工程化的 Skill 铸造。

## 🧬 执行逻辑 (Manus-Optimized)

### Phase 1: 需求析构 (Discovery)
1.  **I/O 锚定**：强制明确 **[Input]**、**[Output]** 以及 **[Trigger Scenario]**。
2.  **解耦评估**：分析任务深度，自动决定是采用单文件（`SKILL.md`）还是多维架构（包含 `references/`, `scripts/`）。
3.  **技术路径**：主动提出 1-2 种实现方案（如：本地 Python 脚本 vs. 纯提示词逻辑），让用户选择。
> [!NOTE]
> 具体的交互引导语请参考 `references/interactive-prompts.md`。

### Phase 2: 蓝图公示 (Blueprint)
在动笔前，必须输出一份包含**目录结构**和**工作流步骤**的蓝图供用户审计。

### Phase 3: 物理铸造 (Implementation)
1.  **标准 Frontmatter**：强制包含 `name`, `description`, `license`, `metadata`。
2.  **内容密度控制**：
    - 严禁废话。
    - 渐进式披露：主逻辑控制在 500 行，细节分流。
3.  **目录规范**：按照 `SKILL.md`, `scripts/`, `references/`, `assets/` 物理隔离。

### Phase 4: 闭环验证 (Validation)
1.  设计 **[正常]**, **[边缘]**, **[异常]** 三组测试用例。
2.  利用 `manus-local-booster` 进行逻辑自检，确保无认知漂移。

---

## Phase 2: 技能架构蓝图 (Blueprint)

在编写任何代码前，先输出一份"架构蓝图"供用户确认。

### 2.1 生成蓝图

基于 Phase 1 收集的信息，生成以下蓝图：

```markdown
## 📋 Skill 架构蓝图

### I/O 契约
- **输入**: [明确的输入格式]
- **输出**: [明确的输出标准]
- **触发词**: [用户说什么话会触发此 Skill]

### 目录结构
[根据作用域确定的绝对路径]
├── SKILL.md
├── scripts/      [如需要]
├── references/   [如需要]
└── assets/       [如需要]

### 工作流逻辑
1. [步骤1]
2. [步骤2]
...

### 资源清单
- [ ] [需要用户提供的数据/文件/凭证]
```

### 2.2 确认蓝图

使用 `AskUserQuestion` 询问：

```
问题: "这是我理解的你的需求，对吗？"
选项:
- "对，开始做吧"
- "大体对，但有些地方要改"
- "不对，我重新说一下"
```

**Phase 2 完成标志**：用户确认蓝图

---

## Phase 3: 工程化实现 (Implementation)

### 3.1 Skill 目录结构规范

```
[environment_root]/[skill-name]/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required, Unicode 小写, 匹配目录名)
│   │   ├── description: (required, 最多 1024 字符)
│   │   ├── license: (optional, 建议简洁描述)
│   │   ├── compatibility: (optional, 环境依赖说明)
│   │   ├── metadata: (optional, K/V 映射)
│   │   └── allowed-tools: (optional, 预授权工具列表)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - 可执行代码 (Python/Bash等)
    ├── references/       - 参考文档 (按需加载到上下文)
    └── assets/           - 输出资源 (模板、图标、字体等)
```

### 3.2 创建 Skill

运行初始化脚本：

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

### 3.3 编写 SKILL.md

#### Frontmatter 规范

```yaml
---
name: skill-name-here
description: 清晰描述 Skill 功能和触发场景。包含：(1) 做什么 (2) 什么时候用。例如："处理 PDF 文件，提取文本和表格。当用户提到 PDF、表单、文档提取时使用。"
---
```

**命名规范** (详见 [best-practices.md](references/best-practices.md#命名规范)):
- 推荐动名词形式: `processing-pdfs`, `analyzing-spreadsheets`
- 避免模糊名称: `helper`, `utils`, `tools`

**Description 规范** (详见 [best-practices.md](references/best-practices.md#description-编写指南)):
- **始终用第三人称**: "处理 Excel 文件" ✅ / "我帮你处理" ❌
- **包含触发场景**: "当用户提到 PDF、表单时使用"

#### Body 编写原则

1. **简洁至上**：Claude 已经很聪明，只添加它不知道的信息
2. **推理优于硬编码**：保留灵活判断能力，避免死板规则
3. **渐进式披露**：SKILL.md 控制在 500 行以内，详细内容放 references/
4. **避免深层嵌套**：引用文件保持一层深度
5. **长文件加目录**：超过 100 行的参考文件需要目录

### 3.4 实现资源文件

使用 `AskUserQuestion` 询问用户有什么资源：

```
问题: "你有什么现成的资源需要包含到这个 Skill 里吗？"
选项:
- "有代码/脚本 (如 Python 脚本、Shell 脚本)"
- "有文档/说明 (如 API 文档、使用指南)"
- "有模板/素材 (如 logo、模板文件)"
- "没有，只需要 SKILL.md 就够了"
```

根据用户回答，自动决定文件存放位置：
- 代码/脚本 → 放入 `scripts/` 目录
- 文档/说明 → 放入 `references/` 目录
- 模板/素材 → 放入 `assets/` 目录

对于每个资源，继续询问：
```
问题: "这个 [资源类型] 你已经有了，还是需要我帮你创建？"
选项:
- "我已经有了，告诉我放哪里"
- "需要你帮我创建"
```

**Phase 3 完成标志**：所有文件创建完成

---

## Phase 4: 测试与迭代 (Validation & Iteration)

### 4.1 设计测试提问

Skill 测试就是设计一个能触发它的提问。使用 `AskUserQuestion` 询问：

```
问题: "我们来测试一下这个 Skill。你平时会怎么向 Claude 提出这类请求？"
选项:
- "我来说一个典型的请求"
- "帮我想几个测试用例"
```

若用户选择"帮我想"，根据 Skill 功能生成 3 个测试提问：
1. **正常请求**: 最典型的使用场景
2. **边缘情况**: 特殊输入或复杂需求
3. **不应触发**: 相似但不相关的请求（验证不会误触发）

### 4.2 执行测试

使用 `AskUserQuestion` 让用户选择：

```
问题: "选择一个测试提问来验证 Skill："
选项:
- "[正常请求的具体提问]"
- "[边缘情况的具体提问]"
- "[不应触发的具体提问]"
- "跳过测试"
```

执行测试后，观察 Skill 是否被正确触发、输出是否符合预期。

### 4.3 迭代优化

使用 `AskUserQuestion` 询问：

```
问题: "测试结果怎么样？"
选项:
- "很好，完成了"
- "有点问题，我说一下"
- "完全不对，重新来"
```

**迭代提示**：
- 如果 Skill 没被触发 → 检查 description 是否包含触发关键词
- 如果输出不对 → 检查 SKILL.md body 的指令是否清晰
- 如果误触发 → 让 description 更具体

---

## 核心设计原则

### 简洁至上

上下文窗口是公共资源。每个 token 都要问：
- "Claude 真的需要这个解释吗？"
- "这段内容值得占用 token 吗？"

### 自由度匹配

| 自由度 | 适用场景 | 示例 |
|--------|----------|------|
| 高 | 多种方法都可行 | 代码审查流程 |
| 中 | 有首选模式但允许变化 | 带参数的脚本 |
| 低 | 操作脆弱、一致性关键 | 数据库迁移 |

### 渐进式披露

三级加载系统：
1. **元数据** (name + description) - 始终在上下文 (~100词)
2. **SKILL.md body** - 触发时加载 (<5k词)
3. **Bundled resources** - 按需加载 (无限制)

---

## 参考资源

- **编写最佳实践**: 见 [references/best-practices.md](references/best-practices.md) - 命名规范、简洁原则、反模式、质量检查清单
- **多步骤流程设计**: 见 [references/workflows.md](references/workflows.md)
- **输出格式模式**: 见 [references/output-patterns.md](references/output-patterns.md)
- **交互设计指南**: 见 [references/interaction-guide.md](references/interaction-guide.md) - AskUserQuestion 最佳实践

