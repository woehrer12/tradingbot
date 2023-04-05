import helper.sqlmanager
import helper.config
import logging

conf = helper.config.initconfig()
Token = conf['telegramtoken']

helper.sqlmanager.init()

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

START, LOGIN, CONFIG, CHANGE_STRATEGY, CHANGE_HYPEROPT_LOSS, CHANGE_EPOCHS, CHANGE_TIMEFRAME, CHANGE_TIMERANGE_DAYS = range(8)

start_keyboard = [
    ["/create_account", "/login"],
    ["/cancel","/start"]
]
new_keyboard = [
    ["/start"]]
login_keyboard = [
    ["/account_info","/hyperopting"],
    ["/config"],
    ["/cancel","/start"]
]

markup = ReplyKeyboardMarkup(start_keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    user = update.message.from_user
    await update.message.reply_text(
        "Hi {}! Welcome to Trading4Live.\n" 
        "Your User ID is: {}\n"
        "for registration press /create_account".format(user['first_name'], user['id']),
        reply_markup=ReplyKeyboardMarkup(start_keyboard),
    )
    return START

async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    check = helper.sqlmanager.createuser(update.message.from_user['id'])
    if check == True:
        await update.message.reply_text("Account created successfully!")
        logging.info("Account created successfully! " + update.message.from_user['id'] + " " + update.message.from_user['first_name'])
        return LOGIN
    else:
        await update.message.reply_text("Account alredy exist!")
        return START


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    check = helper.mysql.requestuser(update.message.from_user.id)
    if check == None:
        await update.message.reply_text("Account not exist!")
        return START
    else:
        await update.message.reply_text("You are logged in!\n Start with /config to change your strategy\n then /hyperopting to start the hyperopt\n for search the best strategy",
            reply_markup=ReplyKeyboardMarkup(login_keyboard))
        return LOGIN

async def back_to_login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Back to Login",
        reply_markup=ReplyKeyboardMarkup(login_keyboard))
    return LOGIN


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Byebye!",
        reply_markup=ReplyKeyboardMarkup(new_keyboard),
    )

    return ConversationHandler.END




def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Token).build()


    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [ # First, the user is asked to select the category of the info they want to learn
#                CommandHandler("bitcoin", bitcoin),
#                CommandHandler("ethereum", ethereum),
                CommandHandler("create_account", create_account),
                CommandHandler("login", login),
            ],
            LOGIN: [
#                CommandHandler("account_info", account_info),
#                CommandHandler("hyperopting", hyperopting),
#                CommandHandler("config",config)
            ],
            CONFIG:[
#                CommandHandler("change_strategy", change_strategy),
#                CommandHandler("change_hyperopt_loss", change_hyperopt_loss),
#                CommandHandler("change_hyperoptepochs", change_hyperoptepochs),
#                CommandHandler("change_hyperopt_timeframe", change_hyperopt_timeframe),
#                CommandHandler("change_hyperopt_timerange_days", change_hyperopt_timerange_days),
                CommandHandler("back", back_to_login),
            ],
            CHANGE_STRATEGY: [
                CommandHandler("cancel", cancel),
#                MessageHandler(filters.Text(), change_strategy2)
            ],
            CHANGE_HYPEROPT_LOSS: [
                CommandHandler("cancel", cancel),
#                MessageHandler(filters.Text(), change_hyperopt_loss2)
            ],
            CHANGE_EPOCHS: [
                CommandHandler("cancel", cancel),
#                MessageHandler(filters.Text(), change_hyperoptepochs2)
            ],
            CHANGE_TIMEFRAME: [
                CommandHandler("cancel", cancel),
#                MessageHandler(filters.Text(), change_hyperopt_timeframe2)
            ],
            CHANGE_TIMERANGE_DAYS: [
                CommandHandler("cancel", cancel),
#                MessageHandler(filters.Text(), change_hyperopt_timerange2)
            ],
            
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
