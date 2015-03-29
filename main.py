from users import users, show_dict
from get_release_dates import get_release_dates
from send_sms import send_sms
import os
from get_torrent import get_torrent

available_dict = {}
for key in show_dict.keys():
    if os.path.isfile(key+".txt"):
        print os.path.isfile(key+".txt")
        f = open(key+".txt", "r").read()
        if len(f) > 0:
            available_dict[key] = get_torrent(key)
            
        else:
            os.system("rm -rf "+key+".txt")
            get_release_dates(key)
            os.system("python main.py")

    else:
        get_release_dates(key)
        os.system("python main.py")
print available_dict
for user in users:
    message = ""
    for show in user["shows"]:
        if available_dict[show]:
            message = message + "\n"+ available_dict[show]
            f = open(show+".txt", "r").readlines()
            if f[0].replace("\n", "") in available_dict[show]:
                new = open(show+".txt", "wb")
                new.write("".join(f[1:]))

    if len(message):
        print "sending message"
        # try:
        #     print "Sending message to : " + user["phone"]
        #     send_sms(user["phone"], message)
        # except:
        #     send_sms(user["phone"], message)
    else:
        print "no message"