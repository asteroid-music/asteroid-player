import asyncio
import logging
import motor.motor_asyncio


class Database:
    def __init__(self, db):
        self._db = db

    async def connect(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(self._db)
        self.collection = client.dev.get_collection("queue")

    async def next_song(self):
        """ gets next song, removes it from queue and adds to history """
        queue_item = await self._fetch_from_queue()
        song = queue_item["song"]
        logging.info(f"Fetched item {song}")

        # remove it from queue
        result = await self.collection.update_one(
            {"name": "queue"}, {"$pull": {"songs": {"song._id": song["_id"]}}}
        )
        if result.modified_count > 0:
            logging.info("Removed song from queue.")
        else:
            logging.warning("Failed to remove song from queue.")

        return {"file": song["file"], "duration": song["duration"]}

    async def _fetch_from_queue(self):
        """ get next item from queue, else waits until one available """
        while True:
            await asyncio.sleep(1)
            item = await self._query_database()
            if item is not None:
                return item
            else:
                logging.info("No song in queue.")

    async def _query_database(self):
        queue = await self.collection.find_one({"name": "queue"})
        if queue != None and len(queue["songs"]) > 0:
            return sorted(queue["songs"], key=lambda i: i["votes"], reverse=True)[0]
        else:
            return None
