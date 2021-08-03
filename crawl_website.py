import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def configure_chrome_driver(path):
    '''
    Web browser'ını aktif edebilmek için gerekli driver'in alınması fonskiyonu.
    İndirilmiş durumda ise path üzerinden verilebilir,
    indirilmiş değil ise ChromeDriverManager().install() ile indrilir.

    :param path: chrome driver path
    :return: chrome driver
    '''
    if path:
        # configure driver with zip file if its downloaded
        return webdriver.Chrome(path)
    else:
        # download chrome driver if not exists
        return webdriver.Chrome(ChromeDriverManager().install())


def scroll_down_page(driver):
    '''
    Sayfanın aşağıya scroll edilmesini sağlayan fonksiyon
    :param driver: selenium chrome driver
    '''
    elem = driver.find_element_by_tag_name("body")
    elem.send_keys(Keys.PAGE_DOWN)


def get_video_urls(driver, url_list, url_queue):
    '''
    youtube sayfasındaki html elemanlarında video-title'a sahip id'lerin
    içerdiği hrefler o videoların urlleridir.
    Buradan elde edilen urller eğer daha önceden listeye eklenmemişse eklenir aksi durumda eklenmez.

    :param driver: selenium chrome driver
    :param url_list: crawl edilmiş olan urllerin listeleri
    :param url_queue: crawl edilmiş olan urllerin indirilmesi için eklendiği kuyruk
    '''
    elements = driver.find_elements_by_id('video-title')
    for element in elements:
        url = element.get_attribute('href')
        if url not in url_list:
            url_list.append(url)
            url_queue.put(url)


def crawl(driver, url, url_queue):
    '''
    Öncelikle Youtube web sitesinin browser üzerinde yüklenmesini sağlar.
    Sonsuz bir döngüde 60 saniyelik beklemelerle
    get_video_urls ile sayfadaki videoların url'lerini alır
    scroll_down_page fonksiyonu ile sayfayı aşağı scroll eder

    :param driver: selenium chrome driver
    :param url: youtube search query + keyword
    :param url_queue: crawl edilmiş olan urller
    '''
    driver.get(url)
    url_list = []
    time.sleep(5)
    while True:
        get_video_urls(driver, url_list, url_queue)
        scroll_down_page(driver)
        print(f'\nUrl count : {len(url_list)}')
        time.sleep(60)


