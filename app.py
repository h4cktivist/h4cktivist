from flask import Flask, render_template

import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


def parser(url):
    context = []

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    all_repos = soup.find_all('div', class_='col-10 col-lg-9 d-inline-block')

    for r in all_repos:
        if r.find('p', itemprop='description') is not None:
            desc = r.find('p', itemprop='description').text
        else:
            desc = 'No description'

        repo = {
            'name': r.find('a', itemprop='name codeRepository').text.rsplit('\n        ')[1],
            'desc': desc,
            'lang': r.find('span', itemprop='programmingLanguage').text,
            'link': 'https://github.com/' + r.find('a', itemprop='name codeRepository').get('href')
        }

        context.append(repo)

    return context


@app.route('/')
def index():
    context = parser('https://github.com/h4cktivist?tab=repositories')
    return render_template('index.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
