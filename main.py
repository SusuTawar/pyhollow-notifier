import sys
import youtube_dl
import socketio
import asyncio

loop = asyncio.get_event_loop()


async def main():
    yt_opts = {'quiet': True}
    with youtube_dl.YoutubeDL(yt_opts) as ytdl:
        sio = socketio.AsyncClient(
            reconnection=True, logger=True)

        @sio.event
        def connect():
            print('connection established')

        @sio.on('vid-update', namespace='/hololive')
        def vid_update(data):
            print(data)
            print(f"notification from {data['channel']}")
            try:
                info = ytdl.extract_info(
                    f"https://www.youtube.com/watch?v={data['link']}",
                    False
                )
                if(info['is_live']):
                    print(f"{data['channel']} is live !")
            except Exception as e:
                print(type(e).__name__)

        await sio.connect('http://localhost:4000', namespaces=['/hololive'])
        await sio.wait()


if __name__ == "__main__":
    loop.run_until_complete(main())
