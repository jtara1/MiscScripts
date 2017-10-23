import requests
from bs4 import BeautifulSoup
import os
try:  # python 3
    from urllib.parse import quote, unquote
except ImportError:  # python 2
    from urllib import quote, unquote

from CCMixterSongDownloader.download_history_manager import History
from CCMixterSongDownloader.general_utility import slugify


class CCMixterSongDownloader:
    # needs tags, sort, limit, offset to be defined
    url_template = 'http://ccmixter.org/api/query?tags={tags}&sort={sort}&' \
                   'limit={limit}&offset={offset}'

    def __init__(self):
        pass

    def download(self, save_folder, tags='classical', sort='date', limit=1,
                 skip_previous_songs=True):
        """Downloads songs from ccMixter and saves them

        :param save_folder: location of saved music files
        :param tags: (string) in url, tags of songs used as a filter
        :param sort: (string) in url, sort type used to filter songs
        :param limit: (int) amount of songs to download before stopping
        :param skip_previous_songs: (boolean) if true, checks for previous
            queries made and skips the amount downloaded (as offset in url
            query filter).
        :return:
        """
        # location of music files downloaded
        save_folder = os.path.abspath(save_folder)

        if not skip_previous_songs:
            offset = 0
        else:
            _, offset = History.get_previous_download_amount(tags, sort,
                                                             save_folder)

        query_url = self.url_template.format(tags=tags, sort=sort, limit=limit,
                                             offset=offset)
        response = requests.get(query_url)
        soup = BeautifulSoup(response.text, 'lxml')

        # iterate over the HTML <div> tag that contains the direct link to .mp3
        for count, tag in enumerate(
                soup.find_all('div', attrs={'class': 'upload_info'}),
                start=1):
            print(tag['about'])
            file_name = tag['about']
            file_name = slugify(unquote(file_name))

            # we've downloaded enough songs to reach the limit
            if count >= offset - limit:
                break

            save_path = os.path.join(save_folder, file_name)
            CCMixterSongDownloader._direct_link_download(
                tag['about'].strip(),
                save_path)

        log_file_path = os.path.join(save_folder, History.log_file)
        History.history_log(log_file=log_file_path,
                            mode='write',
                            write_data=self._create_history_log_info(
                                tags, sort, limit))

    @staticmethod
    def _direct_link_download(url, full_save_path):
        """Saves the content from a URL that points directly to media

        :param url: (string) URL of the link whose content will be saved locally
        :param full_save_path: (string) local file path (with the file name)
        :return: 1 if url opened successfully, 0 otherwise
        """
        base_path = os.path.dirname(full_save_path)
        if not os.path.isdir(base_path):
            os.makedirs(base_path)

        r = requests.get(url)
        if r.ok:
            with open(full_save_path, 'wb') as f:
                f.write(r.content)
            return 1
        else:
            r.raise_for_status()
            return 0

    @staticmethod
    def _create_history_log_info(tags, sort, downloads):
        """Info stored when downloading complete to help skip songs already
        downloaded for future calls to download method.
        e.g.: {'classical+hip_hop': {'date': {'downloads': 10}}}
        """
        return {tags: {sort: {'downloads': downloads}}}

if __name__ == '__main__':
    # test
    dl = CCMixterSongDownloader()
    dl.download('test')
