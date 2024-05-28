import requests
from aiogram import Bot, Dispatcher, types, executor


API_TOKEN = '6721535265:AAHLQtvS6r5m81ot7nLgF6isDyTRPATfk64'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
  await message.reply('Привет, я нейроконсультант, который поможет выбрать идеальную настольную игру. Напиши сколько игроков будет, на какое примерное время игры, предпочительный жанр. Если вы не знаете с чего начать, то напишите Рекомендации')

async def get_responsee(message_text):
  prompt ={
    "modelUri": "gpt://b1go1t8vie998tqjdjhu/yandexgpt-lite",
    "completionOptions": {
      "stream": False,
      "temperature": 0.5,
      "maxTokens": "2000"
    },
    "messages": [
      {
        "role": "system",
        "text": "Ты — специалист по настольным играм. Твоя задача — разобраться, какая настольная игра подходит для данного человека, в зависимости от его ответа по количеству игроков, времени и жанрам. Кратко опиши данные игры, примерное их время"
      },
      {
        "role": "user",
        "text": message_text
      }
    ]
  }

  url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-key AQVNxZaGfTtvm3Wg5sKqytyNy5PMlr0GGDfNMzgJ"
  }

  response = requests.post(url, headers = headers, json=prompt)
  result = response.json()
  return result['result']['alternatives'][0]['message']['text']

@dp.message_handler()
async def analize_message(message:types.Message):
  response_text = await get_responsee((message.text))
  await message.answer(response_text)

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)