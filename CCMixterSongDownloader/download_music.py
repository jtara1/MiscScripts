import requests
from bs4 import BeautifulSoup as bs
import os

from CCMixterSongDownloader.download_history_manager import History
from CCMixterSongDownloader.general_utility import slugify

class CCMixterSongDownloader:
    # needs tags, sort, limit, offset to be defined
    url_template = 'http://ccmixter.org/api/query?tags={tags}&sort={sort}&' \
                   'limit={limit}&offset={offset}'

    def __init__(self):
        pass

    def download(self, save_folder, tags='classical', sort='date', limit=10,
                 skip_previous_songs=True):
        save_folder = os.path.abspath(save_folder)

        if skip_previous_songs:
            offset = 0
        else:
            _, offset = History.get_previous_download_amount(tags, sort,
                                                             save_folder)

        query_url = self.url_template.format(tags=tags, sort=sort, limit=limit,
                                             offset=offset)
        response = requests.get(query_url)
        soup = bs(response.text, 'lxml')
        print(soup.prettify())
        print('####################')

        for tag in soup.find_all('div', attrs={'class': 'upload_info'}):
            print(tag['about'])
            save_path = os.path.join(save_folder, slugify(tag['about']))
            self._direct_link_download(tag['about'], save_path)

    @staticmethod
    def _direct_link_download(url, full_save_path):
        base_path = os.path.dirname(full_save_path)
        if not os.path.isdir(base_path):
            os.makedirs(base_path)

        with open(full_save_path, 'wb') as f:
            r = requests.get(url)
            f.write(r.content)

if __name__ == '__main__':
    # test

    dl = CCMixterSongDownloader()
    dl.download('test')
