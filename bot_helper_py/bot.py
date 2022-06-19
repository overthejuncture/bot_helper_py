from telegram import Update

def check(update: Update):
    print(update.message.from_user.id)
