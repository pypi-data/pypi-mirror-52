import asyncio
from typing import *

import telegram
import telegram.ext

from botter.api import BotEventProcessorImpl
from botter.api.handlers import *
from .telegram_api import *
from ..util import NoReturn

EXAMPLE_TOKEN = '1234:some_token'
class TelegramBot(BotEventProcessorImpl):
    name = 'telegram'
    error_base_type = telegram.TelegramError
    
    token: str
    client: telegram.Bot
    logger_name = 'botter.telegram.bot-impl'
    bot_user: TelegramUser
    
    updater: telegram.ext.Updater
    dispatcher: telegram.ext.Dispatcher
    event_loop: asyncio.AbstractEventLoop
    
    def __init__(self, token: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (token is not None):
            self.token = token
        if (getattr(self, 'token', None) is None):
            self.token = None
        
        self.client = telegram.Bot(self.token or EXAMPLE_TOKEN)
        self.register_telegram_events()
    
    def register_telegram_events(self):
        self.updater = telegram.ext.Updater(bot=self.client, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.all, self.on_message))
    
    def create_event(self, event_type: Type[Event], **kwargs):
        self.logger.critical(f"Creating event '{event_type.__name__}'...")
        # noinspection PyArgumentList
        return event_type(bot_user=self.bot_user, **kwargs)
    
    def on_message(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        self.logger.critical(f"Got inbound Telegram update: {update}, context: {context}")
        event = self.create_event(MessageEvent, message=TelegramMessage(self.client, update.message))
        coro = self.process_event(event)
        self.event_loop.run_until_complete(coro)
    
    async def on_ready(self):
        self.logger.critical(f"Telegram bot successfully started")
        self.bot_user = TelegramUser(self.client, self.client.bot)
        event = self.create_event(StartEvent)
        await self.process_event(event)
    
    def start(self) -> NoReturn:
        if (self.token is None or self.token == EXAMPLE_TOKEN):
            raise ValueError("Cannot start Telegram bot without token!")
        if (self.client.token != self.token):
            self.client.base_url = self.client.base_url.replace(self.client.token, self.token)
            self.client.base_file_url = self.client.base_file_url.replace(self.client.token, self.token)
            self.client.token = self.token
        
        self.logger.info("Starting Telegram bot...")
        self.event_loop = asyncio.get_event_loop()
        self.client.get_me()
        self.event_loop.run_until_complete(self.on_ready())
        self.updater.start_polling()
    
    def stop(self):
        self.logger.info("Stopping Telegram bot...")
        self.updater.stop()
        self.event_loop.stop()

__all__ = \
[
    'TelegramBot',
]
