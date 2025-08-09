from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
import requests
from dice_roller import DiceRoller

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

"""
Add your own tool here, and then use it through Cursor!
"""
@mcp.tool()
def check_weather(location: str) -> str:
    """Check the weather for a given location using OpenWeatherMap API"""
    try:
        # OpenWeatherMap API endpoint (free tier)
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error: OPENWEATHER_API_KEY not found in environment variables. Please set it up first."
        
        # Get weather data
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # Use Celsius
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather information
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        # Create a simple recommendation
        if temp > 20 and "rain" not in description.lower():
            recommendation = "The weather looks great! You should go outside and enjoy the sun!"
        elif temp < 10:
            recommendation = "It's quite cold outside. Maybe stay in and keep working!"
        else:
            recommendation = "The weather is moderate. It's up to you whether to go out or stay in!"
        
        return f"Weather in {location}: {temp}°C, {description}. Humidity: {humidity}%, Wind: {wind_speed} m/s. {recommendation}"
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except KeyError as e:
        return f"Error parsing weather data: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
