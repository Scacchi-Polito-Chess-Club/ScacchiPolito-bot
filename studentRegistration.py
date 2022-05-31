from database import *
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
reply_keyboard = [
    ['ID Number', 'Faculty'],
    ['Name', 'Surname'],
    ['Lichess nickname', 'Chess nickname', 'FIDE_ELO'],
    ['Cancel', 'Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def studentRegistration(update, context):
    """Starts registration when the command /register is issued."""
    """Sends a message with three inline buttons attached."""
    conn = connectPostgre()
    user = getTelegramUser(conn, update.message.from_user.id)
    reply = "Hi! Registration started!"
    # if user:
    #     currentdata = "\nCurrent data:\n" \
    #                   f"ID number - {user[1]}\n" \
    #                   f"Name - {user[2]}\n" \
    #                   f"Surname - {user[3]}\n" \
    #                   f"Faculty - {user[4]}\n" \
    #                   f"Lichess - {user[5]}\n" \
    #                   f"Chess - {user[6]}\n" \
    #                   f"ELO FIDE - {user[7]}\n"
    #     reply = reply + currentdata
    #     context.user_data["ID Number"] = user[1]
    #     context.user_data["Name"] = user[2]
    #     context.user_data["Surname"] = user[3]
    #     context.user_data["Faculty"] = user[4]
    #     context.user_data["Lichess's nickname"] = user[5]
    #     context.user_data["Chess's nickname"] = user[6]
    #     context.user_data["FIDE_ELO"] = user[7]
    # else:
    #     context.user_data["Name"] = update.message.from_user.first_name
    #     context.user_data["Surname"] = update.message.from_user.last_name
    update.message.reply_text(reply+"\nClick on the following button to set things.\nWhen you are done, write done!", reply_markup=markup)
    return CHOOSING


def studentRegistrationRegularChoice(update, context):
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    reply = f'Your {text.lower()}? Yes, I would love to hear about that!'
    if text == 'ID Number':
        reply = reply + "\nBe careful, just the numbers!"
    update.message.reply_text(reply)

    return TYPING_REPLY


def studentRegistrationReceivedInformation(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']


    update.message.reply_text(
        "Neat! Just so you know, this is what I already know:"
        f"{facts_to_str(user_data)} You can tell me more, or change something\n\nWhen you finish, type Done .",
        reply_markup=markup,
    )

    return CHOOSING


def studentRegistrationDone(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    if str.lower(update.message.text)=='cancel':
        user_data.clear()
        update.message.reply_text(text=f"OK! Registration Canceled.",
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    conn = connectPostgre()
    insertStudent(conn, update.message.from_user.id, user_data.get("ID Number"), user_data.get("Name"), user_data.get("Surname"), user_data.get("Faculty"), user_data.get("Lichess nickname"), user_data.get("Chess nickname"), user_data.get("FIDE_ELO"))
    # s = getStudent(conn, update.message.from_user.id)
    conn.close()
    update.message.reply_text(text=f"Check the infos: ", reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END

