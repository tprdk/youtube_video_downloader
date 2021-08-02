from video_caption_download import download_video_and_caption, download_playlist
from crawl_website import configure_chrome_driver, crawl
from multiprocessing import Process, Queue
import time
from dl_downloader import download_with_dl

EXAMPLE = False
CHROME_DRIVER_PATH = 'chromedriver_win32/chromedriver.exe'

def example():
    '''
    Bu fonksiyon son değişiklikten sonra çalışmıyor.
    Yerine dl_downloader içerisindeki youtube_dl api kullanılıyor.
    :return:
    '''
    print('Example :')
    video_url = 'https://www.youtube.com/watch?v=tIeHLnjs5U8&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=4&t=3s'
    download_video_and_caption(video_url, 'video.srt', 'en')

    playlist_url = 'https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi'
    download_playlist(playlist_url, 'playlist_video', 'en')

    auto_generated_caption_url = 'https://www.youtube.com/watch?v=_kSvE7ldoc4'
    download_video_and_caption(auto_generated_caption_url, 'agadmator.srt', 'a.en')


def download(url_queue):
    '''
    Sonsuz bir döngü içerisinde indirilmek istenen bir url var ise kuyruğu kontrol eder.
    Var ise url'e sahip dosya indirilir.
    :param url_queue:
    :return:
    '''
    while True:
        url = url_queue.get()
        if url != 'DONE':
            download_with_dl(url, 'download', 'en')
        else:
            break


def main(driver, url):
    url_queue = Queue()

    downloader_process = Process(target=download, args=(url_queue,))
    downloader_process.daemon = True
    downloader_process.start()

    crawl(driver, url, url_queue)
    downloader_process.join()


if __name__ == '__main__':
    if EXAMPLE:
        example()
    else:
        '''
        search_keyword : youtube üzerinden aranmak istenilen keyword 
        '''
        driver = configure_chrome_driver(CHROME_DRIVER_PATH)
        base_url = 'https://www.youtube.com/results?search_query='
        search_keyword = 'short video 10 seconds'
        url = base_url + search_keyword.replace(' ', '+')
        main(driver, url)
