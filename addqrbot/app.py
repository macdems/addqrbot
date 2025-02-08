import os

from quart import Quart, request

from .bot import TelegramBot
from .qr import make_qrcode

TOKEN = os.environ['TOKEN']
telegram_bot = TelegramBot(TOKEN)

app = Quart(__name__)


@app.route('/' + TOKEN, methods=['GET', 'POST'])
async def webhook():
    json = await request.get_json()
    if json:
        await telegram_bot.process(json)
    return 'OK'


@app.route('/')
async def root():
    return 'OK'


@app.route('/qr')
async def qr():
    message = request.args.get('message', '')
    img = make_qrcode(message)
    return img.read(), 200, {'Content-Type': 'image/jpeg'}


@app.route('/setwebhook')
async def set_webhook():
    domain = request.host
    url = await telegram_bot.set_webhook(domain)
    return f'Webhook set to: <code>{url}/&lt;token&gt;</code>'
