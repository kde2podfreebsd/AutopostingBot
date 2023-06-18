from telebot import formatting
from telebot import types
from telebot.types import ReplyKeyboardMarkup


class MarkupBuilder:
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
            "📧 Связаться с нами Если у вас возникли вопросы, проблемы или вам требуется дополнительная помощь, пожалуйста, обратитесь к нам по следующим контактным данным:",
            formatting.mbold("\n 📞 Телефон:"),
            " [номер телефона]",
            formatting.mbold("\n 📧 Email:"),
            " [адрес электронной почты]",
            formatting.mbold("\n 💬 Чат поддержки:"),
            " [ссылка на чат поддержки]\n\nМы всегда готовы помочь вам и ответить на ваши вопросы\.\nНе стесняйтесь обращаться к нам\.",  # noqa
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
"""
        )
        return cls._faq_text

    @classmethod
    @property
    def new_chain_menu_text(cls):
        cls._new_chain_menu_text: object = formatting.format_text(
            "🔗 Выберите источник контента \\- Пожалуйста, выберите, откуда вы хотите парсить контент: Телеграм канал, ВК\\-паблик или Instagram страница\.",
            # noqa
            separator="",
        )
        return cls._new_chain_menu_text

    @classmethod
    def new_chain_menu(cls):
        menu: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True,
        ).add(
            types.KeyboardButton("📡 Телеграм канал"),
            types.KeyboardButton("🌐 ВК-паблик"),
            types.KeyboardButton("📸 Instagram страница"),
            types.KeyboardButton("➡️Продолжить"),
            types.KeyboardButton("🔙Назад"),
        )
        return menu

    @classmethod
    @property
    def create_new_telegram_chain_text(cls):
        cls._create_new_telegram_chain_text: object = formatting.format_text(
            formatting.mbold("Вы выбрали телеграм канал📡"),
            "\n 🔗 Пожалуйста, отправьте @username канала, откуда вы хотите парсить контент\. Убедитесь, что канал является открытым, username корректен и доступен для поиска",
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
            separator="",
        )
        return cls._create_new_instagram_chain_text

    @classmethod
    @property
    def create_new_vk_chain_text(cls):
        cls._create_new_vk_chain_text: object = formatting.format_text(
            formatting.mbold("Вы выбрали ВК-паблик 🌐 "),
            "\n 🔗 Пожалуйста, отправьте ID паблика, откуда вы хотите парсить контент\.\nДля получения id паблика, воспользуйтесь сервисом https://regvk\.com/id/\. Убедитесь, что паблик является открытым\.",
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
