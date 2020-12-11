import datetime


def log_chat(usr_msg, bot_resp):
    with open("logs.txt", "a") as myfile:
        time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        myfile.write('[' + time + ']' + "USER: " + usr_msg)
        myfile.write('[' + time + ']' + "BOT: " + bot_resp)
        myfile.write("\n")
