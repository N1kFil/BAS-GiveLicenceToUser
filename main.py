import secrets
import aiohttp
import asyncio
import string
from config import COOKIES_BAS, script_name

alphabet = string.ascii_letters + string.digits


async def create_bas_user(cookies: dict):
    async with aiohttp.ClientSession() as session:
        acc_name = ''.join(secrets.choice(alphabet) for _ in range(12))
        acc_password = ''.join(secrets.choice(alphabet) for _ in range(12))
        async with session.post("https://bablosoft.com/bas/users/createuser", json={"username": acc_name, "password": acc_password}, cookies=cookies) as resp:
            bas_answer = await resp.json()
            if bas_answer["success"] == "true":
                return acc_name, acc_password
            else:
                raise Exception(bas_answer)


async def give_licence_to_user(acc_name: str, script_name: str, col_days: int, col_mashines: int, cookies: dict) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post("https://bablosoft.com/bas/users/create", json={
            "user": acc_name,
            "script": script_name,
            "machines": col_mashines,
            "duration": str(col_days),
            "is_duration": True,
            "expire": 99999
        }, cookies=cookies) as resp:
            bas_answer = await resp.json()
            if bas_answer["success"] == "true":
                return True
            else:
                raise Exception(bas_answer)


async def main():
    acc_name, acc_password = await create_bas_user(COOKIES_BAS)
    print(f"Create user {acc_name}:{acc_password}")

    bas_status = await give_licence_to_user(acc_name, script_name=script_name, col_days=33, col_mashines=11, cookies=COOKIES_BAS)
    if bas_status:
        print(f"Give licence - {acc_name} Script - {script_name}")


asyncio.run(main())
