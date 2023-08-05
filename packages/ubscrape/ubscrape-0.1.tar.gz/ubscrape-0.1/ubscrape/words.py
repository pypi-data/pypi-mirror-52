# internal to python
import re
from urllib.parse import unquote
from string import ascii_uppercase
from sqlite3 import IntegrityError

# external
import requests
from bs4 import BeautifulSoup


from .constants import BASE_URL
from .db import initialize_db

CON = initialize_db()


def write_words_for_letter(prefix: str, con):
    if not prefix:
        raise ValueError(f'Prefix {prefix} needs to be at least one letter.')

    def make_url():
        if page_num > 1:
            return f'{BASE_URL}/browse.php?character={letter}&page={page_num}'
        return f'{BASE_URL}/browse.php?character={letter}'

    letter = prefix.upper()

    page_num = con.execute(
        'SELECT max(page_num) FROM word WHERE letter = ?', (letter,)).fetchone()[0]

    if not page_num:
        page_num = 1

    url = make_url()
    req = requests.get(url)

    while req.url != 'https://www.urbandictionary.com/':
        soup = BeautifulSoup(req.text, features="html.parser")
        a_tags = soup.find_all('a', href=re.compile(r'/define.php'))

        pattern = re.compile(
            r'\/define\.php\?term=(.*)')

        links = [l['href'] for l in a_tags]

        encoded_words = [pattern.search(l).group(1)
                         for l in links if pattern.search(l)]

        words = [unquote(w) for w in encoded_words]

        formatted_words = [(w, 0, page_num, letter) for w in words]

        try:
            con.executemany(
                'INSERT INTO word(word, complete, page_num, letter) VALUES (?, ?, ?, ?)',
                formatted_words)
            con.commit()
        except IntegrityError:
            # IntegrityError normally occurs when we try to
            # insert words that are already in the database.
            pass

        print(
            f'Working on page {page_num} for {letter}. Total {140 * (page_num - 1) + len(words)} {letter} words.')

        page_num += 1
        url = make_url()
        req = requests.get(url)


def write_all_words():
    for letter in ascii_uppercase + '*':
        write_words_for_letter(letter, CON)
