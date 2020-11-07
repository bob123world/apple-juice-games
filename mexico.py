### Mexico ###
# A very simple drinking game based on the popular gambling game of the same name.

# The game is used with two dices, in this program those are replaced with a random generator.
# Rules:
# 1.) When throwing a 2 and a 1 with the dice, the loser of the round needs to drown his/hers glass. When you throw 21, you can't lose the round.
# 2.) When both dices result in the same number, the number is multiplies by 100. So when you throw a double 6, you have 600 (highest score in the game)
# 3.) When the dices are not equal, the highest number is multiplied by 10 and the lowest dice is added to that number. So throwing a 5 and a 4 will result in 54.
# 4.) The player who goes first can throw as many times as he likes. He can decide to stop at a certain score. The other players can try as many times as the first player to pass the lowest ranking.
# 5.) The player who threw the least amount of points (except from 21) needs to drink 5 times. When 21 was thrown in the round the player needs to drown his/her glass.
import os
import json
import random
import logging
import requests
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

THROW = range(1)

option_keyboard = [["Throw"]]
dice = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]

class Mexico():
    def __init__(self):
        ### Get working directory
        self.path = os.path.dirname(os.path.realpath(__file__))

        ### Get configuration data
        config = {}
        try:
            config = json.load(open(os.path.join(self.path, "config.json")))
        except:
            logger.critical("File Not found: config.json")
            exit()

        self.token = config["telegram"]["token"]
        self.chat_id = config["telegram"]["chat_id"]

        # Initialize Telegram bot
        pp = PicklePersistence(filename="mexico")
        updater = Updater(self.token, persistence= pp, use_context=True)
        dp = updater.dispatcher

        option_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states = {
                THROW: [MessageHandler(Filters.regex("^(Throw)$"), self.throw),],
            },
            fallbacks = [MessageHandler(Filters.regex("^restart$"), self.start)],
            name = "mexico",
            persistent= True
        )

        dp.add_handler(option_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        updater.idle()

    def start(self, update, context):
        """Message the group that a player has joined"""
        name = update.message.from_user.first_name
        self.broadcast(name + " has joined!")
        markup = ReplyKeyboardMarkup(option_keyboard)
        response = "Welcome"
        update.message.reply_text(response, reply_markup=markup)
        return THROW

    def throw(self, update, context):
        name = update.message.from_user.first_name
        random.shuffle(dice)
        dice1 = dice[0]
        random.shuffle(dice)
        dice2 = dice[0]
        message = name + " threw " + dice1 + dice2
        self.broadcast(message)
        return THROW

    def broadcast(self, message):
        """broadcast a message to all the players"""
        send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chat_id + '&parse_mode=Markdown&text=' + message
        response = requests.get(send_text)

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == "__main__":
    bot = Mexico()