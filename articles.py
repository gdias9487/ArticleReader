import pandas as pd
import conversor
import pygame
import conversor
import io
import re

articles = pd.read_csv(conversor.articles['Body'])


def get_all_articles_title():
    titles = [x for x in articles['title']]
    return titles

def get_clean_article_title(title):
    teste = re.sub("[^A-Za-z0-9]","",title)
    return teste.lower()

def get_article_title_by_index(index):
    titles = [x for x in articles['title']]
    return titles[index]


def get_article_text_by_index(index):
    texts = [x for x in articles['text']]
    return texts[index]


def hear_article(text, title):
    return conversor.convert_to_speech(text, title)


def stream(title):
    if conversor.stream(title) is not False:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(conversor.stream(title))
        pygame.mixer.music.play(loops=0)
    else:
        return False


get_clean_article_title(get_article_title_by_index(23))