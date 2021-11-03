import discord
import os
from discord.ext import commands
from emoji import UNICODE_EMOJI
from typing import Union

import constants
from utils import discord_utils, logging_utils


class MiscCog(commands.Cog, name="Misc"):
    """A collection of Misc useful/fun commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="emoji")
    async def emoji(self, ctx, emojiname: Union[discord.Emoji, str], to_delete: str = ""):
        """Finds the custom emoji mentioned and uses it. 
        This command works for normal as well as animated emojis, as long as the bot is in one server with that emoji.

        If you say delete after the emoji name, it deletes original message

        Usage : `~emoji snoo_glow delete`
        Usage : `~emoji :snoo_grin:`
        """
        logging_utils.log_command("emoji", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        emoji = None

        try:
            if(to_delete.lower()[0:3]=="del"):
                await ctx.message.delete()
        except discord.Forbidden:
            embed.add_field(name=f"{constants.FAILED}!",
                            value=f"Unable to delete original message. Do I have `manage_messages` permissions?")
            await ctx.send(embed=embed)
            return

        # custom emoji
        if isinstance(emojiname, discord.Emoji):
            await ctx.send(emojiname.url)
            return
        # default emoji
        elif isinstance(emojiname, str) and emojiname in UNICODE_EMOJI:
            await ctx.send(emojiname)
            return
        if emojiname[0]==":" and emojiname[-1]==":":
            emojiname = emojiname[1:-1]

        for guild in self.bot.guilds:
            emoji = discord.utils.get(guild.emojis, name=emojiname)
            if emoji is not None:
                break

        if emoji is None:
            embed.add_field(name=f"{constants.FAILED}!",
                            value=f"Emoji named {emojiname} not found",
                            inline=False)
            await ctx.send(embed=embed)
            return

        await ctx.send(emoji.url)


    @commands.command(name="about", aliases=["aboutthebot","github"])
    async def about(self, ctx):
        """A quick primer about BBN and what it does

        Usage : `~about`
        """
        logging_utils.log_command("about", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        emoji = None
        owner = await self.bot.fetch_user(os.getenv("BOT_OWNER_DISCORD_ID"))

        embed.add_field(name=f"About Me!",
                        value=f"Hello!\n"
                        f"Bot Be Named is a discord bot that we use while solving Puzzle Hunts.\n"
                        f"The bot has a few channel management functions, some puzzle-hunt utility functions, "
                        f"as well as Google-Sheets interactivity.\n"
                        f"You can make channels as well as tabs on your Sheet, and other similar QoL upgrades to your puzzlehunting setup.\n\n"
                        f"[Bot Github link](https://github.com/kevslinger/bot-be-named/)\n\n"
                        f"To learn more about the bot or useful functions, use `{constants.DEFAULT_BOT_PREFIX}startup`\n"
                        f"Any problems? Let {owner.mention} know.",
                        inline=False)
        await ctx.send(embed=embed)


    @commands.command(name="startup")
    async def startup(self, ctx):
        """A quick primer about helpful BBN functions

        Usage : `~startup`
        """
        logging_utils.log_command("startup", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        emoji = None
        owner = await self.bot.fetch_user(os.getenv("BOT_OWNER_DISCORD_ID"))

        embed.add_field(name=f"Helpful commands!",
                        value=f"Some of the useful bot commands are -\n"
                        f"- `{constants.DEFAULT_BOT_PREFIX}help` for a list of commands\n"
                        f"- `{constants.DEFAULT_BOT_PREFIX}help commandname` for a description of a command (and its limitations). **When in doubt, use this command**.\n"
                        f"- `{constants.DEFAULT_BOT_PREFIX}addverifieds` for setting up roles in Verifieds and Trusted categories on your server\n"
                        f"- `{constants.DEFAULT_BOT_PREFIX}chancrab` and `{constants.DEFAULT_BOT_PREFIX}sheetcrab` for making Google Sheet tabs for your current hunt\n"
                        f"- `{constants.DEFAULT_BOT_PREFIX}solved` etc for marking puzzle channels as solved etc\n"
                        f"- `{constants.DEFAULT_BOT_PREFIX}addcustomcommand` etc for making a customised command with reply.\n",
                        inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MiscCog(bot))