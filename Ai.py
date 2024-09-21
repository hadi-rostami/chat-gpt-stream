from httpx import AsyncClient
from time import time
from json import loads
from asyncio import run


class AIBOT:

    URL = "https://chatgptdemo.info/chat/chat_api_stream"

    @classmethod
    async def stream_request(self, client: AsyncClient, data: dict, callback):
        async with client.stream("POST", AIBOT.URL, json=data) as response:
            if response.status_code == 200:
                text = ""
                async for line in response.aiter_lines():
                    if line:
                        line = loads(line.split("data: ")[1])
                        text += line["choices"][0]["delta"].get("content", "")
                        if callback:
                            await callback(text)

                return text
            else:
                return f"Failed with status code: {response.status_code}"

    @classmethod
    async def send_message(self, message: str, callback=None):
        async with AsyncClient(timeout=30) as client:
            data = {
                "question": message,
                "chat_id": "66eb28342da7a0793efbe444",
                "timestamp": time(),
            }

            return await AIBOT.stream_request(client, data, callback)


async def print_partial_text(text):
    print(text)


async def main():
    message = await AIBOT.send_message("امیر کبیر کی بود", callback=print_partial_text)

    print(f"متن نهایی: {message}")


run(main())
