from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

# read file
with open("token.txt", "r") as file:
    bot_token = file.read()


async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm a bot!")


async def default_reply(update: Update, context):
    # user = update.message.from_user
    user_choice = update.message.text
    context.user_data["is_useful"] = user_choice
    context.chat_data
    context.bot_data
    await update.message.reply_text("Ok", reply_markup=ReplyKeyboardRemove())


async def user_info(update: Update, context):
    user = update.message.forward_origin.sender_user
    reply = f"User ID: {user.id}, Name: {user.full_name}, Username: {user.username if user.username else 'No username'}"
    markup = ReplyKeyboardMarkup([["Nice", "Great", "Not good"]])
    await update.message.reply_text(reply, reply_markup=markup)


async def help(update: Update, context):
    await update.message.reply_text("Help!")


async def menu(update: Update, context):
    reply = "What do you want?????"
    markup = ReplyKeyboardMarkup([["user_info", "help", "menu"]])

    await update.message.reply_text(reply, reply_markup=markup)


def main():

    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler(command="start", callback=start))
    app.add_handler(
        MessageHandler(filters=filters.FORWARDED & ~filters.COMMAND, callback=user_info)
    )
    app.add_handler(CommandHandler(command="help", callback=help))
    app.add_handler(CommandHandler(command="menu", callback=menu))

    app.add_handler(MessageHandler(filters=filters.TEXT, callback=default_reply))

    app.run_polling()


if __name__ == "__main__":
    main()
