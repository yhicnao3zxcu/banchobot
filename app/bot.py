from discord.ext.commands import *
from app.extensions import *

import discord
import app

class BanchoBot(Bot):
    async def on_ready(self):
        app.session.logger.info(f'Logged in as {self.user}.')
        app.session.filters.populate()
        await self.load_cogs()

    async def close(self):
        app.session.redis.close()
        app.session.database.engine.dispose()
        await app.session.redis_async.close()
        await super().close()

    async def load_cogs(self):
        extensions = [
            "app.extensions.errors",
            "app.extensions.bridge",
            "app.extensions.link",
            "app.extensions.fun",
            "app.extensions.recent",
            "app.extensions.profile",
            "app.extensions.top",
            "app.extensions.simulate",
            "app.extensions.search",
            "app.extensions.rankings",
            "app.extensions.pprecord",
            "app.extensions.moderation",
            "app.extensions.beatmaps",
        ]
        
        for extension in extensions:
            try:
                await self.load_extension(extension)
                app.session.logger.info(f'Loaded extension: {extension}')
            except Exception as e:
                app.session.logger.error(f'Failed to load extension {extension}: {e}')
        
        try:
            await self.tree.sync()
            app.session.logger.info('Command tree synced successfully')
        except Exception as e:
            app.session.logger.error(f'Failed to sync command tree: {e}')

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    app.session.bot = BanchoBot(app.session.config.DISCORD_BOT_PREFIX, intents=intents, help_command=None)
    app.session.bot.run(app.session.config.DISCORD_BOT_TOKEN, log_handler=None)
