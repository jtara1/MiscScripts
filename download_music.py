import requests
from bs4 import BeautifulSoup as bs


url = 'http://ccmixter.org/api/query?tags=classical&sort=name'
response = requests.get(url)
print(response.text)

class CCMixterSongDownloader:
    def __init__(self):
        pass

    def download(self, tag='classical', sort='name', amount=10):
        query_url = 'http://ccmixter.org/api/query?'
        response = requests.get(query_url)
        soup = bs(response.text, 'lxml')
        print(soup.prettify())
        print('####################')

        for tag in soup.find_all('div', attrs={'class': 'upload_info'}):
            print(tag['about'])
            break

if __name__ == '__main__':
    # test
    dl = CCMixterSongDownloader()
    dl.download()