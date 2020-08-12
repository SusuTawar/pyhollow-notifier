from setuptools import find_packages, setup

setup(
    name='hollow-notifier',
    version='0.0.1',
    license='LICENSE',
    description='vtuber on stream auto downloader',
    packages=['hollownotifier'],
    install_requires=['requests',
                      'python-socketio[asyncio_client]', 'youtube-dl'],
    python_requires='>=3.6',
    entry_points={
        'hollownotifier': ['app=app.__main__:main'],
    },
)
