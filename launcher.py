import os
import runpy
from time import sleep

from twitter.error import TwitterError

from image_bot import Bot

if __name__ == '__main__':
    
    bot = Bot()
    
    while True:
            
        try:
                        
            new_mentions = bot.check_if_exists_new_mentions()
            
            if new_mentions:
                
                command_mentions = bot.filter_only_command_mentions(new_mentions[0])
                
                bot.tweet_an_image_to_addressed_users(command_mentions) 
                
            print('>> Chillin! <<')
            sleep(int(os.getenv('SLEEP_TIME')))
        
        except TwitterError as e:
            
            if e[0]['code'] == 88:
                
                runpy.run_path(path_name='launcher.py')
