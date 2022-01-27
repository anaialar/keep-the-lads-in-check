from typing import List, Tuple

import discord
from bot.database import BotDatabase

class BotPermissionUtils:
    permissions = {
       'ADMINISTRATOR': 0,
       'MODERATOR': 1,
       'DJ': 50,
       'GENERAL': 99,
       'MUTED': 100
    }

    database: BotDatabase

    def __init__(self, database: BotDatabase):
        self.database = database
        self.get_role_permission = database.permissions.get_role_permission
        self.set_role_permission = database.permissions.set_role_permission
        self.remove_role_permission = database.permissions.remove_role_permission

    async def get_all_role_permissions(self, guild: discord.Guild) -> List[Tuple[str, str]]:
        result = []

        async for permission in self.database.permissions.get_all_role_permissions():
            role_name = discord.utils.get(guild.roles, id = permission.get('roleId')).name
            permission_name = self.get_permission_name(permission.get('permission')).lower()
            result.append((role_name, permission_name))

        return result

    def is_administrator(self, permission: int) -> bool:
        return permission <= self.permissions.get('ADMINISTRATOR')

    def is_moderator(self, permission: int) -> bool:
        return permission <= self.permissions.get('MODERATOR')

    def is_dj(self, permission: int) -> bool:
        return permission == self.permissions.get('DJ') or self.is_moderator(permission)

    def is_general(self, permission: int) -> bool:
        return permission <= self.permissions.get('GENERAL')

    def is_muted(self, permission: int) -> bool:
        return permission >= self.permissions.get('MUTED')

    def get_permission_name(self, permission: int) -> str:
        for (name, item_permission) in self.permissions.items():
            if item_permission == permission:
                return name

        return None
