from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

my_db = mysql.connector.connect(
    host = "cloud.mindsdb.com",
    user = "kryshchainani@gmail.com",
    password = "Stronk",
    port="3306"
)

TOKEN: Final = '6225730302:AAGIfC6NFuE2GJFupFDNZmLbQ4ff04EeDDg'
BOT_USERNAME: Final = '@LegalCodebreakerBot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Im Here to answer any questions you may have about the Singaporean Legal System!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('If you need more help, please turn to Google or seek an actual lawyer to get professional advice.')


# Responses

def handle_response(text: str, username:str) -> str:
    user_message = str(text)
    cursor = my_db.cursor()
    cursor.execute(f'''SELECT response from mindsdb.testbot5 WHERE author_username = "{username}" AND text="{user_message}" ''')
    for x in cursor:
        formatted_text = str(x).replace("\\n", "\n").strip("(),")
        return formatted_text


async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text:str = text.replace(BOT_USERNAME, '').strip()
            response:str = handle_response(new_text, update.message.chat.username)
        else:
            return
    else:
        response: str = handle_response(text, update.message.chat.username)

    print('Bot:',response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
    print('starting bot...')
    app =Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    app.add_error_handler(error)

    print('polling started...')
    app.run_polling(poll_interval=1)
