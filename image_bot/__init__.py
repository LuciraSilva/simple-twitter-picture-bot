import os

from dotenv import load_dotenv

from .bot import Bot

load_dotenv()

if not os.path.isfile(os.getenv('DB_PATH')):
    with open(os.getenv('DB_PATH'), 'a') as db:
        db.write('')
        
if not os.path.exists(os.getenv('IMAGES_DIR')):
    os.mkdir(os.getenv('IMAGES_DIR'))    
        

