#!/usr/bin/env python3
"""
Orbital Mechanics MCP Server
Provides satellite tracking, ISS position, and orbital mechanics data
"""

import asyncio
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import httpx


class OrbitalMechanicsServer:
    def __init__(self):
        self.name = "Orbital Mechanics MCP Server"
        self.version = "1.0.0"
        
    async def get_iss_position(self) -> Dict[str, Any]:
        """Get current ISS position"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://api.open-notify.org/iss-now.json")
                data = response.json()
                
                return {
                    "success": True,
                    "timestamp": data.get("timestamp"),
                    "latitude": float(data["iss_position"]["latitude"]),
                    "longitude": float(data["iss_position"]["longitude"]),
                    "message": data.get("message", "success")
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_people_in_space(self) -> Dict[str, Any]:
        """Get list of people currently in space"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://api.open-notify.org/astros.json")
                data = response.json()
                
                return {
                    "success": True,
                    "number": data.get("number", 0),
                    "people": data.get("people", []),
                    "message": data.get("message", "success")
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_iss_pass_times(self, lat: float, lon: float, alt: float = 0) -> Dict[str, Any]:
        """Get ISS pass times for a given location"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"http://api.open-notify.org/iss-pass.json?lat={lat}&lon={lon}&alt={alt}"
                response = await client.get(url)
                data = response.json()
                
                return {
                    "success": True,
                    "passes": data.get("response", []),
                    "message": data.get("message", "success")
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_satellite_tle_data(self) -> Dict[str, Any]:
        """Get Two-Line Element (TLE) data for common satellites"""
        try:
            # Sample TLE data for demonstration
            tle_data = {
                "ISS": {
                    "name": "INTERNATIONAL SPACE STATION",
                    "line1": "1 25544U 98067A   21001.00000000  .00002182  00000-0  40864-4 0  9990",
                    "line2": "2 25544  51.6461 339.2971 0002829 197.4792 223.2975 15.48919103123456"
                },
                "HUBBLE": {
                    "name": "HUBBLE SPACE TELESCOPE",
                    "line1": "1 20580U 90037B   21001.00000000  .00000000  00000-0  00000+0 0  9990",
                    "line2": "2 20580  28.4690  80.8340 0002900 200.0000 160.0000 15.09300000000000"
                }
            }
            
            return {
                "success": True,
                "satellites": tle_data,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "note": "Sample TLE data - use real TLE service for accurate tracking"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def calculate_orbital_period(self, semi_major_axis: float) -> Dict[str, Any]:
        """Calculate orbital period using Kepler's Third Law"""
        try:
            # Earth's gravitational parameter (GM) in km³/s²
            GM_EARTH = 398600.4418
            
            # Convert semi-major axis from km to m for calculation
            a_meters = semi_major_axis * 1000
            
            # Calculate period using T = 2π * sqrt(a³/GM)
            import math
            period_seconds = 2 * math.pi * math.sqrt((a_meters ** 3) / (GM_EARTH * 1e9))
            period_minutes = period_seconds / 60
            period_hours = period_minutes / 60
            
            return {
                "success": True,
                "semi_major_axis_km": semi_major_axis,
                "orbital_period": {
                    "seconds": round(period_seconds, 2),
                    "minutes": round(period_minutes, 2),
                    "hours": round(period_hours, 2)
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        try:
            if method == "orbital/iss_position":
                return await self.get_iss_position()
            
            elif method == "orbital/people_in_space":
                return await self.get_people_in_space()
            
            elif method == "orbital/iss_pass_times":
                lat = params.get("latitude")
                lon = params.get("longitude") 
                alt = params.get("altitude", 0)
                
                if lat is None or lon is None:
                    return {"success": False, "error": "latitude and longitude are required"}
                
                return await self.get_iss_pass_times(float(lat), float(lon), float(alt))
            
            elif method == "orbital/satellite_tle":
                return await self.get_satellite_tle_data()
            
            elif method == "orbital/calculate_period":
                sma = params.get("semi_major_axis")
                if sma is None:
                    return {"success": False, "error": "semi_major_axis is required"}
                
                return await self.calculate_orbital_period(float(sma))
            
            else:
                return {"success": False, "error": f"Unknown method: {method}"}
                
        except Exception as e:
            return {"success": False, "error": f"Request handling error: {str(e)}"}


async def main():
    """Main MCP server loop"""
    server = OrbitalMechanicsServer()
    
    # MCP protocol implementation
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line.strip())
            method = request.get("method", "")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "1.0.0",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": server.name,
                            "version": server.version
                        }
                    }
                }
            
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "get_iss_position",
                                "description": "Get current position of the International Space Station",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "get_people_in_space", 
                                "description": "Get list of people currently in space",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "get_iss_pass_times",
                                "description": "Get ISS pass times for a location",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "latitude": {"type": "number"},
                                        "longitude": {"type": "number"},
                                        "altitude": {"type": "number"}
                                    },
                                    "required": ["latitude", "longitude"]
                                }
                            },
                            {
                                "name": "get_satellite_tle",
                                "description": "Get Two-Line Element data for satellites",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "calculate_orbital_period",
                                "description": "Calculate orbital period from semi-major axis",
                                "inputSchema": {
                                    "type": "object", 
                                    "properties": {
                                        "semi_major_axis": {"type": "number"}
                                    },
                                    "required": ["semi_major_axis"]
                                }
                            }
                        ]
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name", "")
                tool_params = params.get("arguments", {})
                
                # Map tool names to internal methods
                method_map = {
                    "get_iss_position": "orbital/iss_position",
                    "get_people_in_space": "orbital/people_in_space", 
                    "get_iss_pass_times": "orbital/iss_pass_times",
                    "get_satellite_tle": "orbital/satellite_tle",
                    "calculate_orbital_period": "orbital/calculate_period"
                }
                
                if tool_name in method_map:
                    result = await server.handle_request(method_map[tool_name], tool_params)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, indent=2)
                                }
                            ]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }
            
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0", 
                "id": request.get("id") if 'request' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main()) 