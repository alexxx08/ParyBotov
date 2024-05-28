from aiogram import Bot, Dispatcher, types, executor
from neiro.text import get_response
from neiro.test import generate_image
from neiro.nastolki import get_responsee


bot = Bot(token= "6721535265:AAHLQtvS6r5m81ot7nLgF6isDyTRPATfk64")
dp = Dispatcher(bot)

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/start', description= 'Команда запуска бота'),
        types.BotCommand(command='/get_responsee', description='Cгенерировать настолку'),
        types.BotCommand(command='/generate_image', description='Сгенерировать изображение'),
        types.BotCommand(command='/get_response', description='Cгенерировать вопрос(промпт)'),
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands='start')
async def func_start(message: types.Message):
    await message.answer('Привет я твой нейросотрудник, который может помочь тебе с следующими задачами: Сгенерировать изображение(/generate_image: ), сгенерировать настолку(/get_responsee: ), сгенерировать вопрос(промпт)(/get_response: )')


@dp.message_handler(commands='get_responsee')
async def func_start(message: types.Message):
    text = message.get_args()
    print(text)
    respons = await get_responsee(text)
    await message.answer(respons)

@dp.message_handler(commands='generate_image')
async def func_start(message: types.Message):
    text = message.get_args()
    response_img = await get_response(message.text)
    await message.reply('Идет генерация, подождите')
    try:
        image_data = generate_image(response_img)
        await message.reply_photo(photo=image_data)
    except Exception as e:
        await message.reply(f'Произошла ошибка {e}')

@dp.message_handler(commands='get_response')
async def func_start(message: types.Message):
    text = message.get_args()
    response_text = await get_response(message.text)
    print(response_text)
    await message.reply(f"Промпт: {response_text}")


async def on_startup(dispatcher):
    await set_commands(dispatcher.bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True, on_startup= on_startup)