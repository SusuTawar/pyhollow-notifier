from distutils.core import setup

setup(
    name='Hollow Notifier (py)',
    version='0.0.1',
    license='LICENSE',
    description='vtuber on stream auto downloader',
    install_requires=['requests','python-socketio[asyncio_client]','youtube-dl'],
    python_requires='>=3.6'
)
