import os, requests
import time
import datetime

USERID = ''
API_ENDPOINT = 'https://asia-east2-toaster-253815.cloudfunctions.net/message'

def toast(method):
    if USERID == '':
        raise UnboundLocalError('Run set_id(<telegram id>) first!')

    def insert_toast(*args, **kw):      
        try:
            start = datetime.datetime.now()
            result = method(*args, **kw)
            end = datetime.datetime.now()
            diff = start - end
            # Create Message
            msg = "🍞 Ding! Function `{}` has completed!\n*Start Time:* {}\n*End Time:* {}\n*Time Taken:* {}".format(
                method.__name__, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"), format_time(diff)
            )
            data = {
                'userid':USERID,
                'msg':msg
            }

            res = requests.post(url = API_ENDPOINT, data = data)
            return result

        except Exception as e:
            msg = '⚠️ An error has occurred with function `{}`\n*Error message:*{}'.format(method.__name__, str(e))
            print('Error caught:',e)
            data = {
                'userid':USERID,
                'msg':msg
            }
            # Send Telegram Message
            res = requests.post(url = API_ENDPOINT, data = data)

    return insert_toast

def set_id(userid):
    if userid.isnumeric():
        global USERID
        USERID = userid
    else:
        raise TypeError('Your Telegram ID should be all numbers.')

def format_time(time_diff):
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return '{} days, {} hours, {} mins, {} sec'.format(days, int(hours), int(minutes), seconds)
    return '{} hours, {} mins, {} sec'.format(int(hours), int(minutes), seconds)


    