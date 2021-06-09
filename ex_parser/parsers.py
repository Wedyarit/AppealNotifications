import bs4
import json
import requests

from utils.appeal import Appeal


def appeals():
    cookies = json.loads(open('ex_parser/cookies.json', 'r').read())
    soup = bs4.BeautifulSoup(requests.get(url='https://excalibur-craft.ru/index.php?do=appeals&go=new', cookies=cookies).text, 'html.parser')

    _appeals = []
    for tr in soup.find('table', {'class': 'table table-bordered mb-0'}).find('tbody').find_all('tr'):
        tds = list(map(lambda x: x.text, tr.find_all('td')))
        if len(tds) == 0:
            return None
        _appeals.append(Appeal(id=tr.find('th').text, violator=tds[0], server=tds[1], date=tds[3]))

    return _appeals


def fill_in_appeals(appeals_: [Appeal]):
    cookies = json.loads(open('ex_parser/cookies.json', 'r').read())
    for appeal in appeals_:
        soup = bs4.BeautifulSoup(requests.get(url=f'{appeal.url}', cookies=cookies).text, 'html.parser')
        appeal.author = soup.findAll('tr')[-1].find('td').text
