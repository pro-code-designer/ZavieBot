import re
import Database as db
from typing import Final
from Makepdf import makepdf
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, filters, ContextTypes, Application


# Function to validate phone numbers
def validate_number(number):
    pattern = r'09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}'
    return re.match(pattern, number) is not None

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Function to validate names (supports both English and Persian names)
def validate_name(name):
    pattern1 = r'^[A-Za-z\s]+$'
    pattern2 = r'^[\u0600-\u06FF\s]+$'
    return (re.match(pattern1, name) is not None) or (re.match(pattern2, name) is not None)

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
TOKEN: Final = '6635980529:AAECa563vQWDpsXx73yTXDFjDOiQ3WZKjRk'
BOT_USERNAME: Final = 'ZzavieBot'

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to start the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to get help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to sign up
async def signup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Print user and chat information for debugging
    print(context._user_id, "\n", context._chat_id, context.args)
    i = 0
    name = ''
    fname = ''
    number = ''
    # Extracting name, last name, and phone number from the command arguments
    for item in context.args:
        if(item != ','):
            if(i == 0):
                name += item+' '
            elif(i == 1):
                fname += item+' '
            else:
                number = item
                break
        else:
            i += 1
    print(f"name ={name}  family name={fname}    phone number={number}")
    # Check if the user has already signed up
    if(db.get_by_id(context._user_id) != None):
        await update.message.reply_text('you signed up before.')
    # Validate and check the format of the entered name, last name, and phone number
    elif(not validate_name(name)):
        await update.message.reply_text(f'it is not a valid name you put {name} as a name!')
    elif (not validate_name(fname)):
        await update.message.reply_text(f'it is not a valid last name you put {fname} as a last name!')
    elif (not validate_number(number)):
        await update.message.reply_text(f'it is not a valid phone number you put {number} as a phone number!')
    else:
        # Add the user to the database
        db.add_user(context._user_id, name, fname, number)
        await update.message.reply_text('signed up successfully.')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to edit user information
async def edit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Print user and chat information for debugging
    print(context._user_id, "\n", context._chat_id, context.args)
    i = 0
    name = ''
    fname = ''
    number = ''
    # Extracting name, last name, and phone number from the command arguments
    for item in context.args:
        if(item != ','):
            if(i == 0):
                name += item+' '
            elif(i == 1):
                fname += item+' '
            else:
                number = item
                break
        else:
            i += 1
    print(f"name ={name}  family name={fname}    phone number={number}")
    # Check if the user has signed up before
    if(db.get_by_id(context._user_id) == None):
        await update.message.reply_text('sign up first')
    # Validate and check the format of the entered name, last name, and phone number
    elif(not validate_name(name)):
        await update.message.reply_text(f'it is not a valid name you put {name} as a name!')
    elif (not validate_name(fname)):
        await update.message.reply_text(f'it is not a valid last name you put {fname} as a last name!')
    elif (not validate_number(number)):
        await update.message.reply_text(f'it is not a valid phone number you put {number} as a phone number!')
    else:
        # Update user data in the database
        db.change_user_data(context._user_id, name, fname, number)
        await update.message.reply_text('edited successfully.')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to show user information
async def show_me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Retrieve user data from the database
    data = db.get_by_id(context._user_id)
    # Check if user data is available
    if(data != None):
        name = data[1]
        fname = data[2]
        number = data[3]
        permi = ''
        stay = ''
        if(data[4] == 1):
            permi = 'have permission'
        else:
            permi = 'do not have permissiont'
        if(data[5] == 1):
            stay = 'stay'
        else:
            stay = 'do not stay'
        # Display user information
        await update.message.reply_text(f'your name ={name}\nfamily name={fname}\nphone number={number}\nand you {permi} to stay in night and you {stay} tonight ')
    else:
        await update.message.reply_text(f'ther is no data for you make sure you signed up before!')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to change permission
async def permi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = context.args[0]
    data = db.get_by_number(number)
    if (not validate_number(number)):
        await update.message.reply_text(f'it is not a valid phone number you put {number} as a phone number!')
    elif(data != None):
        id = data[0]
        permi = data[4]
        if(permi != 1):
            permis = 'have permission'
            db.permi_night_stay(id, 1)
        else:
            permis = 'do not have permissiont'
            db.permi_night_stay(id, 0)
            if(data[5] == 1):
                db.tonight_stay(id, 0)
        await update.message.reply_text(f'phone number={number}\n{permis} to stay in night')
    else:
        await update.message.reply_text(f'ther is no data for the number you search!')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to change stay status
async def stay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = db.get_by_id(context._user_id)
    if(data != None):
        if(data[4] == 1):
            id = data[0]
            stay = data[5]
            if(stay != 1):
                stays = 'stay'
                db.tonight_stay(id, 1)
            else:
                stays = 'do not stay'
                db.tonight_stay(id, 0)
            await update.message.reply_text(f'you {stays} tonight')
        else:
            await update.message.reply_text(f'you dont have permission to stay at night')
    else:
        await update.message.reply_text(f'ther is no data for the number you search!')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to get a PDF containing all users
async def get_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = makepdf("All_User", db.get_all_user())
    if(ans):
        document = open("./All_User.pdf", "rb")
        await update.message.reply_document(document, "همه کاربران")

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to get a PDF containing users with permission
async def get_by_permission_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = makepdf("Permissioned_User", db.get_by_night_permi())
    if(ans):
        document = open("./Permissioned_User.pdf", "rb")
        await update.message.reply_document(document, "کاربرانی که اجازه شب ماندن دارند")

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Command to get a PDF containing users with night stay
async def get_by_night_stay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = makepdf("Night_Stay_User", db.get_by_night_stay())
    if(ans):
        document = open("./Night_Stay_User.pdf", "rb")
        await update.message.reply_document(document, "کاربرانی که شب می مانند")

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('signup', signup_command))
    app.add_handler(CommandHandler('edit', edit_command))
    app.add_handler(CommandHandler('show_me', show_me_command))
    app.add_handler(CommandHandler('change_permission', permi_command))
    app.add_handler(CommandHandler('change_stay', stay_command))
    app.add_handler(CommandHandler('get_all', get_all_command))
    app.add_handler(CommandHandler(
        'get_by_permission', get_by_permission_command))
    app.add_handler(CommandHandler(
        'get_by_night_stay', get_by_night_stay_command))

    # Messages

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the
    app.run_polling()
