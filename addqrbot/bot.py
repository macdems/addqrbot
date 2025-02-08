from urllib.parse import urlencode
from uuid import uuid4

from telegram import InlineQueryResultPhoto, Update
from telegram.ext import Application, CommandHandler, InlineQueryHandler, MessageHandler
from telegram.ext.filters import TEXT

from .qr import make_qrcode

class TelegramBot:

    def __init__(self, token):
        self.token = token
        self.application = Application.builder() \
            .token(token) \
            .connection_pool_size(1024) \
            .pool_timeout(10) \
            .concurrent_updates(True) \
        .build()

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(TEXT, self.process_message))
        self.application.add_handler(InlineQueryHandler(self.inline_query))

    async def process(self, json):
        update = Update.de_json(json, self.application.bot)
        if not self.application._initialized:
            await self.application.initialize()
        await self.application.process_update(update)

    async def set_webhook(self, domain):
        await self.application.bot.set_webhook(url=f'https://{domain}/{self.token}')
        return await self.get_webhook_url_base()

    async def get_webhook_url_base(self):
        webhook_info = await self.application.bot.get_webhook_info()
        return webhook_info.url.rsplit('/', 1)[0]

    async def process_message(self, update, context):
        msg = update.message.text
        img = make_qrcode(msg)
        await update.message.reply_photo(img)

    async def start(self, update, context):
        await update.message.reply_text("Hello! Send me a message and I'll reply with a QR code of it.")

    async def inline_query(self, update, context):
        query = update.inline_query.query

        msg = urlencode({'message': query})

        url = f'{await self.get_webhook_url_base()}/qr?{msg}'

        results = [
            InlineQueryResultPhoto(
                id=uuid4(), title="QR code", caption=query, photo_url=url, thumb_url=url, photo_width=310, photo_height=310
            )
        ]

        await update.inline_query.answer(results)
