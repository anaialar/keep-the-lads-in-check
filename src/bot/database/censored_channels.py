from typing import Dict, List

from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

class BotCensoredChannelsDatabase:
    censored_channels: Collection
    censored_channels_cache: Dict[int, bool]

    def __init__(self, database: Database):
        self.censored_channels = database.get_collection('censoredChannels')
        self.censored_channels.create_index('channelId', unique = True)
        self.censored_channels_cache = {}

    async def is_censored(self, channel_id: int) -> bool:
        catched_censored_channel = self.censored_channels_cache.get(channel_id, None)

        if catched_censored_channel == None:
            is_censored = False

            if (await self.censored_channels.find_one({ 'channelId': channel_id })) != None:
                is_censored = True

            self.censored_channels_cache[channel_id] = is_censored
            return is_censored

        else:
            return catched_censored_channel

    def get_censored_channels(self) -> List[Dict]:
        return self.censored_channels.find()

    # Returns False if that channel is already being censored
    async def add_censored_channel(self, channel_id: int) -> bool:
        try:
            await self.censored_channels.insert_one({ 'channelId': channel_id })
            self.censored_channels_cache[channel_id] = True
            return True

        except DuplicateKeyError:
            return False

        except Exception as error:
            raise error

    # Retuns False if the channel wasn't already censored otherwise True
    async def remove_censored_channel(self, channel_id: int) -> bool:
        existed = (await self.censored_channels.delete_one({ 'channelId': channel_id })).deleted_count >= 1
        self.censored_channels_cache[channel_id] = False
        return existed
