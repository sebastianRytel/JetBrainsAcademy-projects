import requests
from bs4 import BeautifulSoup
import re

def get_script(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    div_title = soup.find('div', {'class': 'originalTitle'})
    div_desc = soup.find('div', {'class' :'summary_text'})
    title = div_title.text.strip()
    description = div_desc.text.strip()
    return creating_dict(title, description)

def creating_dict(title, description):
    movie_dict = {'title' : None, 'description' : None}
    movie_dict['title'] = title
    movie_dict['description'] = description
    return movie_dict

def url_validation(url):
    if re.match('.*imdb.com/title*', url) is not None:
        return True
    else:
        return False

def main():
    print('Input the URL:')
    input_url = input()
    if url_validation(input_url):
        return get_script(input_url)
    else:
        return "Invalid movie page!"

print(main())

# import requests
# import json
# from bs4 import BeautifulSoup
#
# def get_script(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     for script in soup.find_all('script'):
#         if script.get('type') == 'application/ld+json':
#             return json.loads(str(script)[35:-9])
#
# def parsing_json(input_url):
#     dict_title_descr = {"title": None, 'description' : None}
#     jsoned = get_script(input_url)
#     dict_title_descr['title'] = jsoned['name']
#     for key, value in jsoned.items():
#         print(key, value)
#     return dict_title_descr
#
# def main():
#     print('Input the URL:')
#     input_url = input()
#     return parsing_json(input_url)
#
# print(main())
