import asyncio
import pymongo
import logging


class Database:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.test

    async def next_song(self):
        """ gets next song, removes it from queue and adds to history """
        song = await self._fetch_from_queue()

        # remove from queue
        self.db.queue.remove(song.get('_id'))

        # add to history, after changing id -> song_id to avoid conflicts
        song['song_id'] = song.pop('_id')
        self.db.history.insert_one(song)

        return song


    async def _fetch_from_queue(self):
        """ get next item from queue, else waits until one available """
        while True:
            await asyncio.sleep(1)
            try:
                item = self.db.queue.find({}).sort('votes', -1).limit(1).next()
            except StopIteration as e:
                logging.info("No song in queue.")
            except Exception as e:
                logging.error(e)
            else:
                # logging.info(f"Fetched song from queue {item}")
                return item
