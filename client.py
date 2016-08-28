import argparse
import ipaddress
import requests
import datetime
import os


class Client(object):

    def __init__(self):
        os.system('clear')
        self.user_name = input('Please, add your user name to log in: ')

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
            self.server = {
                'host': ipaddress.ip_address(args.host),
                'port': args.port
            }
        except ValueError as e:
            print('The given host is not a valid IP address')
            exit(0)

        if not(1024 < self.server["port"] < 65535):
            print('The given port number is not in the range between 1024 and 65535!')
            exit(0)

        self.server["address"] = 'http://' + self.server["host"].compressed + ':' + str(self.server["port"])
        self.route = self.server["address"] + "/tweet"

        self.menu()

    def post_tweet(self, message):
        payload = {"content": str(message), "poster": self.user_name}
        requests.post(self.route, json=payload)

    @staticmethod
    def display_goodbye_message():
        print('\nThanks for using TWEETCOOL!\n')

    def menu(self):
        while True:
            try:
                option = input('''
---------------- TWITTERCOOL ------------------
{0}
Enter:
    tweet -- to post your thoughts;
    refresh -- to refresh the timeline;
    exit or CTRL+D -- to quit the application.
{0}

Option: '''.format(47*'-')).lower()

                if option == 'refresh':
                    os.system('clear')
                    r = requests.get(self.route)
                    requested_data = r.json()
                    print('>>> TIMELINE')
                    for tweet in requested_data:
                        print('>>>{0} <{1}>: {2}'.format(
                            tweet['poster'],
                            datetime.datetime.fromtimestamp(int(tweet['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                            tweet['content'])
                                                        )
                elif option == 'tweet':
                    try:
                        self.post_tweet(input('Post a tweet: '))
                    except UnicodeDecodeError as e:
                        print('Not Allowed Character Error: %s. Restart to post again.' % e)
                        exit()
                elif option == 'exit':
                    self.display_goodbye_message()
                    exit()
                else:
                    print('Not a valid option. Try again!')

            except EOFError:
                self.display_goodbye_message()
                exit()

            except KeyboardInterrupt:
                self.display_goodbye_message()
                exit()


client = Client()


