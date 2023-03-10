import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import yaml
from os import path

load_dotenv()

client = MongoClient(f"mongodb+srv://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_URL']}/?retryWrites=true&w=majority")

db = client[os.environ['DB_NAME']]


def print_err(msg):
    print('\033[91m' + msg + '\033[0m')

def print_ignore(msg):
    print('\033[93m' + msg + '\033[0m')


# First query all available articles of DB
all_articles_codes = list(map(lambda x: x['code'], db.articles.find({ 'available' : True })))

added_articles_codes = []
# List all files in folder articles
for file_path in os.listdir('articles'):
    # check if current path is a file
    if os.path.isfile(os.path.join('articles', file_path)):
        article_path = path.join('.', 'articles', file_path)
        with open(article_path, "r", encoding='utf8') as stream:
            try:
                article_yaml = yaml.safe_load(stream)
                article = {}

                if 'code' not in article_yaml or not article_yaml['code']: raise Exception("Missing code")
                article['code'] = article_yaml['code']

                if 'available' not in article_yaml or 'available' not in article_yaml : raise Exception("Missing available")
                article['available'] = article_yaml['available']

                if 'date' not in article_yaml or 'date' not in article_yaml : raise Exception("Missing date")
                article['date'] = article_yaml['date']

                if 'title' not in article_yaml or 'title' not in article_yaml : raise Exception("Missing title")
                article['title'] = article_yaml['title']

                if 'thumbnail' in article_yaml and article_yaml['thumbnail']:
                    if (not path.exists(path.join('.', 'articles', 'images', article_yaml['thumbnail']))):
                        print_ignore(f"[{file_path}] error: {article_yaml['thumbnail']} file doesn't exists, solution: thumbnail ignored")
                    else : article['thumbnail'] = f'images/articles/{article_yaml["thumbnail"]}'
                
                if 'url' in article_yaml and article_yaml['url']:
                    article['url'] = article_yaml['url']
                
                elif 'content' in article_yaml and article_yaml['content']:
                    article['content'] = article_yaml['content']
                
                if 'summary' not in article_yaml or 'summary' not in article_yaml : raise Exception("Missing summary")
                article['summary'] = article_yaml['summary']

                db.articles.replace_one({ 'code' : article['code'] }, article, upsert=True)
                added_articles_codes.append(article['code'])

            except yaml.YAMLError as exc:
                print_err(f'[{file_path}] error: {exc}, solution: skipped ')
                continue

places_to_unavailable = list(filter(lambda x: x not in added_articles_codes, all_articles_codes))

if (len(places_to_unavailable) > 0):
    db.articles.update_many({ 'code' : { '$in' : places_to_unavailable } }, { '$set' : { 'available': False }})
    print(f'Made unavailable : {places_to_unavailable}')
