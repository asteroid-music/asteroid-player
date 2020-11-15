from player import play_song
from database import Database
import logging


class Cycler:
    """main async class handling encapsulating song fetching and
    playback"""

    def __init__(self, cfg):
        self.db = Database(cfg["database"])
        self.musicfiles = cfg["musicfiles"]

    async def cycle(self):
        """ get song and play """
        next_song = await self.db.next_song()
        logging.info(f"Next song {next_song}")
        try:
            await play_song(self.musicfiles, next_song)
        except Exception as e:
            logging.error(f"Playback error: {e}")
        return

    async def cycle_forever(self):
        """ main loop """
        await self.db.connect()
        while True:
            await self.cycle()
