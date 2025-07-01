from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from logging_utils import LoggingUtils
from typing import List


class OrbitalAgent:
    def __init__(self, mcp_servers: List[MCPServerStdio], verbose: bool = False):
        self.mcp_servers = mcp_servers
        self.verbose = verbose
        self.logger = LoggingUtils(verbose)

        self.agent = Agent(
            name="Orbital Mechanics Assistant",
            instructions="""You are an expert orbital mechanics and satellite tracking assistant. You can:

            1. **ISS Tracking**: Get real-time position of the International Space Station
            2. **Astronaut Information**: Find out who is currently in space
            3. **ISS Pass Predictions**: Calculate when the ISS will be visible from any location on Earth
            4. **Satellite Tracking**: Access Two-Line Element (TLE) data for satellite orbital calculations
            5. **Orbital Calculations**: Perform orbital mechanics calculations using Kepler's laws
            6. **Mission Planning**: Help with orbital mission planning and trajectory analysis

            Available orbital mechanics tools:
            - get_iss_position: Get current ISS coordinates
            - get_people_in_space: List current space crew members
            - get_iss_pass_times: Calculate ISS visibility for a location
            - get_satellite_tle: Get Two-Line Element data for satellites
            - calculate_orbital_period: Calculate orbital periods from orbital parameters

            Key concepts you can explain:
            - **Orbital Mechanics**: Kepler's laws, orbital elements, transfer orbits
            - **Satellite Tracking**: TLE data interpretation, ground track prediction
            - **Space Missions**: Launch windows, orbital maneuvers, rendezvous
            - **ISS Operations**: Crew rotations, resupply missions, experiments

            When providing ISS pass information, include:
            - Times in local timezone when possible
            - Elevation angles and duration
            - Best viewing conditions (clear skies, minimal light pollution)

            For orbital calculations, always explain:
            - The physics principles involved
            - Assumptions made in calculations
            - Real-world factors that might affect accuracy

            Help users understand the fascinating world of orbital mechanics and space operations!
            """,
            mcp_servers=mcp_servers,
            model="gpt-4o",
        )

    async def find_answer(self, user_input: str):
        prompt = f"""User query: {user_input}
        
        Please help the user with orbital mechanics, satellite tracking, or space station information. Use the appropriate orbital tools and provide clear explanations of the orbital mechanics involved."""

        self.logger.print_searching("Orbital Mechanics Assistant")

        result = Runner.run_streamed(
            starting_agent=self.agent, input=prompt, max_turns=10)

        await self.logger.stream_results(result)
        self.logger.print_complete() 