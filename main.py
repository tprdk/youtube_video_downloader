import sys
from pytube import YouTube
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


def download_video_and_caption(url, srt_path):
    youtube = YouTube(url, on_progress_callback=show_progress_bar)

    caption = youtube.captions['en']
    with open(srt_path, 'w', encoding='utf-8') as caption_file:
        caption_file.write(caption.generate_srt_captions())

    youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()



video_url = 'https://www.youtube.com/watch?v=tIeHLnjs5U8&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=4&t=3s'
download_video_and_caption(video_url, 'video.srt')
