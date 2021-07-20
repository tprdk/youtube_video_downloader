import sys
from pytube import YouTube, Playlist
'''
pytube v10.9.2 (pip install pytube==10.9.2)
pytube document = https://pytube3.readthedocs.io/en/latest/api.html
python v3.6
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
    if caption is not None:
        with open(caption_file_name, 'w', encoding='utf-8') as caption_file:
            caption_file.write(caption.generate_srt_captions())


def download_video_and_caption(url, caption_file_name, caption_language):
    youtube = YouTube(url, on_progress_callback=show_progress_bar)
    download_caption(youtube.captions, caption_file_name, caption_language)
    youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()


def download_playlist(url, caption_file_name_prefix, caption_language):
    playlist = Playlist(url)
    print(f'Number of videos in playlist : {len(playlist.video_urls)}')
    for index, v_url in enumerate(playlist.video_urls):
        print(f'\nDownloading : {v_url}')
        youtube = YouTube(v_url, on_progress_callback=show_progress_bar)

        caption_file_name = caption_file_name_prefix + f'_{index}.srt'
        download_caption(youtube.captions, caption_file_name, caption_language)

        youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()


video_url = 'https://www.youtube.com/watch?v=tIeHLnjs5U8&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=4&t=3s'
#download_video_and_caption(video_url, 'video.srt', 'en')

playlist_url = 'https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi'
#download_playlist(playlist_url, 'playlist_video', 'en')

auto_generated_caption_url = 'https://www.youtube.com/watch?v=_kSvE7ldoc4'
download_video_and_caption(auto_generated_caption_url, 'agadmator.srt', 'a.en')

