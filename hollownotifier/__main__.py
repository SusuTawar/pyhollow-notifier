import socketio
import asyncio
import youtube_dl
from config import read_ch
from subprocess import Popen

loop = asyncio.get_event_loop()
hn_host = 'http://localhost'
sio_port = 4000


async def main():
    channels = read_ch()
    sio = socketio.AsyncClient(
        reconnection=True, logger=True)
    namespaces = [f'/{ch}' for ch in channels.keys()]

    yt_opts = {
        'quiet': False,
    }

    @ sio.event
    def connect():
        print('connection established')

    for group in namespaces:
        @ sio.on('vid-update', namespace=group)
        def vid_update(data):
            if data['group'] not in channels:
                return print(f"{data['group']} not in {channels}")
            if data['channel'] not in channels[data['group']]:
                return print(f"{data['channel']} not in {channels[data['group']]}")
            with youtube_dl.YoutubeDL(yt_opts) as ytdl:
                try:
                    print(f"fetch {data['title']} metadata ")
                    url = f"https://www.youtube.com/watch?v={data['link']}"
                    info = ytdl.extract_info(url, False)
                    ytdl_cmd = [
                        'youtube-dl',
                        '--quiet',
                        '--config-location', 'config/ytdl.conf',
                        '--output', f"youtube/{data['group']}/{data['channel']}/%(title)s.%(ext)s",
                        url
                    ]
                    if(info['is_live'] or True):
                        print(
                            f"{data['channel']} from {data['group']} is live!"
                        )
                        print(data['title'])
                        choice = input("Download (y/n) ? ")
                        if choice[:1].lower() == 'y':
                            print(f"downloading {data['title']}...")
                            ytdl = Popen(ytdl_cmd)
                except Exception as e:
                    print(e)

    await sio.connect(f'{hn_host}:{sio_port}/', namespaces=namespaces)
    await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(main())
