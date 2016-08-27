import argparse
import ipaddress
import requests
import datetime
import os


parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host",
                    help="IP address of the Tweetcool server",
                    default='127.0.0.1')  # Equals 'localhost'
parser.add_argument("-P", "--port",
                    help="Post used by the Tweetcool server",
                    type=int,
                    default=9876)
args = parser.parse_args()

try:
    server = {
        'host': ipaddress.ip_address(args.host),
        'port': args.port
    }
except ValueError as e:
    print('The given host is not a valid IP address')
    exit(0)

if not(1024 < server["port"] < 65535):
    print('The given port number is not in the range between 1024 and 65535!')
    exit(0)

server["address"] = 'http://' + server["host"].compressed + ':' + str(server["port"])

# Logic starts here... somewhere..

os.system('clear')

print('''---------------- TWITTERCOOL ------------------''')

while True:
    try:
        option = input('''{0}
Enter:
    tweet -- to post your thoughts;
    refresh -- to refresh the timeline;
    exit or CTRL+D -- to quit the application.
{0}

Option: '''.format('-'*47)).lower()

        if option == 'refresh':
            get_request = requests.get(server['address'] + '/tweet')
            requested_incoming_data = get_request.json()
            os.system('clear')
            print('>>> TWEETCOOL TIMELINE')
            for tweet in requested_incoming_data:
                print('''>>> {0} <{1}>: {2}'''.format(
                    tweet['poster'],
                    datetime.datetime.fromtimestamp(int(tweet['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                    tweet['content']
                                                     )
                      )

        elif option == 'tweet':
            user_name = input('\nPlease, enter your user name to log in: ')
            tweet = input('Post: ')
            post_request = requests.post(server['address'] + '/tweet', json={"content": tweet,
                                                                             "poster": user_name
                                                                            }
                                         )
        elif option == 'exit':
            print('''Thanks for using TWEETCOOL!
''')
            break
        else:
            print('Not a valid option. Try again!')

    except EOFError:
        print('''
Thanks for using TWEETCOOL!
            ''')
        break






