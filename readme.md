# sirsprite
A simple bot that performs utility functions for the Thousand Roads community.

## Running
1. The bot has only been tested on Python 3.10.2, so I recommend installing it. 
   Earlier versions may work but I haven't tested it so proceed at your own risk.
2. Set up your virtual environment:
   ```bash
   python3.10 -m venv env
   source env/bin/activate
3. Install dependencies.  At present the only dependency is the development version of
   [discord.py](https://github.com/Rapptz/discord.py).  It must be installed from Git.
   ```bash
    pip install git+https://github.com/Rapptz/discord.py.git
4. Set up your configuration.  A handful of thread, channel, and message IDs must be supplied
   in `config.py` for all of the bot's extensions to function properly.  An example configuration
   is provided in [config.example.py](config.example.py), though obviously you will need to fill in
   your own token, guild IDs, etc. as appropriate.
5. Execute `python3.10 main.py` to get the bot running.

## Extension information
### [Storycrafter](cogs/storycrafter.py)
The [Storycrafter](cogs/storycrafter.py) extension enables users to submit prompts for community discussion into
a designated thread.  Users may opt into notifications for new prompts.
A message is also sent to the thread's parent channel for increased visibility.
The prompts are dictated by the user through a Discord text input modal initialized via a slash command.
### [Moderation](cogs/moderation.py)
The [Moderation](cogs/moderation.py) extension provides several avenues through which users may submit reports
to the community staff. The first of these avenues is a persistent view (ideally posted in a highly visible and
relatively static channel) featuring a button that will open the report modal when clicked.
Messages and users can also be reported through  the context menu (visible only on desktop). 
Reports may be submitted anonymously, and are forwarded to the moderation channel where they will be viewable by all mods.
