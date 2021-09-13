import requests
import string
from bs4 import BeautifulSoup
import os
import re

# def get_script(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     div_title = soup.find('div', {'class': 'originalTitle'})
#     div_desc = soup.find('div', {'class' :'summary_text'})
#     title = div_title.text.strip()
#     description = div_desc.text.strip()
#     return creating_dict(title, description)
#
# def creating_dict(title, description):
#     movie_dict = {'title' : None, 'description' : None}
#     movie_dict['title'] = title
#     movie_dict['description'] = description
#     return movie_dict
#
# def url_validation(url):
#     if re.match('.*imdb.com/title*', url) is not None:
#         return True
#     else:
#         return False
#
# def main():
#     print('Input the URL:')
#     input_url = input()
#     if url_validation(input_url):
#         return get_script(input_url)
#     else:
#         return "Invalid movie page!"
#
# print(main())

# import requests
#
# def writing_to_file(page_content_request):
#     file = open('source.html', 'wb')
#     file.write(page_content_request)
#     file.close()
#
# def request_code(url):
#     r = requests.get(url)
#     if r:
#         page_content_request = requests.get(url).content
#         writing_to_file(page_content_request)
#         return 'Content saved.'
#     else:
#         return f'The URL returned {r.status_code}!'
#
# def main():
#     print("Input the URL:")
#     url = input()
#     return request_code(url)
#
# print(main())

# list_articles = []
#
# def formatting_title(article_title, article_content):
#     article_without_punctuation = ''
#     for letter in article_title:
#         if letter in string.punctuation:
#             article_without_punctuation = article_title.replace(letter, '')
#     article_with_underscores = article_without_punctuation.replace(' ', '_')
#     saving_content_to_file(article_with_underscores, article_content)
#
# def saving_content_to_file(article_title, article_content):
#     file = open(f'{article_title}.txt', 'w', encoding='utf-8')
#     file.write(article_content)
#     file.close()
#
# def looking_for_tag(article_link):
#     r = requests.get('https://www.nature.com'+article_link)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     div_tag_art_type = soup.find('div', {'class' : 'article__type'})
#     if div_tag_art_type != None:
#         for index, el in enumerate(div_tag_art_type):
#             if index == 0:
#                 if (el.strip()) == 'NEWS':
#                     article_title = soup.find('h1', {'class': 'article-item__title'})
#                     article_body = soup.find('div', {'class' : 'article__body cleared'})
#                     article_content = article_body.find_all(['p','h2'])
#                     article_content_joined = ''
#                     for content in article_content:
#                         article_content_joined += content.text.replace('\n','')
#                     formatting_title(article_title.text, article_content_joined)
#
# def get_script():
#     r = requests.get('https://www.nature.com/nature/articles')
#     soup = BeautifulSoup(r.content, 'html.parser')
#     all_articles_links = soup.find_all('a', {'data-track-action' : "view article"})
#     for i in all_articles_links:
#         article_link = i.get('href')
#         looking_for_tag(article_link)
#
# def main():
#     return get_script()
#
# main()

# def formatting_title(article_title, article_content):
#     article_without_punctuation = article_title.strip()
#     for letter in article_title:
#         if letter in string.punctuation:
#             article_without_punctuation = article_without_punctuation.replace(letter, '')
#     article_with_underscores = article_without_punctuation.replace(' ', '_')
#     saving_content_to_file(article_with_underscores, article_content)
#
# def folder_creation(folder_number):
#     os.mkdir(f'Page_{folder_number}')
#
# def changing_directory():
#     os.chdir(os.getcwd()+f'\Page_{page_no.value}')
#     os.path.dirname(os.getcwd())
#
# def saving_content_to_file(article_title, article_content):
#     changing_directory()
#     file = open(f'\'{article_title}.txt', 'w', encoding='utf-8')
#     file.write(article_content)
#     file.close()
#     os.chdir(os.path.dirname(os.getcwd()))
#
# def article_verification(article_link):
#     r = requests.get('https://www.nature.com' + article_link)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     article_title = ''
#     article_content = ''
#     if soup.find('h1', {'class': ['article-item__title', 'c-article-title']}) is not None:
#         article_title = soup.find('h1', {'class': ['article-item__title', 'c-article-title']})
#         article_body = soup.find('div', {'class': ['article__body cleared', 'c-article-body']})
#         article_content = article_body.find_all(['p', 'h2', 'h3'])
#     elif soup.find('div', {'id': ['content', 'animation-wrapper']}) is not None:
#         article_title = soup.find('h1', {'class': ['heading entry-title', 'page-title']})
#         article_body = soup.find('div', {'class': ['entry-content', 'milestones-wrapper']})
#         article_content = article_body.find_all(['p', 'h2'])
#     return article_title, article_content
#
# def article_scraping(article_link):
#     article_title, article_content = article_verification(article_link)
#     article_content_joined = ''
#     for content in article_content:
#         article_content_joined += content.text.replace('\n','')
#     formatting_title(article_title.text, article_content_joined)
#
# def page_scraping(page, article_type):
#     x = article_type.replace(' ', '+')
#     r = requests.get(f'https://www.nature.com/search?q={x}&page={str(page)}')
#     soup = BeautifulSoup(r.content, 'html.parser')
#     all_articles_links = soup.find_all('a', {'data-track-action' : "search result"})
#     for article in all_articles_links:
#         article_link = article.get('href')
#         article_scraping(article_link)
#
# class Counter:
#     def __init__(self):
#         self.value = 0
#     def number(self):
#         self.value += 1
#
# page_no = Counter()
#
# def main():
#     page = (int(input()))
#     article_type = input()
#     for i in range(1, page+1):
#         page_no.number()
#         folder_creation(page_no.value)
#         page_scraping(i, article_type)
# main()

class Counter:
    def __init__(self):
        self.value = 0
    def number(self):
        self.value += 1

page_no = Counter()
header_no = Counter()

def formatting_title(article_title, article_content):
    article_without_punctuation = article_title.strip()
    for letter in article_title:
        if letter in string.punctuation:
            article_without_punctuation = article_without_punctuation.replace(letter, '')
    article_with_underscores = article_without_punctuation.replace(' ', '_')
    saving_content_to_file(article_with_underscores, article_content)

def folder_creation(folder_number):
    os.mkdir(f'Page_{folder_number}')

def changing_directory():
    os.chdir(os.getcwd()+f'\Page_{page_no.value}')
    os.path.dirname(os.getcwd())

def saving_content_to_file(article_title, article_content):
    changing_directory()
    file = open(f'{article_title}.txt', 'w', encoding='utf-8')
    file.write(article_content)
    file.close()
    os.chdir(os.path.dirname(os.getcwd()))

def article_parsing(article_link):
    r = requests.get('https://www.nature.com' + article_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    article_content = ''
    if soup.find('div', {'class': ['article-item__body', 'article__body cleared']}) is not None:
        article_item_body = soup.find('div', {'class': 'article-item__body'})
        article_content = article_item_body.find_all('p')
    elif soup.find('div', {'id': ['content', 'animation-wrapper']}) is not None:
        article_body = soup.find('div', {'class': ['entry-content', 'milestones-wrapper']})
        article_content = article_body.find_all(['p', 'h2'])
    return article_content

def article_scraping(article_link, article_title):
    article_content = article_parsing(article_link)
    article_content_joined = ''
    for content in article_content:
        article_content_joined += content.text.replace('\n','')
    formatting_title(article_title, article_content_joined)

def page_scraping(page, article_type):
    request_for_page = requests.get(f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page}')
    soup = BeautifulSoup(request_for_page.content, 'html.parser')
    article_rows = soup.find_all('li', {'class' : 'app-article-list-row__item'})
    for row in article_rows:
        article_header = row.find('span', {'class' : 'c-meta__type'})
        if article_header.text == article_type:
            article_link = row.find('a', {'class' : 'c-card__link u-link-inherit'})
            get_article_link = article_link.get('href')
            article_title = article_link.text
            article_scraping(get_article_link, article_title)

def main():
    page = (int(input()))
    article_type = input()
    for i in range(1, page+1):
        page_no.number()
        folder_creation(page_no.value)
        page_scraping(i, article_type)

main()
