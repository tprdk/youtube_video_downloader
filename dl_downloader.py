from __future__ import unicode_literals
import os
import youtube_dl

'''
python v3.6
youtube_dl 2021.6.6 (pip install --upgrade youtube-dl)
youtube_dl documentation = https://github.com/ytdl-org/youtube-dl
'''

def download_with_dl(url, download_path, subtitle_language):
    '''
    youtube_dl api ile video ve altyazı indirme fonksiyonu
    :param url: video url
    :param download_path: folder path
    :param subtitle_language: altyazı dili

    ydl_opt: indirme için verilecek konfigürasyon dict
    :param outtmpl: videonun indirilme adı
    :param format: video formatı
    :param writesubtitles : subtitles indirilmesinin aktif edilmesi
    :param writeautomaticsub: youtube tarafından oluşturulmuş subtitles indirilmesinin aktif edilmesi
    '''
    try:
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s-%(id)s.%(ext)s'),
            'format': '([ext=mp4])',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitle': f'--write-sub --sub-lang {subtitle_language}',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f'youtube_dl exception : {e}')