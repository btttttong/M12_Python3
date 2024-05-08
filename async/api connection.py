import asyncio
import time
from aiohttp import ClientSession

API_URL = f"https://api.openweathermap.org/data/2.5/weather"

cities = ["Bangkok", "Seoul"]


async def get_weather(city):
    async with ClientSession() as session:
        params = {"q": city, "appid": "8ebef75da796ef43be8115869e834322"}
        async with session.get(API_URL, params=params) as response:
            weather = await response.json()

    return f"{city}: {weather['main']['temp'] } , temp: {weather['main']['temp'] - 273:2.1f}C"


async def main(cities):
    tasks = []
    for city in cities:
        tasks.append(asyncio.create_task(get_weather(city)))
    print(time.strftime("%X"))
    for task in tasks:
        await task
        print(task.result())
    print(time.strftime("%X"))


asyncio.run(main(cities))
