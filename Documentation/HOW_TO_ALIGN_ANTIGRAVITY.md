# 📖 如何让 Antigravity 对齐规则

## 方法 1：发送快速对齐包（推荐）

### 步骤 1：复制文档内容
```bash
cat /Users/neverdie/iflow_workspace/QUICK_ALIGN.md
```

### 步骤 2：在 Antigravity 中粘贴
直接发送给 Antigravity：
```
请阅读以下项目规则，并严格遵守：

[粘贴 QUICK_ALIGN.md 的全部内容]
```

### 步骤 3：验证理解
让 Antigravity 回答：
```
请回答以下问题验证你已理解规则：
1. AlexWang 的单笔风险偏好是多少？
2. 做决策前必须执行什么步骤？
3. 如果你犯错了应该怎么办？
```

---

## 方法 2：让 Antigravity 自己读取

如果 Antigravity 可以访问文件系统：
```
请阅读以下文件并遵守其中的规则：
1. /Users/neverdie/iflow_workspace/QUICK_ALIGN.md
2. /Users/neverdie/iflow_workspace/【金融汇报】(分析主理人)/Knowledge_Archive/aboutme.md
3. /Users/neverdie/iflow_workspace/CLAUDE.md
```

---

## 方法 3：创建 Antigravity 专用配置

如果 Antigravity 支持配置文件，我可以创建一个 `.antigravity.config` 文件。

---

## 协作流程示例

### 场景 1：你想让 Antigravity 设计品牌
```
你：我现在让 Antigravity 设计品牌，你暂停工作。
Claude Code：收到，已暂停。记得完成后 git commit。

[切换到 Antigravity]
你：[粘贴 QUICK_ALIGN.md]
你：请设计一个 Logo，风格要符合量化交易的专业感。
Antigravity：[开始工作]

[完成后]
你：git commit -m "feat: 新增品牌 Logo"
你：Claude Code，Antigravity 已完成，你可以继续了。
```

### 场景 2：你想让 Antigravity 写前端代码
```
你：[粘贴 QUICK_ALIGN.md]
你：请创建一个交易仪表盘，但不要修改 Python 交易脚本。
Antigravity：收到，我只负责前端部分。
```

---

## 常见问题

**Q: Antigravity 会不会覆盖你的修改？**
A: 只要遵守"同一时间只让一个 AI 操作"的规则，就不会冲突。

**Q: 如果 Antigravity 不遵守规则怎么办？**
A: 立即停止它，让我（Claude Code）检查并修复。

**Q: 我可以同时问两个 AI 吗？**
A: 可以，但不要让它们同时修改同一个文件。

---

## 推荐工作流

1. **金融/交易任务** → 只用 Claude Code（我）
2. **品牌/设计任务** → 只用 Antigravity
3. **前端开发** → Antigravity 主导，我辅助
4. **系统架构** → 我主导，Antigravity 辅助

---

**下一步**：复制 `QUICK_ALIGN.md` 的内容，发给 Antigravity 试试看！
