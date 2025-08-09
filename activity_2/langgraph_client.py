# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

import os
from dotenv import load_dotenv
load_dotenv()


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/brandi/student/ai_makerspace/AIE7-MCP-Session/server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent("openai:gpt-4.1", tools)
            agent_response = await agent.ainvoke({"messages": "what's the weather in Brest, France?"})
            
            # Extract just the text from the last message
            if agent_response and "messages" in agent_response:
                last_message = agent_response["messages"][-1]
                text_response = last_message.content
                print("Agent Response Text:")
                print(text_response)
            else:
                print("No messages found in response")
            
            # You can also access the raw response if needed
            print("\nRaw Response Structure:")
            print(agent_response)

if __name__ == "__main__":
    asyncio.run(main())