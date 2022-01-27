class BotMessages:
    help = {
        'GENERAL_HELP_MESSAGE': lambda prefix: (f'\n\r***{prefix}help**:* DM help mesasge'
            f'\n\r***{prefix}meme_random** or **{prefix}mr**:* fetch a random meme'
            f'\n\r***{prefix}joke_random** or **{prefix}jr**:* have the bot say a random joke (can\'t promise to be good though)'
            f'\n\r***{prefix}choose_random_member** or **{prefix}crm**:* chooses a random member excluding bots'
            f'\n\r***{prefix}choose_random_online_member** or **{prefix}crom**:* chooses a random online member excluding bots'
            f'\n\r***{prefix}sticker** (tag):* gives a sticker associated with the given tag'
            f'\n\r***{prefix}weather** (city):* gives the weather of the given location'),

        'AUDIO_HELP_MESSAGE': lambda prefix: (f'\n\r***{prefix}audio_play** or **{prefix}ap** [voice channel] (url):* plays the audio given youtube url or search query in the given voice channel (the [] is required)'
            f'\n\r***{prefix}audio_stop** or **{prefix}as**:* stops the audio currently being played'),

        'MODERATOR_HELP_MESSAGE': lambda prefix: (f'\n\r***{prefix}delete** or **{prefix}d** (number max 15):* deletes the messages in the order of most recent'
            f'\n\r***{prefix}add_channel_censoring** or **{prefix}acc** #channel:* add a channel to censor'
            f'\n\r***{prefix}remove_channel_censoring** or **{prefix}rcc** #channel:* remove a channel from censor list'
            f'\n\r***{prefix}currently_censored_channels** or **{prefix}gcc**:* get a list of currently censored channels'),

        'ADMINISTRATOR_HELP_MESSAGE': lambda prefix: (f'\n\r***{prefix}say** (text):* make the bot text something'
            f'\n\r***{prefix}delete** or **{prefix}d** (> 15):* delete the messages in the order of most recent, with no limit to how many'
            f'\n\r***{prefix}change_default_role** or **{prefix}cdr** @role:* set the given role as the default role given to all members'
            f'\n\r***{prefix}set_role_permission** or **{prefix}srp** @role (permission name):* set the permission for a role'
            f'\n\r***{prefix}remove_role_permission** or **{prefix}rrp** @role:* remove the permissions of a role'
            f'\n\r***{prefix}get_all_role_permissions** or **{prefix}garp**:* DM a list of all roles and their respective permissions')
    }

    command_exceptions = {
        'UNHANDLED': 'Failed to run command.',
        'GUILD_ONLY': 'This command is meant for a guild.',
        'UNKNOWN_COMMAND': 'This command doesn\'t exist.',
        'UNAUTHORIZED': 'You are not authorized to access this command.',
        'UNKNOWN_SYNTAX': 'Command syntax is incorrect.',
        'ROLE_NOT_FOUND': 'Role not found.',
        'CHANNEL_NOT_FOUND': 'Role not found.',
        'PERMISSION_NOT_FOUND': 'Permission not found.',
        'VOICE_CHANNEL_NOT_FOUND': 'Voice channel named not found.',
        'FUN': {
            'JOKE_NOT_FOUND': 'Ran out of jokes.',
            'STICKER_NOT_FOUND': 'Sticker not found.',
            'STICKER_RATE_LIMITED': 'Too many stickers posted at a time.',
            'CITY_NOT_FOUND': 'City not found.'
        },
        'ADMINISTRATOR': {
            'ROLE_PERMISSION_NOT_FOUND': lambda role_id: f'Role <@&{role_id}> has no permission associated with it.'
        },
        'AUDIO': {
            'CHANNEL_NAME_REQUIRED': 'The channel name is required.',
            'QUERY_OR_URL': 'YouTube search query or url is required.',
            'VIDEO_NOT_FOUND': 'No video was found for the given query.',
            'ALREADY_PLAYING': 'Unable to play, an audio is already being played. Stop it first.',
            'ALREADY_STOPPED': 'No audio is being played.'
        },
        'MODERATOR': {
            'DELETE_MAXIMUM_15': 'Can only delete upto 15 messages.',
            'ALREADY_CENSORED': 'The channel is already being censored.',
            'ALREADY_NOT_CENSORED': 'The channel is already not being censored.'
        }
    }

    command_responses = {
        'FUN': {
            'CHOOSE_MEMBER': lambda name: f'{name}! I choose you.',
            'WEATHER_RESPONSE': lambda info: '**City:** {city}\n**Weather:** {description}\n**Temperature:** {temperature}°C\n**Feels like**: {feels_like}°C\n**Latitude:** {latitude}\n**Longitude:** {longitude}'.format(**info)
        }
    }
