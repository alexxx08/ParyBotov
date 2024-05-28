import requests
import base64
import time
from random import randint
from aiogram import Dispatcher, Bot, types, executor
from neiro.text import get_response

API_KEY = '6721535265:AAHLQtvS6r5m81ot7nLgF6isDyTRPATfk64'
bot = Bot(token= API_KEY)
dp = Dispatcher(bot)

@dp.message_handler(commands = 'start')
async def func_start(message: types.Message):
    await message.answer('Привет, я твой шедеврум на минималках')

def generate_image(prompt_text):
    prompt = {
        "modelUri": "art://b1g3f13cj7d6d3ss2md9/yandex-art/latest",
        "generationOptions": {
          "seed": 17
        },
        "messages": [
          {
            "weight": 1,
            "text": prompt_text
          }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVNx1Vg9GnV7j4QMg3_HY9Su6Eu-qC6FkHOpRIL",
    }

    response = requests.post(url= url, headers= headers, json= prompt)
    result = response.json()
    print(result)

    operation_id = result['id']

    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = requests.get(operation_url, headers=headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
        else:
            time.sleep(5)


@dp.message_handler()
async def handler_message(message: types.Message):
    response_text = await get_response(message.text)
    print(response_text)
    await message.reply('Идёт генерация изображения, подождите')
    try:
        image_data = generate_image(response_text)
        await message.reply_photo(photo= image_data)
    except Exception as e:
        await message.reply(f'Произошла ошибка {e}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)