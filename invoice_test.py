import os

import telebot
from dotenv import load_dotenv
from telebot.types import LabeledPrice
from telebot.types import ShippingOption

load_dotenv()

token = os.getenv("MAIN_BOT_TOKEN")
provider_token = os.getenv("PROVIDER_YOOKASSA_TEST")
bot = telebot.TeleBot(token)

# More about Payments: https://core.telegram.org/bots/payments

prices = [
    LabeledPrice(label="Подписка на месяц", amount=300),
    LabeledPrice("Подписка на 3 месяца", 800 * 100),
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
def command_start(message):
    bot.send_message(
        message.chat.id,
        " Use /buy to order one, /terms for Terms and Conditions",
    )


@bot.message_handler(commands=["terms"])
def command_terms(message):
    bot.send_message(
        message.chat.id, "Thank you for shopping with our Autoposting bot!\n"
    )


@bot.message_handler(commands=["buy"])
def command_pay(message):
    bot.send_message(
        message.chat.id,
        "Real cards won't work with me, no money will be debited from your account."
        " Use this test card number to pay for sub: `4242 4242 4242 4242`"
        "\n\nThis is your demo invoice:",
        parse_mode="Markdown",
    )
    bot.send_invoice(
        message.chat.id,  # chat_id
        "Подписка на месяц",  # title
        "Подписка на месяц на связку",  # description
        "ПОдписка на месяц",  # invoice_payload
        provider_token,  # provider_token
        "RUB",  # currency
        prices,  # prices
        photo_url="http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg",
        photo_height=None,  # !=0/None or picture won't be shown
        photo_width=512,
        photo_size=512,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter="time-machine-example",
    )


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options,
        error_message="Oh, seems like our Dog couriers are having a lunch right now. Try again later!",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
        " try to pay again in a few minutes, we need a small rest.",
    )


@bot.message_handler(content_types=["successful_payment"])
def got_payment(message):
    bot.send_message(
        message.chat.id,
        "Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! "
        "Stay in touch.\n\nUse /buy again to get sub".format(
            message.successful_payment.total_amount / 100,
            message.successful_payment.currency,
        ),
        parse_mode="Markdown",
    )


bot.infinity_polling(skip_pending=True)
