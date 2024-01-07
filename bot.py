from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, BaseFilter
from aiogram.types import Message
from config_data.config import load_config

BOT_TOKEN = '6615710993:AAH3zSDHg1ft2fksg2KTYPxtXn9aBGoCDas'
config = load_config('.env')

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()

admin_ids: list[int] = config.tg_bot.admin_ids

# Собственный фильтр, проверяющий юзера на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# Этот хэндлер будет срабатывать, если апдейт от админа
@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    await message.answer(text='Вы админ')


# Этот хэндлер будет срабатывать, если апдейт не от админа
@dp.message()
async def answer_if_not_admins_update(message: Message):
    print(f'{message=}')
    await message.answer(text='Вы не админ')


if __name__ == '__main__':
    dp.run_polling(bot)

