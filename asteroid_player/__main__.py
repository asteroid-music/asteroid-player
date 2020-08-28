import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s', 
    datefmt='%d/%m/%Y %H:%M:%S',
    level=logging.INFO
)

import asyncio

from player import play_song
from database import Database


class Cycler:
    """ main async class handling encapsulating song fetching and
        playback """

    def __init__(self):
        self.db = Database()

    async def cycle(self):
        """ get song and play """
        next_song = await self.db.next_song()
        logging.info(f"Next song {next_song}")
        await play_song(next_song)
        return

    async def cycle_forever(self):
        """ main loop """
        while True:
            await self.cycle()


if __name__ == '__main__':
    cylcer = Cycler()
    asyncio.run(cylcer.cycle_forever())


