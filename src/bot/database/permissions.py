from typing import Union, Dict, List

from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

class BotPermissionsDatabase:
    permissions: Collection
    permissions_cache: Dict[int, int]

    def __init__(self, database: Database):
        self.permissions = database.get_collection('permissions')
        self.permissions.create_index('roleId', unique = True)
        self.permissions_cache = {}

    # Returns permission or returns False if entry wasn't found
    async def get_role_permission(self, role_id: int) -> Union[int, bool]:
        catched_permission = self.permissions_cache.get('roleId')

        if catched_permission == None:
            entry = await self.permissions.find_one({ 'roleId': role_id })
            if entry == None:
                return False

            else:
                permission = entry.get('permission', False)
                self.permissions_cache[role_id] = permission
                return permission
        else:

            return catched_permission

    def get_all_role_permissions(self) -> List[Dict]:
        return self.permissions.find()

    def set_role_permission(self, role_id: int, permission: int) -> None:
        return self.permissions.replace_one({
                'roleId': role_id
            }, {
                'roleId': role_id,
                'permission': permission
            }, upsert = True)

    # Returns True if entry was found and False if it wasn't
    async def remove_role_permission(self, role_id: int) -> bool:
        existed = (await self.permissions.delete_one({ 'roleId': role_id })).deleted_count >= 1

        if existed:
            self.permissions_cache[role_id] = None
            return True

        else:
            return False
