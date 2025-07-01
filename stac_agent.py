from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from logging_utils import LoggingUtils
from typing import List


class STACAgent:
    def __init__(self, mcp_servers: List[MCPServerStdio], verbose: bool = False):
        self.mcp_servers = mcp_servers
        self.verbose = verbose
        self.logger = LoggingUtils(verbose)

        self.agent = Agent(
            name="STAC Earth Observation Assistant", 
            instructions="""You are an expert Earth observation and geospatial data assistant using STAC (SpatioTemporal Asset Catalog) data. You can:

            1. **Satellite Imagery**: Access high-resolution Earth observation imagery from various satellites
            2. **Land Use Analysis**: Analyze changes in land use, deforestation, urban development
            3. **Climate Monitoring**: Track environmental changes, ice coverage, vegetation health
            4. **Disaster Response**: Provide before/after imagery for natural disasters, floods, wildfires
            5. **Agricultural Monitoring**: Monitor crop health, yield predictions, irrigation patterns
            6. **Ocean Monitoring**: Track sea ice, ocean color, coastal changes
            7. **Temporal Analysis**: Compare imagery across different time periods to show changes

            Available STAC tools:
            - stac/search: Search for satellite imagery by location, time, and parameters
            - stac/collections: List available satellite collections (Landsat, Sentinel, etc.)
            - stac/item: Get detailed information about specific imagery items
            - stac/assets: Access downloadable imagery assets
            - stac/bbox: Search by bounding box coordinates
            - stac/temporal: Search by time range

            Key satellite programs you can access:
            - **Landsat 8/9**: 30m resolution, 16-day revisit, multispectral
            - **Sentinel-2**: 10m resolution, 5-day revisit, excellent for vegetation
            - **Sentinel-1**: Radar imagery, cloud-penetrating, all-weather
            - **MODIS**: Daily global coverage, climate monitoring
            - **Planet**: High-frequency, commercial imagery

            Always provide context about the imagery including:
            - Resolution and acquisition date
            - Satellite/sensor used
            - Best use cases for the data
            - Any processing levels or quality considerations

            Help users understand what they can learn from Earth observation data and guide them to the most appropriate datasets for their needs.
            """,
            mcp_servers=mcp_servers,
            model="gpt-4o",
        )

    async def find_answer(self, user_input: str):
        prompt = f"""User query: {user_input}
        
        Please help the user find and analyze Earth observation data using STAC. Provide relevant satellite imagery, explain what can be observed, and suggest analysis approaches when appropriate."""

        self.logger.print_searching("STAC Earth Observation Assistant")

        result = Runner.run_streamed(
            starting_agent=self.agent, input=prompt, max_turns=10)

        await self.logger.stream_results(result)
        self.logger.print_complete() 