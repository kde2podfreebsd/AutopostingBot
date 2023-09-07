import asyncio
import os

import telebot
from dotenv import load_dotenv
from telebot.types import LabeledPrice
from telebot.types import ShippingOption
from telebot.async_telebot import AsyncTeleBot
import telebot

load_dotenv()

token = os.getenv("MAIN_BOT_TOKEN")
provider_token = os.getenv("PROVIDER_YOOKASSA_TEST")
bot = AsyncTeleBot(token)

# More about Payments: https://core.telegram.org/bots/payments

prices = [
    LabeledPrice(label="Подписка на месяц", amount=500 * 100)
]

shipping_options = [
    ShippingOption(id="instant", title="Подписка на месяц").add_price(
        LabeledPrice("Teleporter", 300 * 100)
    ),
    ShippingOption(id="pickup", title="Подписка на 3 месяца").add_price(
        LabeledPrice("Pickup", 800 * 100)
    ),
]


@bot.message_handler(commands=["start"])
async def command_start(message):
    await bot.send_message(
        message.chat.id,
        " Use /buy to order one, /terms for Terms and Conditions",
    )


@bot.message_handler(commands=["terms"])
async def command_terms(message):
    await bot.send_message(
        message.chat.id, "Thank you for shopping with our Autoposting bot!\n"
    )


@bot.message_handler(commands=["buy"])
async def command_pay(message):
    await bot.send_message(
        message.chat.id,
        "🔗 Спасибо за выбор нашего сервиса! Для оплаты выбранной подписки, поспользуйтесь встроенным эквайрингом Yookassa. После успешной оплаты ваша подписка будет автоматически активирована.",
        parse_mode="Markdown",
    )
    await bot.send_invoice(
        message.chat.id,  # chat_id
        "Подписка на месяц",  # title
        "Подписка на месяц на связку",  # description
        "Подписка на месяц",  # invoice_payload
        provider_token,  # provider_token
        "RUB",  # currency
        prices
    )


@bot.shipping_query_handler(func=lambda query: True)
async def shipping(shipping_query):
    print(shipping_query)
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options,
        error_message="Ошибка, попробуйте позже или напишите в тех поддержку",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
async def checkout(pre_checkout_query):
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="Что-то случилось на стороне эквайринга, попробуйте позже или напишите в тех поддержку",
    )


@bot.message_handler(content_types=["text"])
async def HandlerTextMiddleware(message):
    if message.text == "kek":
        print("kek")


@bot.message_handler(content_types=["successful_payment"])
async def got_payment(message):

    await bot.send_message(
        message.chat.id,
        f'''
✅ Ваша оплата успешно прошла! Спасибо за покупку подписки/подписок на сумму {message.successful_payment.total_amount / 100} {message.successful_payment.currency}. Ваша подписка теперь активна и вы можете продолжить использовать нашего бота для парсинга и постинга контента.

🔗 Теперь вы можете создать новую связку. Для этого перейдите в главное меню и выберите 'Добавить новую связку'. Вы сможете выбрать источник контента, канал для постинга, тип парсинга и время постинга.

Если у вас возникнут вопросы или проблемы, не стесняйтесь обращаться к нам.        
'''
    )


async def polling():
    task1 = asyncio.create_task(bot.infinity_polling())
    await task1


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(polling())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()