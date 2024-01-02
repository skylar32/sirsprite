token = 'YOUR TOKEN GOES HERE'
guilds = {
    # Each server the bot is in should have its own entry in this dictionary
    000000000000000000: {   # this is the server ID
        'name': 'My Server',    # for logging purposes
        'storycrafter': {   # settings for the storycrafter extension
            'channel_id': 00000000000000000, # the ID of the channel the prompts should be posted in
            'role_id': 00000000000000000,   # the ID of the role that should be pinged
            'role_link': 'https://discord.com/channels/abcxyz'  # link to the message with instructions for acquiring
                                                                # the storycrafter ping role (optional)
        },
        'staff': 00000000000000000, # the ID of the mod chat
        'report_post_id': 00000000000000000, # the ID of the persistent report review message, once sent
        'setup_mode': True, # setting this to true enables certain setup commands for the guild. set it to false
                            # or remove it once setup is complete in order to hide the commands and prevent clutter.
    },
    000000000000000001: {
        # and so on...
    },
}
