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
        name = r.find('a', itemprop='name codeRepository')
        description = r.find('p', itemprop='description')
        lang = r.find('span', itemprop='programmingLanguage')
        link = 'https://github.com/' + r.find('a', itemprop='name codeRepository').get('href')

        repo = {
            'name': name.text.rsplit('\n        ')[1],
            'desc': description.text if description else 'No description',
            'lang': lang.text if lang else 'No language',
            'link': link
        }

        context.append(repo)

    return context


@app.route('/')
def index():
    context = parser('https://github.com/h4cktivist?tab=repositories')
    return render_template('index.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
