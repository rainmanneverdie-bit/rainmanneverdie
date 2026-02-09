# 🛠️ Engineering Discipline & Development Protocol

## 1. Occam's Razor
- **Minimalism**: Do not add dependencies (pip/npm) unless it simplifies the code by at least 50%.
- **Dry/KISS**: Prefer standard library over "cool" frameworks unless production-essential.

## 2. Linter-Driven Fixes
- **Workflow**: Do not guess style issues. Run a linter (if available) or check execution logs.
- **Self-Healing**: If a script fails, locate the exact line, explain the *ROOT CAUSE* in 10 words, and patch only that line.

## 3. Scaling & Modularity
- **Architecture**: Always check if a function can be abstracted into an "Internal Skill" before hardcoding it.
- **Performance**: High-frequency data loops must be asynchronous or efficient enough to run on a standard Mac environment.

## 4. Documentation
- **Comments**: Only comment on "Why", not "What".
- **Naming**: Use descriptive variable names that reflect financial or technical context (e.g., `funding_rate` instead of `fr`).

## 5. API Keys 健康检查
- **启动时验证**: 所有 API keys 必须在系统启动时验证有效性
- **失败告警**: 验证失败时记录到日志并通知用户
- **降级策略**: 关键服务（如推送）必须有备用渠道
- **定期检查**: 每小时检查一次关键服务状态

