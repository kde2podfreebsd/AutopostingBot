import datetime

from telebot import formatting
from telebot import types
from telebot.types import ReplyKeyboardMarkup

from Bot.Config import new_chain_manager


class MarkupBuilder:
    error_timeParse_toChain_text = None
    _error_no_added_sources_url_text: None | object = None
    error_botNotAdmin_toChain_text: None | object = None
    _setParsingOldTypeText: None | object = None
    confirmNewChain_output_text: object | None = None
    setTime_text: None | object = None
    setParsingType_text: None | object = None
    # choose_parsing_type_text: None | object = None
    setTargetChannel_text: None | object = None
    error_maxSize_toChain_text: None | object = None
    error_duplicate_source_url_toChain_text: None | object = None
    _welcome_text: object | None = None
    _hide_menu: object | None = None
    _contact_text: object | None = None
    _faq_text: object | None = None
    _new_chain_menu_text: object | None = None
    _create_new_telegram_chain_text: object | None = None
    _create_new_instagram_chain_text: object | None = None
    _create_new_vk_chain_text: object | None = None

    @classmethod
    def main_menu(cls):
        menu: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True,
        ).add(
            types.KeyboardButton("🔗 Добавить новую связку"),
            types.KeyboardButton("💳 Оплатить подписку"),
            types.KeyboardButton("📋 Мои связки"),
            types.KeyboardButton("📖 Помощь"),
        )
        return menu

    @classmethod
    @property
    def welcome_text(cls):
        cls._welcome_text: object = formatting.format_text(
            formatting.mbold("👋Приветствую вас в нашем боте!"),  # noqa
            "\nВы можете добавить новую связку для парсинга и постинга контента, управлять текущими связками, оплатить подписку или получить помощь\.",  # noqa
            # noqa
            # noqa
            separator="",
        )
        return cls._welcome_text

    @classmethod
    @property
    def hide_menu(cls):
        cls._hide_menu: object = types.ReplyKeyboardRemove()
        return cls._hide_menu

    @classmethod
    @property
    def help_text(cls):
        cls._welcome_text: object = formatting.format_text(
            "📖 Добро пожаловать в раздел помощи\!\n\nЗдесь вы можете найти ответы на часто задаваемые вопросы и получить руководство по использованию нашего бота\.",  # noqa
            # noqa
            # noqa
            formatting.mbold("👋\n\nВыберите одну из следующих опций:"),  # noqa
            separator="",
        )
        return cls._welcome_text

    @classmethod
    def help_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [types.InlineKeyboardButton(text="❓ FAQ", callback_data="faq")],
                [
                    types.InlineKeyboardButton(
                        text="📧 Связаться", callback_data="contact"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_main_menu"
                    )
                ],
            ],
        )

    @classmethod
    @property
    def contact_text(cls) -> object:
        cls._contact_text: object = formatting.format_text(
            "📧 Связаться с нами Если у вас возникли вопросы, проблемы или вам требуется дополнительная помощь, пожалуйста, обратитесь к нам по следующим контактным данным:",  # noqa
            formatting.mbold("\n 📞 Телефон:"),  # noqa
            " [номер телефона]",  # noqa
            formatting.mbold("\n 📧 Email:"),  # noqa
            " [адрес электронной почты]",  # noqa
            formatting.mbold("\n 💬 Чат поддержки:"),  # noqa
            " [ссылка на чат поддержки]\n\nМы всегда готовы помочь вам и ответить на ваши вопросы\.\nНе стесняйтесь обращаться к нам\.",  # noqa
            # noqa
            # noqa
        )

        return cls._contact_text

    @classmethod
    @property
    def faq_text(cls) -> object:
        cls._faq_text: object = formatting.format_text(
            f"""
{formatting.mbold("❔ Вопрос: ")}Как добавить новую связку для парсинга контента?
{formatting.mbold("💬 Ответ: ")}Чтобы добавить новую связку, перейдите в меню "Добавить новую связку" и следуйте инструкциям\.

{formatting.mbold("❔ Вопрос: ")}Как изменить источник контента для существующей связки?
{formatting.mbold("💬 Ответ: ")}Выберите связку, которую хотите изменить, в меню "Мои связки", затем выберите опцию "Изменить источник контента" и следуйте инструкциям\.

{formatting.mbold("❔ Вопрос: ")}Как настроить время постинга для связки?
{formatting.mbold("💬 Ответ: ")}В меню "Мои связки" выберите нужную связку, затем выберите опцию "Изменить время постинга" и следуйте инструкциям\.

{formatting.mbold("❔ Вопрос: ")}Как удалить связку?
{formatting.mbold("💬 Ответ: ")}В меню "Мои связки" выберите связку, которую хотите удалить, затем выберите опцию "Удалить связку" и подтвердите удаление\.

{formatting.mbold("❔ Вопрос: ")}Как оплатить подписку для связки?
{formatting.mbold("💬 Ответ: ")}В меню "Мои связки" выберите связку, для которой хотите оплатить подписку, затем выберите опцию "Оплатить подписку" и следуйте инструкциям\.

{formatting.mbold("❔ Вопрос: ")}Как связаться с командой поддержки?
{formatting.mbold("💬 Ответ: ")}В разделе "Помощь" выберите опцию "Связаться с нами" для получения контактной информации и способов связи с нашей командой поддержки\.
"""  # noqa
        )
        return cls._faq_text

    @classmethod
    @property
    def new_chain_menu_text(cls):
        cls._new_chain_menu_text: object = formatting.format_text(
            "🔗 Выберите источник контента \\- Пожалуйста, выберите, откуда вы хотите парсить контент: Телеграм канал, ВК\\-паблик или Instagram страница\.",  # noqa
            # noqa
            # noqa
            separator="",
        )
        return cls._new_chain_menu_text

    @classmethod
    # @property
    def current_chain_menu_text(cls, chat_id: int | str):
        additional_text = new_chain_manager.get_source_urls(chat_id=chat_id)
        cls._new_chain_menu_text: object = formatting.format_text(
            additional_text,
            "\n🔗 Выберите источник контента \\- Пожалуйста, выберите, откуда вы хотите парсить контент: Телеграм канал, ВК\\-паблик или Instagram страница\.",  # noqa
            # noqa
            # noqa
            # noqa
            separator="",
        )
        return cls._new_chain_menu_text

    @classmethod
    def new_chain_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="📡 Телеграм канал", callback_data="new_chain#tg"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🌐 ВК-паблик", callback_data="new_chain#vk"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="📸 Instagram страница", callback_data="new_chain#inst"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_main_menu"
                    )
                ],
            ],
        )

    @classmethod
    def current_chain_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="📡 Телеграм канал", callback_data="new_chain#tg"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🌐 ВК-паблик", callback_data="new_chain#vk"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="📸 Instagram страница", callback_data="new_chain#inst"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➡️Продолжить", callback_data="new_chain#continue"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_new_chain_menu"
                    )
                ],
            ],
        )

    @classmethod
    @property
    def create_new_telegram_chain_text(cls):
        cls._create_new_telegram_chain_text: object = formatting.format_text(
            formatting.mbold("Вы выбрали телеграм канал📡"),
            "\n 🔗 Пожалуйста, отправьте @username канала, откуда вы хотите парсить контент\. Убедитесь, что канал является открытым, username корректен и доступен для поиска",
            # noqa
            # noqa
            separator="",
        )
        return cls._create_new_telegram_chain_text

    @classmethod
    @property
    def create_new_instagram_chain_text(cls):
        cls._create_new_instagram_chain_text: object = formatting.format_text(
            formatting.mbold("Вы выбрали Instagram страницу 📸 "),
            "\n 🔗 Пожалуйста, отправьте ссылку на Instagram страницу, откуда вы хотите парсить контент\. Убедитесь, что профиль является открытым, сслыка корректна и доступна для просмотра\.",
            # noqa
            # noqa
            separator="",
        )
        return cls._create_new_instagram_chain_text

    @classmethod
    @property
    def create_new_vk_chain_text(cls):
        cls._create_new_vk_chain_text: object = formatting.format_text(
            formatting.mbold("Вы выбрали ВК\\-паблик 🌐 "),
            "\n 🔗 Пожалуйста, отправьте ID паблика, откуда вы хотите парсить контент\.\nДля получения id паблика, воспользуйтесь сервисом https://regvk\.com/id/\. Убедитесь, что паблик является открытым\.",
            # noqa
            # noqa
            separator="",
        )
        return cls._create_new_vk_chain_text

    @classmethod
    def back_to_new_chain_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_new_chain_menu"
                    )
                ]
            ],
        )

    @classmethod
    def back_to_chain_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_chain_menu"
                    )
                ]
            ],
        )

    @classmethod
    @property
    def error_in_add_url_toChain(cls):
        cls._create_new_telegram_chain_text: object = formatting.format_text(
            "⚠️ Извините, но ссылка, которую вы предоставили, не корректна или недоступна\\. Пожалуйста, убедитесь, что вы правильно скопировали и вставили ссылку, и что источник доступен для просмотра, затем попробуйте снова\\.",
            # noqa
            separator="",
        )
        return cls._create_new_telegram_chain_text

    @classmethod
    @property
    def error_botNotAdmin_toChain(cls):
        cls.error_botNotAdmin_toChain_text: object = formatting.format_text(
            "⚠️ Извините, но похоже, что бот не является администратором указанного вами канала\. Пожалуйста, добавьте бота в качестве администратора на вашем канале с правами на публикацию сообщений, а затем попробуйте снова\.",
            # noqa
            separator="",
        )
        return cls.error_botNotAdmin_toChain_text

    @classmethod
    @property
    def error_targetInSource_toChain(cls):
        cls._create_new_telegram_chain_text: object = formatting.format_text(
            "⚠️ Извините, но похоже, что бот уже добавлен в источники для автопостинга\. Укажите другой канал для постинга",
            # noqa
            separator="",
        )
        return cls._create_new_telegram_chain_text

    @classmethod
    @property
    def error_dateFromParse_toChain(cls):
        cls._create_new_telegram_chain_text: object = formatting.format_text(
            "⚠️ Неверный формат даты\. Пожалуйста, введите дату в правильном формате ДД\.ММ\.ГГГГ или выберите опцию 'С начала' для парсинга с самого первого поста на канале\.",
            # noqa
            separator="",
        )
        return cls._create_new_telegram_chain_text

    @classmethod
    @property
    def error_timeParse_toChain(cls):
        cls.error_timeParse_toChain_text: object = formatting.format_text(
            "⚠️ Неверный формат даты\\. Пожалуйста, введите дату в правильном формате \\- hh:mm\\|hh:mm\\|hh:mm",
            # noqa
            separator="",
        )
        return cls.error_timeParse_toChain_text

    @classmethod
    @property
    def error_duplicate_source_url_toChain(cls):
        cls.error_duplicate_source_url_toChain_text: object = formatting.format_text(
            "⚠️ Извините, но ссылка, которую вы предоставили, уже добавлена в текущую связку\. Укажите другую ссылку",
            # noqa
            # noqa
            separator="",
        )
        return cls.error_duplicate_source_url_toChain_text

    @classmethod
    @property
    def error_maxSize_toChain(cls):
        cls.error_maxSize_toChain_text: object = formatting.format_text(
            "⚠️ Извините, максимальное колличество исходных каналов для автопостинга \\- 3\.",  # noqa
            # noqa
            separator="",
        )
        return cls.error_maxSize_toChain_text

    @classmethod
    def setTargetChannel(cls, chat_id: int | str):
        additional_text = new_chain_manager.get_source_urls(chat_id=chat_id)
        cls.setTargetChannel_text: object = formatting.format_text(
            additional_text,
            "\nПожалуйста, отправьте ссылку на ваш телеграм канал, на который вы хотите выкладывать контент\. Убедитесь, что бот добавлен в этот канал как администратор с правами на публикацию сообщений\.",
            # noqa
            # noqa
            separator="",
        )
        return cls.setTargetChannel_text

    @classmethod
    @property
    def setParsingType(cls):
        cls.setParsingType_text: object = formatting.format_text(
            "🔄 Выберите тип парсинга\nПожалуйста, выберите, какие посты вы хотите парсить: новые или старые\.",  # noqa
            # noqa
            separator="",
        )
        return cls.setParsingType_text

    @classmethod
    def parsingTypeMenu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🆕 Новые", callback_data="new_chain#type=new"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔄 Старые", callback_data="new_chain#type=old"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_setTarget"
                    )
                ],
            ],
        )

    @classmethod
    def setTime(cls, parsing_type):
        cls.setTime_text: object = formatting.format_text(
            f"Вы указали тип парсинга: {parsing_type}"
            "\n\n⏰ Пожалуйста, введите время выхода постов, разделяя время запятыми\. Используйте формат 24\\-часов\. Например, если вы хотите, чтобы посты публиковались в 10:00, 14:00 и 18:00, введите '10:00\|14:00\|18:00",
            # noqa
            separator="",
        )
        return cls.setTime_text

    from typing import List

    @classmethod
    def setAdditionalText(cls, time_list: List[str]):
        cls.setTime_text: object = formatting.format_text(
            f"Вы указали время для выхода постов: {time_list}"
            "\n\n➕Вы можете добавить подпись к каждому посту, который публикуется на вашем канале с источников:   Введите текст подписи с гиперссылкой в формате '[Текст](Ссылка)', или пропустите этот пункт, нажав на кнопку '➡️Пропустить'",
            # noqa
            separator="",
        )
        return cls.setTime_text

    @classmethod
    def back_to_timeSetter(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="➡️Пропустить", callback_data="skip_to_confirmChain"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_timeSetter"
                    )
                ],
            ],
        )

    @classmethod
    def back_to_timeSetterSolo(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_timeSetter"
                    )
                ]
            ],
        )

    @classmethod
    def confirmNewChainText(cls, chat_id: int | str):
        chain_builder = new_chain_manager.chainStore[chat_id]
        posting_type = ""
        if chain_builder.parsing_type == "Новые":
            posting_type = chain_builder.parsing_type
        elif isinstance(chain_builder.parsing_type, datetime.datetime):
            posting_type = f"Постинга с даты: {chain_builder.parsing_type}"
        elif chain_builder.parsing_type == "С начала":
            posting_type = f"Постинга с начала"
        cls.confirmNewChain_output_text = f"""
Исходные каналы для парсинга: {new_chain_manager.get_source_urls(chat_id=chat_id)}
Канал для постинга: {chain_builder.target_tg_channel_username}
Тип постинга: {posting_type}
Время для постинга: {chain_builder.parsing_time}
Добавочный текст: {chain_builder.additional_text if chain_builder.additional_text is not None else ""}
        """
        return cls.confirmNewChain_output_text

    @classmethod
    @property
    def confirm_chain1(cls):
        return "✅ Ваша новая связка успешно создана\! Теперь контент будет автоматически парситься из выбранного вами источника и публиковаться на вашем канале согласно выбранному вами расписанию\. Оплатите эту связку в разделе 💳 Оплатить подписку\.\nВы можете управлять своими связками в любое время в меню '📋 Мои связки'\."

    @classmethod
    def confirmNewChain(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="✅Потдвердить связку",
                        callback_data="new_chain#confirmChain",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="❌Сбросить связку", callback_data="back_to_new_chain_menu"
                    )
                ],
            ],
        )

    @classmethod
    @property
    def setParsingOldTypeText(cls):
        cls._setParsingOldTypeText = "📅 Пожалуйста, введите дату в формате ДД\.ММ\.ГГГГ, с которой вы хотите начать парсить посты из источника\.\n\nЕсли вы хотите начать с самого первого поста на канале, выберите опцию 'С начала'\."
        return cls._setParsingOldTypeText

    @classmethod
    def setParsingOldType(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="С начала", callback_data="new_chain#from_start"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_set_parsing_type"
                    )
                ],
            ],
        )

    @classmethod
    def backFromTimeSetter(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_set_parsing_type"
                    )
                ]
            ],
        )

    @classmethod
    @property
    def error_no_added_sources_url_text(cls):
        cls._error_no_added_sources_url_text = (
            "Вы не указали ссылки на источники для постинга"
        )
        return cls._error_no_added_sources_url_text
