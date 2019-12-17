# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer

from utils.cm.agent import parse_http_accept_language
from adapter.bot import get_bot, trainer_databases, trainer, STORAGE_ADAPTER

app = Flask(__name__)
CORS(app, supports_credentials=True)

# bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
bot = None

@app.route("/")
def index():
    global bot
    bot = get_bot("scapp", STORAGE_ADAPTER.SQLLITE, None, None)
    return render_template("index.html")

@app.route("/trainer")
def bot_trainer():
    chats = [
        'How are you?',
        'I am good.',
        'That is good to hear.',
        'Thank you',
        'You are welcome.',
    ]
    bot = get_bot("scapp", STORAGE_ADAPTER.SQLLITE, None, None)
    result = trainer(chats)
    return jsonify(result), 200

@app.route("/trainer_all")
def bot_trainer_databases():
    l = parse_http_accept_language(request.headers.get('Accept-Language', ''))
    if l is None:
        l = 'ja'
    # l = 'en'

    logic_adapters = [
        "chatterbot.logic.MathematicalEvaluation"
        ,"chatterbot.logic.TimeLogicAdapter"
        ,"chatterbot.logic.BestMatch"
    ]
    bot = get_bot("scapp", STORAGE_ADAPTER.SQLLITE, logic_adapters, None)
    result = trainer_databases(bot, l)
    return jsonify(result), 200

@app.route("/get")
def get_bot_response():
    msg = request.args.get('msg')
    if bot is None:
        return 'Not Setting ChatBot!!!'

    result = None
    try:
        result = str(bot.get_response(msg))
    except EOFError as e:
        result = str(e)

    return result

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8084)
