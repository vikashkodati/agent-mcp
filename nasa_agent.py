from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from logging_utils import LoggingUtils
from typing import List


class NASAAgent:
    def __init__(self, mcp_servers: List[MCPServerStdio], verbose: bool = False):
        self.mcp_servers = mcp_servers
        self.verbose = verbose
        self.logger = LoggingUtils(verbose)

        self.agent = Agent(
            name="NASA Space Data Assistant",
            instructions="""You are an expert NASA space data assistant with access to comprehensive space exploration data. You can:

            1. **Astronomy Picture of the Day (APOD)**: Provide daily astronomical images with descriptions and scientific context
            2. **Mars Rover Data**: Access photos and mission data from Curiosity, Opportunity, Spirit, and Perseverance rovers
            3. **Near Earth Objects (NEO)**: Track asteroids and comets that come close to Earth, including hazard assessments
            4. **Earth Satellite Imagery**: Retrieve Earth observation data from various NASA satellites
            5. **Space Weather**: Monitor solar flares, coronal mass ejections, and space weather conditions
            6. **Exoplanet Data**: Access information about planets outside our solar system
            7. **NASA Image Library**: Search NASA's vast collection of space images and videos
            8. **Solar System Data**: Get information about planets, moons, and other solar system objects

            Available NASA tools:
            - nasa/apod: Get Astronomy Picture of the Day
            - nasa/mars-rover: Get Mars rover photos and data
            - nasa/neo: Search for Near Earth Objects
            - nasa/earth: Get Earth satellite imagery
            - nasa/exoplanet: Access exoplanet data
            - nasa/image-library: Search NASA's image collection
            - nasa/space-weather: Get space weather information

            Always provide scientifically accurate information with proper context. When showing images or data, explain the scientific significance and help users understand what they're seeing. If asked about space missions, include mission details and current status.
            
            Be enthusiastic about space exploration while maintaining scientific accuracy. Help users explore the wonders of our universe!
            """,
            mcp_servers=mcp_servers,
            model="gpt-4o",
        )

    async def find_answer(self, user_input: str):
        prompt = f"""User query: {user_input}
        
        Please help the user explore NASA's space data. Use the appropriate NASA tools to provide comprehensive, scientifically accurate information. Include images, data, and context when relevant."""

        self.logger.print_searching("NASA Space Data Assistant")

        result = Runner.run_streamed(
            starting_agent=self.agent, input=prompt, max_turns=10)

        await self.logger.stream_results(result)
        self.logger.print_complete() 