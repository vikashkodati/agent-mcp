# Space Domain Agent Platform

An AI-powered platform featuring three specialized space domain agents built with OpenAI Agents SDK and Model Context Protocol (MCP) servers. Explore NASA's vast space data, analyze Earth observation imagery, and perform orbital mechanics calculations.

## What This Is

This project demonstrates how to build AI agents that integrate with space domain services through MCP servers. It features:

- **NASA Space Data Agent**: Access NASA's comprehensive space exploration and astronomy data
- **STAC Earth Observation Agent**: Analyze satellite imagery and Earth observation data
- **Orbital Mechanics Agent**: Track satellites and perform orbital calculations
- **Interactive CLI**: Rich terminal interface with clickable links and real-time streaming
- **MCP Integration**: Connects to NASA, STAC, and Orbital Mechanics MCP servers

## Required API Keys

To run this project, you'll need:

1. **OpenAI API Key** - For the AI agents (GPT-4o)
   - Sign up at: https://platform.openai.com/
   - Get your API key from: https://platform.openai.com/api-keys

2. **NASA API Key** - For accessing NASA's vast data repositories
   - Sign up at: https://api.nasa.gov/
   - Get your API key instantly from the NASA API portal

3. **STAC API Key** - Optional for some STAC services
   - Required for certain Earth observation data providers

## Setup Instructions

1. **Clone and navigate to the project**:
   ```bash
   cd /path/to/agent-mcp
   ```

2. **Create environment file**:
   ```bash
   # Create .env file with your API keys
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "NASA_API_KEY=your_nasa_api_key_here" >> .env
   echo "STAC_API_KEY=your_stac_api_key_here" >> .env
   echo "VERBOSE=false" >> .env
   ```

3. **Install dependencies using uv**:
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install project dependencies
   uv sync
   ```

4. **Run the application**:
   ```bash
   # Run with uv
   uv run main.py
   
   # Or with verbose logging for debugging
   VERBOSE=true uv run main.py
   ```

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                  Space Domain Agent Platform                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐                       │
│  │   User Input    │    │  Interactive    │                       │
│  │  (Terminal UI)  │◄──►│  CLI Handler    │                       │
│  └─────────────────┘    └─────────────────┘                       │
│           │                       │                                │
│           ▼                       ▼                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                Agent Router                                 │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │   │
│  │  │ NASA Agent  │ │ STAC Agent  │ │ Orbital Mechanics   │   │   │
│  │  │ (Space Data)│ │ (Earth Obs) │ │ Agent (Satellites)  │   │   │
│  │  │ (GPT-4o)    │ │ (GPT-4o)    │ │ (GPT-4o)           │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘   │
│  └─────────────────────────────────────────────────────────────┘   │
│           │                │                      │                │
│           ▼                ▼                      ▼                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MCP Layer                                │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │   │
│  │  │ NASA MCP    │ │ STAC MCP    │ │ Orbital Mechanics   │   │   │
│  │  │ Server      │ │ Server      │ │ MCP Server          │   │   │
│  │  │ (Space Data)│ │ (Satellite  │ │ (ISS/Satellite      │   │   │
│  │  │             │ │  Imagery)   │ │  Tracking)          │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│           │                │                      │                │
│           ▼                ▼                      ▼                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              External Services                              │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │   │
│  │  │ NASA APIs   │ │ STAC        │ │ Open Notify API     │   │   │
│  │  │ • APOD      │ │ • Landsat   │ │ • ISS Position      │   │   │
│  │  │ • Mars Rover│ │ • Sentinel  │ │ • Astronauts        │   │   │
│  │  │ • NEO       │ │ • MODIS     │ │ • Pass Times        │   │   │
│  │  │ • Exoplanets│ │ • Planet    │ │ • TLE Data          │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

Flow:
1. User selects space domain agent via interactive menu
2. Agent processes user query using OpenAI GPT-4o
3. Agent calls appropriate MCP server for space domain data
4. MCP server fetches data from space APIs and services
5. Results stream back through Rich terminal interface
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `NASA_API_KEY`: Your NASA API key for space data access (required)
- `STAC_API_KEY`: Your STAC API key for Earth observation data (optional)
- `VERBOSE`: Set to "true" for detailed logging (optional, defaults to false)

## How It Works

### NASA Space Data Agent
1. User asks about space exploration, astronomy, or planetary science
2. Agent accesses NASA's comprehensive data including:
   - Astronomy Picture of the Day (APOD)
   - Mars rover photos and mission data
   - Near Earth Objects (NEO) tracking
   - Earth satellite imagery
   - Space weather monitoring
   - Exoplanet discoveries
   - NASA's image and video library

### STAC Earth Observation Agent
1. User requests satellite imagery or Earth observation data
2. Agent searches through STAC catalogs including:
   - Landsat 8/9 multispectral imagery
   - Sentinel-1/2 radar and optical data
   - MODIS global monitoring data
   - Commercial satellite imagery
   - Climate and environmental monitoring

### Orbital Mechanics Agent
1. User asks about satellites, orbital mechanics, or space operations
2. Agent provides real-time tracking and calculations:
   - Current ISS position and crew information
   - ISS pass times for any location
   - Satellite tracking with TLE data
   - Orbital period calculations
   - Mission planning assistance

## Project Structure

```
├── main.py                   # Main entry point with interactive CLI
├── nasa_agent.py             # NASA Space Data Agent implementation
├── stac_agent.py             # STAC Earth Observation Agent implementation
├── orbital_agent.py          # Orbital Mechanics Agent implementation
├── orbital_mechanics_server.py # Custom orbital mechanics MCP server
├── mcp_config.py             # MCP server configuration and connections
├── logging_utils.py          # Rich console output and streaming utilities
├── pyproject.toml            # Project dependencies and configuration
└── .env                      # Environment variables (create this file)
```

## Terminal Features

### Clickable Links
URLs in the output will be clickable in supported terminals:
- **macOS**: iTerm2, Hyper, Kitty, WezTerm
- **Windows**: Windows Terminal, ConEmu
- **Linux**: GNOME Terminal (3.26+), Konsole, Tilix
- **Cross-platform**: VS Code integrated terminal, JetBrains IDEs terminal

### Rich Interface
- Interactive arrow-key navigation
- Real-time streaming responses
- Colored output with progress indicators
- Tool call visibility in verbose mode

## Space Domain Capabilities

### 🚀 NASA Data Access
- **Astronomical Data**: Daily astronomy pictures, solar system imagery
- **Mars Exploration**: Rover photos, mission updates, geological data
- **Earth Science**: Climate data, weather monitoring, environmental tracking
- **Space Weather**: Solar flares, magnetic storms, radiation levels
- **Exoplanets**: Confirmed discoveries, habitability assessments
- **Deep Space**: Hubble imagery, galaxy observations, cosmic phenomena

### 🌍 Earth Observation
- **Land Use Analysis**: Deforestation tracking, urban development
- **Climate Monitoring**: Ice coverage, vegetation health, temperature trends
- **Disaster Response**: Flood mapping, wildfire tracking, damage assessment
- **Agriculture**: Crop monitoring, yield prediction, irrigation analysis
- **Ocean Monitoring**: Sea ice extent, water quality, coastal changes

### 🛰️ Orbital Mechanics
- **Real-time Tracking**: ISS position, satellite locations
- **Pass Predictions**: Visibility calculations for any location
- **Orbital Analysis**: Period calculations, mission planning
- **Space Operations**: Launch windows, rendezvous planning
- **Educational**: Kepler's laws, orbital elements explanation

## Dependencies

- `openai-agents`: OpenAI Agents SDK for AI agent functionality
- `python-dotenv`: Environment variable management
- `rich`: Enhanced terminal output and UI components
- `httpx`: HTTP client for API requests
- `asyncio`: Asynchronous programming support (built-in)

## Troubleshooting

1. **Missing API Keys**: Ensure both OpenAI and NASA API keys are set in `.env`
2. **Connection Issues**: Check your internet connection and API key validity
3. **Terminal Issues**: Use a supported terminal for the best experience
4. **Verbose Mode**: Set `VERBOSE=true` to see detailed operation logs
5. **MCP Server Issues**: Check if npx and Python are installed and accessible

## Getting Started Examples

### NASA Agent Examples:
- "Show me today's astronomy picture"
- "Find Mars rover photos from Curiosity"
- "What near-Earth asteroids are approaching?"
- "Show me Earth from space"

### STAC Agent Examples:
- "Find Landsat imagery of the Amazon rainforest"
- "Show deforestation changes over time"
- "Get Sentinel-2 data for crop monitoring"
- "Find satellite images of Hurricane damage"

### Orbital Mechanics Examples:
- "Where is the ISS right now?"
- "When will the ISS pass over New York?"
- "Who is currently in space?"
- "Calculate orbital period for a 400km altitude"

Explore the cosmos with AI-powered space domain intelligence! 🚀🌌