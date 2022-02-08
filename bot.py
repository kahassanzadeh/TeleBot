import telegram.ext
import os
import logging

PORT = int(os.environ.get('PORT',5000))



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open('token.txt','r') as f:
    TOKEN = f.read()

listOfChatsText = dict()
listOfChatsIDs = dict()
listOfSuggestions = dict()
messageIdChatId = dict()

bot = telegram.Bot(TOKEN)



def start(update, context):
    update.message.reply_text("Hello! Welcome to NeuralBot")
    listOfChatsIDs[update.message.chat_id] = 0
    print(update.message.chat_id)

def help(update, context):
    update.message.reply_text("""
    The Following commands are available:

    /start -> Welcome Message
    /help -> This Message
    /content -> Info about 
    /contact -> Contact

    """)

def contact(update, context):
    """This function will initiate the values or storing and handling the bot response"""

    global listOfChatsIDs,listOfChatsText,bot
    id = update.message.chat_id
    listOfChatsIDs[id] = "contact_0"
    listOfChatsText[id] = ""
    bot_welcome = """
    با سلام به ربات انجمن علمی مهندسی مواد و متالورژی دانشگاه صنعتی امیر کبیر خوش آمدید

    با تشکر از شما برای زمانی که برای پیشنهادات و انتقادات میگذارید
    همچنین از این طریق میتوانید اگر سوالی دارید نیز بپرسید.
    پیام بعدی شما به صورت خودکار و ناشناس به انجمن علمی انتقال داده میشود و در اسرع وقت نیز پاسخ آن به شما داده خواهد شد.
    با تشکر

    """
    bot.sendMessage(chat_id = id,text = bot_welcome)
    pass

def handle_contact(update,context):
    global listOfChatsText,listOfChatsIDs,bot,listOfSuggestions,messageIdChatId

    id = update.message.chat_id
    
    if id != -625033197 and listOfChatsIDs[id] == "contact_0" :
        listOfChatsText[id] = (update.message.text).replace("\n"," ")
        message = bot.sendMessage(chat_id = -625033197,text = listOfChatsText[id])
        listOfSuggestions[message.message_id] = message
        messageIdChatId[id] = message.message_id


    if id == -625033197:
        msg = update.message.reply_to_message
        idForReplying = find_ID(msg.message_id)
        bot.sendMessage(chat_id = idForReplying, text = update.message.text)
        listOfChatsText[idForReplying] = ""
        listOfChatsIDs[idForReplying] = 0

    pass

def find_ID(msg_id):
    global messageIdChatId
    for key in messageIdChatId:
        if messageIdChatId[key] == msg_id:
            return key




def main():
    
    updater = telegram.ext.Updater(TOKEN, use_context=True)

    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start",start))
    disp.add_handler(telegram.ext.CommandHandler("help",help))
    disp.add_handler(telegram.ext.CommandHandler("contact",contact))
    disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,handle_contact))


    updater.start_webhook(listen="0.0.0.0",
                        port= int(PORT),
                        url_path=TOKEN)


    updater.bot.setWebhook('https://enigmatic-hamlet-56713.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
    
