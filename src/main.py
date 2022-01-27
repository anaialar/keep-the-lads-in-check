import os
import threading
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
from bot import Bot

app = Flask(__name__)

@app.route('/')
def hello_world() -> str:
    return 'Keep the lads in check!'

def main() -> None:
    bot = Bot()
    app_thread = threading.Thread(target = lambda: app.run(host = '0.0.0.0', port = os.getenv('PORT')), daemon = True)
    app_thread.start()
    bot.run(os.getenv('BOT_TOKEN'))

if __name__ == '__main__':
    main()
