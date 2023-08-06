from .model import Anime, Character

import requests
from bs4 import BeautifulSoup

import time
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count


class MALScraper:
    """Scrapes https://myanimelist.net/ using BeautifulSoup4.

    Methods
    -------
    get_anime(anime), get_anime_url(anime)
    """

    def __init__(self):
        # MAL search url
        self.MAL_ANIME_URL = 'https://myanimelist.net/anime.php?q='
        self.MAL_CHAR_URL = 'https://myanimelist.net/character.php?q='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }

    def get_anime(self, anime):
        """Gets the anime model data.

        Parameters
        ----------
        anime : str
            Name of the anime.

        Returns
        -------
        class Anime
            Returns the scraped anime model data.
        """

        # Gets the anime url.
        anime_url = self.get_anime_url(anime)

        return Anime(anime_url)

    def get_anime_url(self, anime):
        """Gets the url of the anime from the website.

        Parameters
        ----------
        anime : str
            Name of the anime.

        Returns
        -------
        str
            Returns the anime url link.
        """
        url = self.MAL_ANIME_URL + anime

        res = requests.get(url, headers=self.headers)
        while res.status_code != 200:
            print(res.status_code)
            time.sleep(1)
            res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, features='lxml')
        lnk = None
        try:
            a = soup.find('a', {'class': 'hoverinfo_trigger fw-b fl-l'})
            lnk = a['href']
        except Exception as e:
            print(f'Error getting anime url.\nError: {e}')
        return lnk

    def get_all_anime(self, start=0, to=16150):
        """Gets all the anime from the website. Each anime has kind of index based pointer.

        Parameters
        ----------
        start : int
            Start point of the anime. Starts at 0.
        to : int
            End point of the anime. Ends at 16100.

        Returns
        -------
        str
            Returns the anime url link.
        """
        if to % 50 != 0 or to > 16150:
            raise ValueError(
                'Value of parameter to must be divisible by 50, or less than or equal to 16100.')

        total_anime = to - 50
        count = start
        links = []

        while count <= total_anime:
            url = f'https://myanimelist.net/topanime.php?limit={count}'
            print(f'Parsing {url} ...')
            res = requests.get(url, headers=self.headers)

            while res.status_code != 200:
                print(res.status_code)
                time.sleep(1)
                res = requests.get(url, headers=self.headers)

            soup = BeautifulSoup(res.text, features='lxml')

            try:
                aa = soup.find_all(
                    'a', {'class': 'hoverinfo_trigger fl-l fs14 fw-b'})

                for a in aa:
                    link = a['href']

                    if link:
                        links.append(link)
            except Exception as e:
                print(e)

            count += 50

        print(f'Scraping animes total of {len(links)}')

        with ThreadPool(cpu_count()) as p:
            animes = p.map(Anime, links)

        return animes

    def get_character(self, name):
        """Gets the character model data.

        Parameters
        ----------
        name : str or int
            Name of the character.

        Returns
        -------
        class Character
            Returns the scraped character model data.
        """

        # Gets the character url.
        char_url = self.get_character_url(name)

        if char_url is None:
            print(f'{name} not found.')
            return None

        return Character(char_url)

    def get_character_url(self, name):
        """Gets the url of the character from the website.

        Parameters
        ----------
        name : str or int
            Name of the character.

        Returns
        -------
        str
            Returns the character url link.
        """
        url = self.MAL_CHAR_URL + str(name)

        res = requests.get(url, headers=self.headers)
        while res.status_code != 200:
            print(res.status_code)
            time.sleep(1)
            res = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(res.text, features='lxml')
        lnk = None

        try:
            a = soup.find('div', {'id': 'content'}).find('table', {
                'width': '100%', 'cellspacing': '0', 'cellpadding': '0', 'border': '0'}).find('td', {'width': '175'}).find('a')
            lnk = a['href']
        except Exception as e:
            print(f'Error getting character url.\nError: {e}')

        return lnk

    def get_all_characters(self, start=0, to=10000):
        if to % 50 != 0 or to > 16150:
            raise ValueError(
                'Value of parameter to must be divisible by 50, or less than or equal to 16100.')

        total_anime = to - 50
        count = start
        links = []

        while count <= total_anime:
            url = f'https://myanimelist.net/character.php?limit={count}'
            print(f'Parsing {url} ...')
            res = requests.get(url, headers=self.headers)

            while res.status_code != 200:
                time.sleep(1)
                res = requests.get(url, headers=self.headers)

            soup = BeautifulSoup(res.text, features='lxml')

            try:
                aa = soup.find('div', {'id': 'content'}).find_all(
                    'a', {'class': 'fs14 fw-b'})

                for a in aa:
                    link = a['href']

                    if link:
                        links.append(link)
            except Exception as e:
                print(e)

            count += 50

        with ThreadPool(cpu_count()) as p:
            chars = p.map(Character, links)

        return chars
