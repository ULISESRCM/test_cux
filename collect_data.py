import sys
from scrape import *

chat_name = "" #sys.argv[-1] #'\xe0\xa4\xac\xe0\xa5\x80\xe0\xa4\x9c\xe0\xa5\x87\xe0\xa4\xaa\xe0\xa5\x80 \xe0\xa4\xae\xe0\xa5\x80\xe0\xa4\xa1\xe0\xa4\xbf\xe0\xa4\xaf\xe0\xa4\xbe \xe0\xa4\xb0\xe0\xa5\x80\xe0\xa4\xb5\xe0\xa4\xbe'
locate_chat(chat_name)
all_chats = scroll_to_top()

run_scraper()