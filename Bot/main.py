# import asyncio
# from datetime import datetime, time, timedelta
# from telebot.asyncio_filters import ForwardFilter
# from telebot.asyncio_filters import IsDigitFilter
# from telebot.asyncio_filters import IsReplyFilter
# from telebot.asyncio_filters import StateFilter
# from Bot.Config import bot
# from Bot.Config import message_context_manager
# from Bot.Config import new_chain_manager
# from Bot.Handlers.helpMenuHandler import _contact
# from Bot.Handlers.helpMenuHandler import _faq
# from Bot.Handlers.helpMenuHandler import _helpMenu
# from Bot.Handlers.mainMenuHandler import _mainMenu
# from Bot.Handlers.newChainHandler import _addNewChain
# from Bot.Handlers.newChainHandler import _addSourceToCurrentChain
# from Bot.Handlers.newChainHandler import confirmedChain
# from Bot.Handlers.newChainHandler import confirmNewChainText
# from Bot.Handlers.newChainHandler import error_no_added_sources_url
# from Bot.Handlers.newChainHandler import instagram_source_channel_msg
# from Bot.Handlers.newChainHandler import NewChainStates
# from Bot.Handlers.newChainHandler import setParsingOldType
# from Bot.Handlers.newChainHandler import setPostSchedule
# from Bot.Handlers.newChainHandler import setTargetChannel
# from Bot.Handlers.newChainHandler import telegram_source_channel_msg
# from Bot.Handlers.newChainHandler import vk_source_channel_msg
# from Bot.Markups import MarkupBuilder
# from Bot.Middlewares.floodingMiddleware import FloodingMiddleware
# from DataBase.DataAccessLayer.ChainDAL import ChainDAL
# from DataBase.session import async_session
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
#
#
# class Bot:
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super().__new__(cls, *args, **kwargs)
#         return cls._instance
#
#     def __init__(self):
#         bot.add_custom_filter(IsReplyFilter())
#         bot.add_custom_filter(ForwardFilter())
#         bot.add_custom_filter(StateFilter(bot))
#         bot.add_custom_filter(IsDigitFilter())
#         bot.setup_middleware(FloodingMiddleware(1))
#         self.scheduler = AsyncIOScheduler()
#
#     @staticmethod
#     @bot.message_handler(func=lambda message: True)
#     async def HandlerTextMiddleware(message):
#         if message.text == "📖 Помощь":
#             def show_scheduled_tasks():
#                 jobs = b.scheduler.get_jobs()
#                 print("Scheduled tasks:")
#                 for job in jobs:
#                     print(f"Next run: {job.next_run_time}, ID: {job.id}")
#
#             show_scheduled_tasks()
#             await _helpMenu(message)
#
#         if message.text == "🔗 Добавить новую связку":
#             await bot.delete_state(message.chat.id)
#             new_chain_manager.newChain(chat_id=message.chat.id)
#             print(new_chain_manager.chainStore)
#             await _addNewChain(message)
#
#         if message.text == "🔙Назад":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=message.chat.id)
#             await _mainMenu(message=message)
#
#     @staticmethod
#     @bot.callback_query_handler(func=lambda call: True)
#     async def HandlerInlineMiddleware(call):
#         print("call data: ", call.data)
#         if call.data == "contact":
#             await _contact(call)
#
#         if call.data == "faq":
#             await _faq(call)
#
#         if call.data == "back_to_main_menu":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             await _mainMenu(message=call.message)
#
#         if call.data == "back_to_new_chain_menu":
#             print(new_chain_manager.chainStore)
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             await bot.delete_state(call.message.chat.id)
#             await _addNewChain(message=call.message)
#
#         if call.data == "back_to_chain_menu":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             await bot.delete_state(call.message.chat.id)
#             await _addSourceToCurrentChain(call.message)
#             print(new_chain_manager.chainStore)
#
#         if call.data == "back_to_setTarget":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             print("back_to_setTarget")
#             await setTargetChannel(call.message)
#             await bot.set_state(call.message.chat.id, NewChainStates.setTarget)
#
#         if call.data == "new_chain#tg":
#             await telegram_source_channel_msg(call.message)
#             await bot.set_state(call.message.chat.id, NewChainStates.telegram)
#
#         if call.data == "new_chain#vk":
#             await vk_source_channel_msg(call.message)
#             await bot.set_state(call.message.chat.id, NewChainStates.vk)
#
#         if call.data == "new_chain#inst":
#             await instagram_source_channel_msg(call.message)
#             await bot.set_state(call.message.chat.id, NewChainStates.instagram)
#
#         if call.data == "new_chain#continue":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             if len(new_chain_manager.chainStore[call.message.chat.id].source_urls) == 0:
#                 await error_no_added_sources_url(call.message)
#             else:
#                 await setTargetChannel(call.message)
#                 await bot.set_state(call.message.chat.id, NewChainStates.setTarget)
#
#         if call.data == "new_chain#type=new":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             new_chain_manager.add_parsing_type(chat_id=call.message.chat.id, parsing_type="Новые")
#             await setPostSchedule(call.message, "🆕 Новые")
#             await bot.set_state(call.message.chat.id, NewChainStates.setParsingTime)
#
#         if call.data == "new_chain#type=old":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             await setParsingOldType(call.message)
#
#         if call.data == "new_chain#from_start":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             new_chain_manager.add_parsing_type(chat_id=call.message.chat.id, parsing_type="С начала")
#             await setPostSchedule(call.message, "С начала")
#             await bot.set_state(call.message.chat.id, NewChainStates.setParsingTime)
#
#         if call.data == "back_to_set_parsing_type":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             msg = await bot.send_message(
#                 call.message.chat.id,
#                 MarkupBuilder.setParsingType(),
#                 reply_markup=MarkupBuilder.parsingTypeMenu(),
#                 parse_mode="MarkdownV2",
#             )
#             await message_context_manager.add_msgId_to_help_menu_dict(chat_id=call.message.chat.id, msgId=msg.message_id)
#             await bot.set_state(call.message.chat.id, NewChainStates.setParsingType)
#
#         if call.data == "back_to_timeSetter":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             await setPostSchedule(
#                 call.message,
#                 parsing_type=new_chain_manager.chainStore[call.message.chat.id].parsing_type,
#             )
#             await bot.set_state(call.message.chat.id, NewChainStates.setParsingTime)
#
#         if call.data == "skip_to_confirmChain":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             await confirmNewChainText(call.message)
#
#         if call.data == "new_chain#confirmChain":
#             await message_context_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
#             await confirmedChain(call.message)
#
#     def run_scheduled_tasks(self):
#
#         existing_jobs = {}
#
#         async def process_chain():
#             await bot.send_message(406149871, "execute task at time")
#
#         async def schedule_chains():
#             async with async_session() as session:
#
#                 chain_dal = ChainDAL(session)
#                 active_chains = await chain_dal.getActiveChains()
#
#                 for chain in active_chains:
#                     chain_parsing_times = chain[0].parsing_time
#
#                     if existing_jobs.get(chain[0].chain_id) is None:
#                         existing_jobs[chain[0].chain_id] = {
#                             "chain_id": chain[0].chain_id,
#                             "chain_times": chain[0].parsing_time,
#                             "is_added": False,
#                             "jobs": []
#                         }
#
#                         for parsing_time in chain_parsing_times:
#                             scheduled_time = datetime.strptime(parsing_time, "%H:%M").time()
#                             job = self.scheduler.add_job(process_chain, "cron", hour=scheduled_time.hour,
#                                                          minute=scheduled_time.minute)
#                             jobs_list = existing_jobs[chain[0].chain_id]['jobs']
#                             jobs_list.append(job)
#                             existing_jobs[chain[0].chain_id]['jobs'] = jobs_list
#                             existing_jobs[chain[0].chain_id]['is_added'] = True
#
#                     if existing_jobs[chain[0].chain_id]['is_added'] and chain[0].parsing_time == existing_jobs[chain[0].chain_id]['chain_times']:
#                         pass
#                     if existing_jobs[chain[0].chain_id]['is_added'] and chain[0].parsing_time != existing_jobs[chain[0].chain_id]['chain_times']:
#                         for job in existing_jobs[chain[0].chain_id]['jobs']:
#                             job.remove()
#
#                         existing_jobs[chain[0].chain_id]['chain_times'] = chain[0].parsing_time
#
#                         for parsing_time in chain[0].parsing_time:
#                             scheduled_time = datetime.strptime(parsing_time, "%H:%M").time()
#                             job = self.scheduler.add_job(process_chain, "cron", hour=scheduled_time.hour,
#                                                          minute=scheduled_time.minute)
#                             jobs_list = existing_jobs[chain[0].chain_id]['jobs']
#                             jobs_list.append(job)
#                             existing_jobs[chain[0].chain_id]['jobs'] = jobs_list
#                             existing_jobs[chain[0].chain_id]['is_added'] = True
#
#                 print(existing_jobs)
#
#         self.scheduler.add_job(schedule_chains, "interval", seconds=5)  # Проверять каждую минуту
#         self.scheduler.start()
#
#     async def polling(self):
#         task1 = asyncio.create_task(bot.infinity_polling())
#         self.run_scheduled_tasks()  # Start the scheduler here
#         await task1
#
#
# if __name__ == "__main__":
#     b = Bot()
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(b.polling())
#     except KeyboardInterrupt:
#         pass
#     finally:
#         loop.run_until_complete(loop.shutdown_asyncgens())
#         loop.close()
import asyncio
from datetime import datetime
from datetime import time
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telebot.asyncio_filters import ForwardFilter
from telebot.asyncio_filters import IsDigitFilter
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import StateFilter

from Bot.Config import bot
from Bot.Config import message_context_manager
from Bot.Config import new_chain_manager
from Bot.Handlers.helpMenuHandler import _contact
from Bot.Handlers.helpMenuHandler import _faq
from Bot.Handlers.helpMenuHandler import _helpMenu
from Bot.Handlers.mainMenuHandler import _mainMenu
from Bot.Handlers.newChainHandler import _addNewChain
from Bot.Handlers.newChainHandler import _addSourceToCurrentChain
from Bot.Handlers.newChainHandler import confirmedChain
from Bot.Handlers.newChainHandler import confirmNewChainText
from Bot.Handlers.newChainHandler import error_no_added_sources_url
from Bot.Handlers.newChainHandler import instagram_source_channel_msg
from Bot.Handlers.newChainHandler import NewChainStates
from Bot.Handlers.newChainHandler import setParsingOldType
from Bot.Handlers.newChainHandler import setPostSchedule
from Bot.Handlers.newChainHandler import setTargetChannel
from Bot.Handlers.newChainHandler import telegram_source_channel_msg
from Bot.Handlers.newChainHandler import vk_source_channel_msg
from Bot.Markups import MarkupBuilder
from Bot.Middlewares.floodingMiddleware import FloodingMiddleware
from DataBase.DataAccessLayer.ChainDAL import ChainDAL
from DataBase.session import async_session


class ScheduledTasks:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.existing_jobs = {}

    async def process_chain(self):
        await bot.send_message(406149871, "execute task at time")

    async def schedule_chains(self):
        async with async_session() as session:
            chain_dal = ChainDAL(session)
            active_chains = await chain_dal.getActiveChains()

            for chain in active_chains:
                chain_id = chain[0].chain_id
                chain_parsing_times = chain[0].parsing_time

                if self.existing_jobs.get(chain_id) is None:
                    self.existing_jobs[chain_id] = {
                        "chain_id": chain_id,
                        "chain_times": chain_parsing_times,
                        "is_added": False,
                        "jobs": [],
                    }

                    for parsing_time in chain_parsing_times:
                        scheduled_time = datetime.strptime(parsing_time, "%H:%M").time()
                        job = self.scheduler.add_job(
                            self.process_chain,
                            "cron",
                            hour=scheduled_time.hour,
                            minute=scheduled_time.minute,
                        )
                        jobs_list = self.existing_jobs[chain_id]["jobs"]
                        jobs_list.append(job)
                        self.existing_jobs[chain_id]["jobs"] = jobs_list
                        self.existing_jobs[chain_id]["is_added"] = True

                if (
                    self.existing_jobs[chain_id]["is_added"]
                    and chain_parsing_times
                    == self.existing_jobs[chain_id]["chain_times"]
                ):
                    continue

                if (
                    self.existing_jobs[chain_id]["is_added"]
                    and chain_parsing_times
                    != self.existing_jobs[chain_id]["chain_times"]
                ):
                    for job in self.existing_jobs[chain_id]["jobs"]:
                        job.remove()

                    self.existing_jobs[chain_id]["jobs"] = []
                    self.existing_jobs[chain_id]["chain_times"] = chain_parsing_times

                    for parsing_time in chain_parsing_times:
                        scheduled_time = datetime.strptime(parsing_time, "%H:%M").time()
                        job = self.scheduler.add_job(
                            self.process_chain,
                            "cron",
                            hour=scheduled_time.hour,
                            minute=scheduled_time.minute,
                        )
                        jobs_list = self.existing_jobs[chain_id]["jobs"]
                        jobs_list.append(job)
                        self.existing_jobs[chain_id]["jobs"] = jobs_list
                        self.existing_jobs[chain_id]["is_added"] = True

        print(len(self.existing_jobs[chain_id]["jobs"]))

    def run(self):
        self.scheduler.add_job(
            self.schedule_chains, "interval", seconds=5
        )  # Проверять каждую минуту
        self.scheduler.start()


class Bot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitFilter())
        bot.setup_middleware(FloodingMiddleware(1))
        self.scheduler = AsyncIOScheduler()
        self.scheduled_tasks = ScheduledTasks(self.scheduler)

    @staticmethod
    @bot.message_handler(func=lambda message: True)
    async def HandlerTextMiddleware(message):
        if message.text == "📖 Помощь":

            def show_scheduled_tasks():
                jobs = b.scheduler.get_jobs()
                print("Scheduled tasks:")
                for job in jobs:
                    print(f"Next run: {job.next_run_time}, ID: {job.id}")

            show_scheduled_tasks()
            await _helpMenu(message)

        if message.text == "🔗 Добавить новую связку":
            await bot.delete_state(message.chat.id)
            new_chain_manager.newChain(chat_id=message.chat.id)
            print(new_chain_manager.chainStore)
            await _addNewChain(message)

        if message.text == "🔙Назад":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            await _mainMenu(message=message)

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def HandlerInlineMiddleware(call):
        print("call data: ", call.data)
        if call.data == "contact":
            await _contact(call)

        if call.data == "faq":
            await _faq(call)

        if call.data == "back_to_main_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _mainMenu(message=call.message)

        if call.data == "back_to_new_chain_menu":
            print(new_chain_manager.chainStore)
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await bot.delete_state(call.message.chat.id)
            await _addNewChain(message=call.message)

        if call.data == "back_to_chain_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await bot.delete_state(call.message.chat.id)
            await _addSourceToCurrentChain(call.message)
            print(new_chain_manager.chainStore)

        if call.data == "back_to_setTarget":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            print("back_to_setTarget")
            await setTargetChannel(call.message)
            await bot.set_state(call.message.chat.id, NewChainStates.setTarget)

        if call.data == "new_chain#tg":
            await telegram_source_channel_msg(call.message)
            await bot.set_state(call.message.chat.id, NewChainStates.telegram)

        if call.data == "new_chain#vk":
            await vk_source_channel_msg(call.message)
            await bot.set_state(call.message.chat.id, NewChainStates.vk)

        if call.data == "new_chain#inst":
            await instagram_source_channel_msg(call.message)
            await bot.set_state(call.message.chat.id, NewChainStates.instagram)

        if call.data == "new_chain#continue":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            if len(new_chain_manager.chainStore[call.message.chat.id].source_urls) == 0:
                await error_no_added_sources_url(call.message)
            else:
                await setTargetChannel(call.message)
                await bot.set_state(call.message.chat.id, NewChainStates.setTarget)

        if call.data == "new_chain#type=new":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            new_chain_manager.add_parsing_type(
                chat_id=call.message.chat.id, parsing_type="Новые"
            )
            await setPostSchedule(call.message, "🆕 Новые")
            await bot.set_state(call.message.chat.id, NewChainStates.setParsingTime)

        if call.data == "new_chain#type=old":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await setParsingOldType(call.message)

        if call.data == "new_chain#from_start":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            new_chain_manager.add_parsing_type(
                chat_id=call.message.chat.id, parsing_type="С начала"
            )
            await setPostSchedule(call.message, "С начала")
            await bot.set_state(call.message.chat.id, NewChainStates.setParsingTime)

        if call.data == "back_to_set_parsing_type":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            msg = await bot.send_message(
                call.message.chat.id,
                MarkupBuilder.setParsingType(),
                reply_markup=MarkupBuilder.parsingTypeMenu(),
                parse_mode="MarkdownV2",
            )
            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=call.message.chat.id, msgId=msg.message_id
            )
            await bot.set_state(call.message.chat.id, NewChainStates.setParsingType)

        if call.data == "back_to_timeSetter":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await setPostSchedule(
                call.message,
                parsing_type=new_chain_manager.chainStore[
                    call.message.chat.id
                ].parsing_type,
            )
            await bot.set_state(call.message.chat.id, NewChainStates.setParsingTime)

        if call.data == "skip_to_confirmChain":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await confirmNewChainText(call.message)

        if call.data == "new_chain#confirmChain":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await confirmedChain(call.message)

    async def polling(self):
        task1 = asyncio.create_task(bot.infinity_polling())
        self.scheduled_tasks.run()  # Start the scheduled tasks here
        await task1


if __name__ == "__main__":
    b = Bot()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(b.polling())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
