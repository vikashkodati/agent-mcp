import os
from agents.mcp import MCPServerSse, MCPServerStdio
from typing import Dict


class MCPConfig:
    def __init__(self):
        self.nasa_api_key = os.getenv("NASA_API_KEY")
        if not self.nasa_api_key:
            raise ValueError(
                "NASA_API_KEY environment variable is not set. Get your key from https://api.nasa.gov/")

        # Optional for some STAC services
        self.stac_api_key = os.getenv("STAC_API_KEY", "")

    def get_nasa_params(self):
        return {
            "command": "npx",
            "args": ["-y", "@programcomputer/nasa-mcp-server@latest"],
            "env": {"NASA_API_KEY": self.nasa_api_key}
        }

    def get_stac_params(self):
        return {
            "command": "npx",
            "args": ["-y", "stac-mcp-server@latest"],
            "env": {
                "STAC_API_KEY": self.stac_api_key if self.stac_api_key else ""
            }
        }

    def get_orbital_mechanics_params(self):
        return {
            "command": "python",
            "args": ["orbital_mechanics_server.py"],
            "env": {}
        }

    async def create_servers(self):
        nasa_server = MCPServerStdio(
            cache_tools_list=True,
            name="NASA MCP Server",
            params=self.get_nasa_params(),
        )

        stac_server = MCPServerStdio(
            cache_tools_list=True,
            name="STAC MCP Server", 
            params=self.get_stac_params(),
        )

        orbital_server = MCPServerStdio(
            cache_tools_list=True,
            name="Orbital Mechanics MCP Server",
            params=self.get_orbital_mechanics_params(),
        )

        return {
            "nasa": nasa_server,
            "stac": stac_server,
            "orbital": orbital_server
        }
