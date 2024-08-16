from youtubesearchpython import VideosSearch, PlaylistsSearch
from urllib.parse import urlparse, parse_qs
from pytube import YouTube
import yt_dlp
import config
import os

async def searchYt(query):
    try:
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()
        if not result["result"]:
            return None, None, None
        title = result["result"][0]["title"]
        duration = result["result"][0]["duration"]
        link = result["result"][0]["link"]
        return title, duration, link
    except Exception as e:
        print(f"Error in searchYt: {e}")
        return None, None, None

async def download_audio(link, file_name):
    output_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Highest MP3 bitrate
        }, {
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        }],
        'outtmpl': os.path.join(output_path, f'{file_name}.%(ext)s'),
        'cookiefile': config.COOK_PATH,
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Ganti dengan path ke ffmpeg Anda
        'postprocessor_args': [
            '-acodec', 'libmp3lame',
            '-b:a', '320k',
            '-ar', '48000',  # Sample rate
            '-ac', '2',      # Stereo
            '-q:a', '0',     # Highest quality setting for LAME
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
        'verbose': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            duration = info.get('duration')
            title = info.get('title')
            ydl.download([link])
        
        output_file = os.path.join(output_path, f'{file_name}.mp3')
        return output_file, title, duration
    except Exception as e:
        print(f"Error in download_audio: {e}")
        return None, None, None

def searchPlaylist(query):
    query = str(query)
    playlistResult = PlaylistsSearch(query, limit=1)
    Result = playlistResult.result()
    if not Result["result"] == []:
        title = Result["result"][0]["title"]
        videoCount = Result["result"][0]["videoCount"]
        link = Result["result"][0]["link"]
        return title, videoCount, link
    return None, None, None


def extract_playlist_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get('list', [None])[0]
    return playlist_id


def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        video_id = parsed_url.path[1:]
    else:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
    return video_id
