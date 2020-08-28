import asyncio
from rethinkdb import r
from rethinkdb.errors import ReqlNonExistenceError


class Database:

    def __init__(self):
        self.conn = r.connect()

    async def next_song(self):
        """ gets next song, removes it from queue and adds to history """
        song = await self._fetch_from_queue()

        # remove from queue
        r.table('queue').get(song['id']).delete().run(self.conn)

        # add to history, after changing id -> song_id to avoid conflicts
        song['song_id'] = song.pop('id')
        r.table('history').insert(song).run(self.conn)

        return song


    async def _fetch_from_queue(self):
        """ get next item from queue, else waits until one available """
        try: 
            top = r.table('queue').max('votes').run(self.conn)
        except ReqlNonExistenceError:
            # queue empty
            change = r.table('queue').changes().run(self.conn)
            top = next(change)['new_val'] 

        # not wrapped in finally incase unknown error
        return top
