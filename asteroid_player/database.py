import asyncio
import sqlite3
import logging


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)

    async def next_song(self):
        """ gets next song, removes it from queue and adds to history """
        file, duration, _id = await self._fetch_from_queue()

        # remove from queue
        self.conn.execute("DELETE FROM queue WHERE id=?", (_id,))

        # add to history, after changing id -> song_id to avoid conflicts
        # song['song_id'] = song.pop('_id')
        # self.db.history.insert_one(song)

        self.conn.commit()
        return {"file":file, "duration":duration}


    async def _fetch_from_queue(self):
        """ get next item from queue, else waits until one available """
        while True:
            await asyncio.sleep(1)
            item = self._query_database()
            if item is not None:
                return item
            else:
                logging.info("No song in queue.")

    def _query_database(self):
        query = self.conn.execute(
            (
                "SELECT music.file, music.duration, queue.id FROM queue "
                "JOIN music ON queue.song_id = music.id "
                "ORDER BY queue.votes DESC"
            )
        )
        return query.fetchone()
