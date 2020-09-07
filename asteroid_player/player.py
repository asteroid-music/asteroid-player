import logging
import asyncio
import os.path

try:
    import vlc
except:
    # for testing purposes
    logging.warning("vlc could not be imported -- using MagicMock")
    import unittest.mock as mock
    vlc = mock.MagicMock()

async def play_song(root, song):
    """ use vlc to play song; return once done """
    pl = vlc.MediaPlayer(
        os.path.join(root, song['file'])
    )
    pl.play()
    logging.warning(pl.get_state())
    await asyncio.sleep(song['duration'])
    return

