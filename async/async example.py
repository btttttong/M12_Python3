import asyncio
import time

async def funct1():
    print('start function 1')
    await asyncio.sleep(3)
    print('end function 1')

async def funct2():
    print('start function 2')
    await asyncio.sleep(3)
    print('end function 2')

async def main():
    task1 = asyncio.create_task(funct1())
    task2 = asyncio.create_task(funct2())

    await task1
    await asyncio.sleep(2)
    print('delay stop')
    # await task2

if __name__ == "__main__":
    asyncio.run(main())


