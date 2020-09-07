import yaml
with open("./config.yml", "r") as ymlfile:
    cfg = yaml.load(
        ymlfile, 
        Loader=yaml.SafeLoader
    )

import logging
logcfg = cfg["logging"]
logging.basicConfig(
    format=logcfg["format"], 
    datefmt=logcfg["datefmt"],
    level=logging.__getattribute__(
        logcfg["level"].upper()
    )
)

import asyncio

from player import play_song
from database import Database


class Cycler:
    """ main async class handling encapsulating song fetching and
        playback """

    def __init__(self):
        self.db = Database(cfg['database'])

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


