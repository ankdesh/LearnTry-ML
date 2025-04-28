from fastmcp import Client
# Removed duplicate import
from fastmcp.client.transports import (
    SSETransport,
    PythonStdioTransport, # Note: These are imported but not used in this example
    FastMCPTransport    # Note: These are imported but not used in this example
)
import asyncio


async def asd():
    print("Attempting to connect to server...")
    try:
        # Use async with for proper resource management
        async with Client(SSETransport("http://127.0.0.1:8000/sse")) as client:
            print("Connected. Listing tools...")
            # List available tools
            tools = await client.list_tools()
            print("Available tools:", tools)
            # Example: Call the 'add' tool
            if "add" in tools:
                 print("Calling add(5, 3)...")
                 result = await client.call("add", a=5, b=3)
                 print("Result of add(5, 3):", result)
            else:
                 print("'add' tool not found.")

    except ConnectionRefusedError:
        print("Connection Error: Could not connect to the server.")
        print("Please ensure the server (fastmcp_server.py) is running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(asd())
