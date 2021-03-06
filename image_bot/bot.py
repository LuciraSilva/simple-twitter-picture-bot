import os
import random
from os import getenv
from time import sleep
from typing import Union

from dotenv import load_dotenv
from twitter import Api

load_dotenv()

TWEET_BY_TWEET_INTERVAL = int(os.getenv('TWEET_BY_TWEET_INTERVAL'))

def save_or_read_last_mention_saved(method: str = 'r', content='') -> str:
    
    with open(getenv('DB_PATH'), method) as db:
        
        if method == 'w':
            db.write(str(content))
            return
        
        return db.read()
        
        
        
class Bot(object):
    
    def __init__(self):
        self.credentials = Api(consumer_key=getenv('CONSUMER_KEY'),
                      consumer_secret=getenv('CONSUMER_SECRET'),
                      access_token_key=getenv('ACCESS_TOKEN_KEY'),
                      access_token_secret=getenv('ACCESS_TOKEN_SECRET'))
    
        self.last_saved_mention_id = '' if not save_or_read_last_mention_saved() else int(save_or_read_last_mention_saved())
    
        self.screen_name = self.credentials.VerifyCredentials().screen_name
    
    def delete_tweets(self):
        statuses = self.credentials.GetUserTimeline(count=200)
        
        if statuses:
            [self.credentials.DestroyStatus(status.id) for status in statuses]
            print('Some tweets was deleted!')
                        
            return 
        
        print("There's no tweets to delete!")
        
    def filter_only_command_mentions(self, mentions):
        filtered_mentions = []
        
        for current_mention in mentions:
            if 'send a picture to' in current_mention.text.lower():
                filtered_mentions.append(current_mention)
                
        return filtered_mentions
    
    def check_if_exists_new_mentions(self) -> Union[tuple, bool]:
        
        current_mentions = self.credentials.GetMentions()
        
        if not current_mentions:
            return False
        
        if not self.last_saved_mention_id:
            
            self.last_saved_mention_id = current_mentions[0].id
            
            save_or_read_last_mention_saved(method='w', content=self.last_saved_mention_id)
        
            
        if current_mentions[0].id != self.last_saved_mention_id:
            for index in range(len(current_mentions)):
                
                if (current_mentions[index].id == self.last_saved_mention_id):
                    
                    missed_mentions = current_mentions[: index]
                        
                    self.last_saved_mention_id = current_mentions[0].id
                    
                    save_or_read_last_mention_saved(method='w', content=self.last_saved_mention_id)
                    
                    return (missed_mentions, True)

            self.last_saved_mention_id = current_mentions[0].id
                    
            save_or_read_last_mention_saved(method='w', content=self.last_saved_mention_id)
                                
        return False
        
    def get_addressed_users_screen_name(self, mentions) -> list:
        addressed_users = []
        for index in range(len(mentions)):
            
            screen_name = mentions[index].text.split('@')[-1][:-1].strip()
            if screen_name != self.screen_name:
                addressed_users.append(screen_name)
                
        return addressed_users
    
    def tweet_an_image_to_addressed_users(self, missed_mentions):

        addressed_users = self.get_addressed_users_screen_name(missed_mentions)
        images_name = os.listdir('./images')
        for user in addressed_users:
            
            default_message = 'Hi @{}! Someone sent a picture to you.'.format(user)
            
            chosen_image = random.choice(images_name)
        
            with open(f'images/{chosen_image}', 'rb') as img:
                self.credentials.PostUpdate(status=default_message, media=img)
                
            print('Tweet done!')
            sleep(TWEET_BY_TWEET_INTERVAL)
            
        return 

    

    
