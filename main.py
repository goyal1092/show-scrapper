from users import users, show_dict
from get_release_dates import get_release_dates
from send_sms import send_sms
import os
from get_torrent import get_torrent

available_dict = {}
for key in show_dict.keys():
    if os.path.isfile("/home/gaurav/workspace/show-scrapper/showdir/"+key+".txt"):
        print os.path.isfile("/home/gaurav/workspace/show-scrapper/showdir/"+key+".txt")
        f = open("/home/gaurav/workspace/show-scrapper/showdir/"+key+".txt", "r").read()
        if len(f) > 0:
            if f != "no info":
                available_dict[key] = get_torrent(key)
            else:
                get_release_dates(key)
                available_dict[key] = ""
            
        else:
            os.system("rm -rf "+"/home/gaurav/workspace/show-scrapper/showdir/"+key+".txt")
            get_release_dates(key)

    else:
        get_release_dates(key)
        os.system("python main.py")
print available_dict
for user in users:
    message = ""
    for show in user["shows"]:
        print available_dict[show]
        if available_dict[show]:
            print available_dict[show]
            message = message + "\n"+ available_dict[show]
            f = open("/home/gaurav/workspace/show-scrapper/showdir/"+show+".txt", "r").readlines()
            print f
            if f and f[0].split("\n")[0].strip() in available_dict[show]:
                new = open("/home/gaurav/workspace/show-scrapper/showdir/"+show+".txt", "wb")
                new.write("".join(f[1:]))
    print message
    if len(message):
        print "sending message"
        try:
            print "Sending message to : " + user["phone"]
            send_sms(user["phone"], message)
        except:
            send_sms(user["phone"], message)
    else:
        print "no message"
