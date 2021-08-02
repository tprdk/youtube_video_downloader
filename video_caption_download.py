import sys
from pytube import YouTube, Playlist

'''
python v3.6
pytube v10.9.3 (pip install pytube==10.9.3)
pytube documentation = https://pytube3.readthedocs.io/en/latest/api.html
Şuan bu api'da sorun var.
'''


def show_progress_bar(stream, chunk, bytes_remaining):
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    sys.stdout.write("\r[{}{}] ".format('=' * done, ' ' * (50 - done)))
    sys.stdout.write(f' {curr}/{stream.filesize}')
    sys.stdout.flush()


def download_caption(video_caption, caption_file_name, caption_language):
    # en for real caption
    # a.en for auto generated caption
    if caption_language in video_caption.keys():
        caption = video_caption[caption_language]
    else:
        # no caption found
        caption = None
    print(f'caption : {caption}')
    if caption is not None:
        with open(caption_file_name, 'w', encoding='utf-8') as caption_file:
            caption_file.write(caption.generate_srt_captions())


def download_video_and_caption(url, caption_file_name, caption_language):
    try:
        youtube = YouTube(url, on_progress_callback=show_progress_bar)
        download_caption(youtube.captions, caption_file_name, caption_language)
        youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()
    except Exception as e:
        print(f'YouTube : {e}')


def download_playlist(url, caption_file_name_prefix, caption_language):
    try:
        playlist = Playlist(url)
        print(f'Number of videos in playlist : {len(playlist.video_urls)}')
        for index, v_url in enumerate(playlist.video_urls):
            print(f'\nDownloading : {v_url}')
            youtube = YouTube(v_url, on_progress_callback=show_progress_bar)

            caption_file_name = caption_file_name_prefix + f'_{index}.srt'
            download_caption(youtube.captions, caption_file_name, caption_language)

            youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()
    except Exception as e:
        print(f'download_playlist : {e}')