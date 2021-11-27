import pandas as pd
import conversor
import pygame
import conversor
import io

articles = pd.read_csv(conversor.articles['Body'])


def get_all_articles_title():
    titles = [x for x in articles['title']]
    return titles


def get_article_title_by_index(index):
    titles = [x for x in articles['title']]
    return titles[index]


def get_article_text_by_index(index):
    texts = [x for x in articles['text']]
    return texts[index]


def hear_article(text, title):
    return conversor.convert_to_speech(text, title)


def stream(index):
    if conversor.stream(str(index)) is not False:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(conversor.stream(str(index)))
        pygame.mixer.music.play(loops=0)
    else:
        return False


def play_article(index):
    try:
        pygame.mixer.music.load(f"D:\PythonProjects\pj1\PISI4\mp3/{index}.mp3")
        pygame.mixer.music.play(loops=0)
    except:
        return False
    
