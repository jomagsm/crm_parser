import os

import requests
from bs4 import BeautifulSoup

from webapp.models import Lesson, User

main_url = 'http://crm.attractor-school.com'
url_sign = 'http://crm.attractor-school.com/users/sign_in'
url_link = 'http://crm.attractor-school.com/student/events/link_page'

def parse_site():
    with requests.Session() as s:
        user = User.objects.all().last()
        response_get = s.get(url_sign)
        soup = BeautifulSoup(response_get.content, "lxml")
        hidden = soup.find_all("input", {'type':'hidden'})
        target = url_sign
        payload = {x["name"]: x["value"] for x in hidden}
        login_csrf = soup.find("input", {"name": "authenticity_token"})['value']
        payload['utf8'] = "✓"
        payload['authenticity_token'] = login_csrf
        payload['user[login]'] = user.login
        payload['user[password]'] = user.password
        payload['user[remember_me]'] = 0
        payload['commit'] = 'Войти'
        response_post = s.post(target, data=payload)
        response_get = s.get(url_link)
        soup = BeautifulSoup(response_get.content, "lxml")
        links = soup.find_all('th', {'scope': 'row'})
        lesson_links = []
        webinar_links = []
        webinar_text = 'Вебинар'
        for i in links:
            text = i.text.split(' ')
            if webinar_text in text:
                webinar_links.append(main_url+i.find('a')['href'])
            else:
                lesson_links.append(main_url+i.find('a')['href'])
        for lesson in lesson_links:
            response_get = s.get(lesson)
            soup = BeautifulSoup(response_get.content, "lxml")
            lesson_name_div = soup.find_all('h1')
            p_link = soup.find_all('p')
            video_link = soup.find_all('a',{'class':'video_link'})
            text_link = 'Ссылка на теоретический материал: '
            for p in p_link:
                if text_link in p.text:
                    lesson_document_link = main_url+p.find('a')['href']
            lesson_name = lesson_name_div[0].text
            if video_link:
                youtube_link = video_link[0].text
            else:
                youtube_link = ''
            response_get = s.get(lesson_document_link)
            soup = BeautifulSoup(response_get.content, "lxml")
            links_document = main_url+soup.find_all('a',{'class':'btn btn-warning'})[0]['href']
            response_get = s.get(links_document)
            print(f'Парсинг {lesson_name}')
            print("Текущая деректория:", os.getcwd())
            with open(f'{os.getcwd()}/media/{lesson_name}.pdf', 'wb+') as f:
                f.write(response_get.content)
                f.close()
            Lesson.objects.create(lesson_name=lesson_name, file=f'{lesson_name}.pdf', video=youtube_link)