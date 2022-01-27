from pymongo.database import Database
from pymongo.collection import Collection

class BotStickersCacheDatabase:
    stickers_cache: Collection

    def __init__(self, database: Database):
        self.stickers_cache = database.get_collection('stickersCache')
        self.stickers_cache.create_index('tag', unique = True)

    async def find_sticker_url(self, tag: str) -> str:
        cached_sticker = await self.stickers_cache.find_one({ 'tag': tag })

        if cached_sticker == None:
            return None

        else:
            return cached_sticker.get('url', None)

    async def add_sticker(self, tag: str, url: str) -> None:
        await self.stickers_cache.insert_one({ 'tag': tag, 'url': url })
