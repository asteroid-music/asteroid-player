import logging
import asyncio
import os.path

from playsound import playsound


async def play_song(root, song):
    """ use vlc to play song; return once done """
    logging.info("Playing {}".format(song["file"]))
    playsound(os.path.join(root, song["file"]))
    logging.info("Playback finished.")
    await asyncio.sleep(song["duration"])
