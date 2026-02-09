# 📋 外部技能克隆与适配协议 (Skills Cloning Protocol)

## 1. 目标定位 (Targeting)
- **GitHub**: 搜索 `stars > 100` 且 `last commit < 6 months` 的垂直领域 Repo。
- **Hugging Face**: 锁定 `smolagents` 或 `transformers` 驱动的最新执行脚本。
- **MCP Registry**: 查找官方或社区认证的 MCP Server。

## 2. 提取流程 (Extraction Workflow)
1. **源码解构 (Deconstruction)**：使用 `search_web` 或直接读取 Repo 结构，识别核心逻辑文件（如 `strategy.py`, `utils.py`）。
2. **逻辑脱水 (Dehydration)**：剥离多余的依赖和复杂的 UI，只保留最核心的算法或工具函数。
3. **架构适配 (Adaptation)**：将功能按职能分配至本地六大部门：
   - 交易/数据 -> `【金融汇报】/scripts/`
   - 底层工具 -> `【核心脚本】/scripts/`
   - 自动化/同步 -> `【技能铸造】/scripts/`

## 3. 安全与验证 (Validation)
- **代码审计**：严禁执行任何包含未加密私钥请求或可疑网络外发的外部脚本。
- **沙箱运行**：首次运行必须在受限环境下进行。
- **验收标准**：克隆后的脚本必须能在 `agent_agno.py` 中通过工具调用成功触发。

## 4. 自动记录
- 每次成功克隆后，必须在 `task.md` 中记录来源 Repo 以备溯源。
