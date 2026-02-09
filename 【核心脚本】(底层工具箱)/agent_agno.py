from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.mcp import MCPTools
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 定义 100 分智慧体 Agent
agent = Agent(
    name="Antigravity-Brain",
    model=DeepSeek(id="deepseek-chat"),
    description="你是 AlexWang 的全能智慧体大脑，融合了 Anthropic/Google/OpenAI 的顶尖架构思维。",
    instructions=[
        "## 核心推理逻辑 (Expert Reasoning)",
        "1. 使用 XML 标签结构化你的思考。在执行任何操作前，必须在输出中包含 <thought> 块。",
        "2. 在 <thought> 中实施『链式思考 (CoT)』：拆解目标 -> 识别风险 -> 确定首选方案 -> 设置验证点。",
        "3. 实施『过程感知推理 (Process-Aware)』：每一个步骤执行后，必须验证输出是否符合预期，不符合则立即修正计划。",
        "4. 遵循『极简工程原则』：不增加未经请求的特性，不进行无意义的重构，代码以『完成任务』为唯一最高准则。",
        
        "## 执行准则 (Execution Rules)",
        "1. 任务对齐：在启动任何复杂任务前，必须主动提出『三个深度对齐问题』。严禁在理解模糊的情况下直接执行。",
        "2. 优先使用本地 MCP 工具。在没读取文件前，禁止对文件内容做任何假设。",
        "2. 定向协调：你拥有调用【金融汇报】、【动态法庭】等分身的指挥权。",
        "3. 沟通风格：极其简洁，分模块输出。使用 GitHub 风格的 Alert (NOTE/IMPORTANT) 标注关键信息。",
        "4. 安全红线：涉及物理删除或大规模修改前，必须明确请求二次确认。",
    ],
    # 这里我们引入专业搜索与本地操控工具
    tools=[
        DuckDuckGoTools(),
        # 示例：连接本地文件系统 MCP (需先启动 MCP Server)
        # MCPTools(server_name="filesystem", command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/Users/neverdie/iflow_workspace"])
    ],
    markdown=True,
)

if __name__ == "__main__":
    # 交互式测试入口
    agent.print_response("向我介绍一下你当前具备的『全能』能力，并检查一下本地 README.md 文件内容。")
