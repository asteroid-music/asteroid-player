import logging
import asyncio

try:
    import vlc
except:
    # for testing purposes
    logging.warning("vlc could not be imported -- using MagicMock")
    import unittest.mock as mock
    vlc = mock.MagicMock()

async def play_song(song):
    """ use vlc to play song; return once done """
    pl = vlc.MediaPlayer(".." + song['file'])
    pl.play()
    await asyncio.sleep(song['duration'])
    return

