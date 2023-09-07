import asyncio
from datetime import datetime
from typing import List

from telebot import types
import telebot

from Bot.Config import bot, invoice_factory, provider_token
from Bot.Config import message_context_manager
from Bot.Handlers.mainMenuHandler import _mainMenu
from Bot.Markups.markupBuilder import MarkupBuilder
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.types import LabeledPrice
from telebot.types import ShippingOption

from DataBase.DataAccessLayer.ChainDAL import ChainDAL
from DataBase.session import async_session
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor()


async def run_blocking(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args, **kwargs)


class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    async def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class ChainPrices(object):
    _chain30prices = None | List[LabeledPrice]

    @classmethod
    def chain30prices(cls):
        cls._chain30prices = [LabeledPrice(label="Подписка на 30 дней", amount=500 * 100)]
        return cls._chain30prices

    @classmethod
    def chain90prices(cls):
        cls._chain30prices = [LabeledPrice(label="Подписка на 90 дней", amount=1200 * 100)]
        return cls._chain30prices

    @classmethod
    def chain180prices(cls):
        cls._chain30prices = [LabeledPrice(label="Подписка на 180 дней", amount=2100 * 100)]
        return cls._chain30prices

    @classmethod
    def allChains30prices(cls, chains_count:int):
        cls._chain30prices = [LabeledPrice(label="Подписка на 30 дней", amount=500 * 100 * chains_count)]
        return cls._chain30prices

    @classmethod
    def allChains90prices(cls, chains_count: int):
        cls._chain30prices = [LabeledPrice(label="Подписка на 90 дней", amount=1200 * 100 * chains_count)]
        return cls._chain30prices

    @classmethod
    def allChains180prices(cls, chains_count: int):
        cls._chain30prices = [LabeledPrice(label="Подписка на 180 дней", amount=2100 * 100 * chains_count)]
        return cls._chain30prices


async def _invoiceMenu(message):
    msg_to_del = await bot.send_message(
        message.chat.id,
        "⚙️",
        reply_markup=MarkupBuilder.hide_menu,
        parse_mode="MarkdownV2",
    )

    await bot.delete_message(
        chat_id=message.chat.id, message_id=msg_to_del.message_id, timeout=0
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.invoice_menu_text,
        reply_markup=await MarkupBuilder.invoice_menu(chat_id=message.chat.id),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


async def _sub_status(message):
    msg_to_del = await bot.send_message(
        message.chat.id,
        "⚙️",
        reply_markup=MarkupBuilder.hide_menu,
        parse_mode="MarkdownV2",
    )

    await bot.delete_message(
        chat_id=message.chat.id, message_id=msg_to_del.message_id, timeout=0
    )

    async def getChainsByChatId():
        async with async_session() as session:
            chain_dal = ChainDAL(session)
            active_chains_count = await chain_dal.countActiveChainsByChatId(message.chat.id)
            user_chains = await chain_dal.getChainsByChatId(message.chat.id)
            text = f"<b>На данный момент у вас активно {active_chains_count} подпис-(ка)/(ки)/(ок).</b>\n📝 Вот информация о ваших текущих подписках:\n"
            for chain in user_chains:
                sources = ''
                i = 0
                for url in chain[0].source_urls:
                    i += 1
                    sources += f'\n{i}. {url["source_type"]}: {url["url"]}'
                text += f'''
🆔 ID: {chain[0].chain_id}
🎯 Целевой канал: {chain[0].target_channel}
ℹ️ Истоичники парсинга: {sources}
⏰ Время постинга: {"".join(map(lambda x: x, chain[0].parsing_time))}
📅 Активно до: {chain[0].active_due_date.replace(second=0, microsecond=0)}
-------------------------------------------
'''
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=MarkupBuilder.back_to_invoice_menu(),
                parse_mode="html"
            )

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )

    await asyncio.gather(getChainsByChatId())


@bot.callback_query_handler(func=None, config=invoice_factory.filter())
async def chainsInvoice_callback(call: types.CallbackQuery):

    callback_data: dict = invoice_factory.parse(callback_data=call.data)
    chainInvoice_id = callback_data['product_id']

    print(chainInvoice_id)

    if "payall" in chainInvoice_id:

        callback = chainInvoice_id.split("#")

        async with async_session() as session:
            chain_dal = ChainDAL(session)
            user_chains = await chain_dal.getChainsByChatId(call.message.chat.id)

        if len(user_chains) == 0:
            msg = await bot.send_message(call.message.chat.id, "У вас нет добавленных связок!",
                                         reply_markup=MarkupBuilder.back_to_invoice_menu())

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=call.message.chat.id, msgId=msg.message_id
            )
        else:
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=MarkupBuilder.payChainMenuText,
                reply_markup=MarkupBuilder.chainPayAllPricingMenu(chat_id=callback[1], chains_count=len(user_chains)),
                parse_mode="html"
            )
    else:
        chainInvoice_id = int(callback_data['product_id'])
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=MarkupBuilder.payChainMenuText,
            reply_markup=MarkupBuilder.chainPricingMenu(chain_id=chainInvoice_id),
            parse_mode="html"
        )


async def _chainPayment(message, callback_data):

    await bot.send_message(
        message.chat.id,
        "🔗 Спасибо за выбор нашего сервиса! Для оплаты выбранной подписки, поспользуйтесь встроенным эквайрингом Yookassa. После успешной оплаты ваша подписка будет автоматически активирована.",
        parse_mode="Markdown",
    )

    if int(callback_data[2]) == 30:
        await bot.send_invoice(
            message.chat.id,
            f"Подписка на {callback_data[2]} дней",  # title
            f"Подписка на {callback_data[2]} дней на связку id_{callback_data[1]}. Пользователь: {message.chat.username}",  # description
            f"30#{callback_data[1]}",  # invoice_payload
            provider_token,  # provider_token
            "RUB",  # currency
            ChainPrices.chain30prices(),  # prices
        )

    if int(callback_data[2]) == 90:
        await bot.send_invoice(
            message.chat.id,
            f"Подписка на {callback_data[2]} дней",  # title
            f"Подписка на {callback_data[2]} дней на связку id_{callback_data[1]}. Пользователь: {message.chat.username}",  # description
            f"90#{callback_data[1]}",  # invoice_payload
            provider_token,  # provider_token
            "RUB",  # currency
            ChainPrices.chain90prices(),  # prices
        )

    if int(callback_data[2]) == 180:
        await bot.send_invoice(
            message.chat.id,
            f"Подписка на {callback_data[2]} дней",  # title
            f"Подписка на {callback_data[2]} дней на связку id_{callback_data[1]}. Пользователь: {message.chat.username}",  # description
            f"180#{callback_data[1]}",  # invoice_payload
            provider_token,  # provider_token
            "RUB",  # currency
            ChainPrices.chain180prices(),  # prices
        )


async def _chainAllPayment(message, callback_data):
    async with async_session() as session:
        chain_dal = ChainDAL(session)
        user_chains = await chain_dal.getChainsByChatId(message.chat.id)
        if len(user_chains) == 0:

            msg = await bot.send_message(message.chat.id, "У вас нет добавленных связок!", reply_markup=MarkupBuilder.back_to_invoice_menu())

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )

        else:
            await bot.send_message(
                message.chat.id,
                "🔗 Спасибо за выбор нашего сервиса! Для оплаты всех ваших выбранных подписок, поспользуйтесь встроенным эквайрингом Yookassa. После успешной оплаты ваши подписки будет автоматически продлены активирована.",
                parse_mode="Markdown",
            )

            if int(callback_data[2]) == 30:
                await bot.send_invoice(
                    message.chat.id,
                    f"Подписка на {callback_data[2]} дней",  # title
                    f"Подписка на {callback_data[2]} дней на все связки. Пользователь: {message.chat.username}",
                    # description
                    f"payall#30#{callback_data[1]}",  # invoice_payload
                    provider_token,  # provider_token
                    "RUB",  # currency
                    ChainPrices.allChains30prices(chains_count=len(user_chains)),  # prices
                )

            if int(callback_data[2]) == 90:
                await bot.send_invoice(
                    message.chat.id,
                    f"Подписка на {callback_data[2]} дней",  # title
                    f"Подписка на {callback_data[2]} дней на все связки. Пользователь: {message.chat.username}",
                    # description
                    f"payall#90#{callback_data[1]}",  # invoice_payload
                    provider_token,  # provider_token
                    "RUB",  # currency
                    ChainPrices.allChains90prices(chains_count=len(user_chains)),  # prices
                )

            if int(callback_data[2]) == 180:
                await bot.send_invoice(
                    message.chat.id,
                    f"Подписка на {callback_data[2]} дней",  # title
                    f"Подписка на {callback_data[2]} дней на все связки. Пользователь: {message.chat.username}",
                    # description
                    f"payall#180#{callback_data[1]}",  # invoice_payload
                    provider_token,  # provider_token
                    "RUB",  # currency
                    ChainPrices.allChains180prices(chains_count=len(user_chains)),  # prices
                )


@bot.shipping_query_handler(func=lambda query: True)
async def shipping(shipping_query):
    print(shipping_query)
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        error_message="Ошибка, попробуйте позже или напишите в тех поддержку",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
async def checkout(pre_checkout_query):
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="Что-то случилось на стороне эквайринга, попробуйте позже или напишите в тех поддержку",
    )


@bot.message_handler(content_types=["successful_payment"])
async def got_payment(message):

    invoice_payload = message.successful_payment.invoice_payload.split("#")

    if "payall" in message.successful_payment.invoice_payload:

        async with async_session() as session:
            chain_dal = ChainDAL(session)

            user_chains = await chain_dal.getChainsByChatId(message.chat.id)

        async with async_session() as session:
            chain_dal = ChainDAL(session)
            for chain in user_chains:
                res = await chain_dal.updateActiveDueDate(
                    chain_id=int(chain[0].chain_id), interval_days=int(invoice_payload[1])
                )

        await bot.send_message(
            message.chat.id,
            MarkupBuilder.got_payment_text(total_amount=message.successful_payment.total_amount / 100,
                                           currency=message.successful_payment.currency)
        )

        await _mainMenu(message=message)

    else:

        async with async_session() as session:
            chain_dal = ChainDAL(session)
            result = await chain_dal.updateActiveDueDate(
                chain_id=int(invoice_payload[1]), interval_days=int(invoice_payload[0])
            )

        await bot.send_message(
            message.chat.id,
            MarkupBuilder.got_payment_text(total_amount=message.successful_payment.total_amount / 100, currency = message.successful_payment.currency)
        )

        await _mainMenu(message=message)