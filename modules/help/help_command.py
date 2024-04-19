from nextcord.ext import commands
from utils import discord_utils


class HelpCommand(commands.MinimalHelpCommand):
    """Custom help command override using embeds"""

    def get_ending_note(self):
        """Returns note to display at the bottom"""
        prefix = self.context.clean_prefix
        invoked_with = self.invoked_with
        return f"Use {prefix}{invoked_with} [command] for more info on a command."

    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        return f"{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        prefix = self.context.clean_prefix
        embed = discord_utils.create_embed()
        embed.title = "Bot Commands"
        embed.set_author(
            name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar
        )
        description = self.context.bot.description
        if description:
            embed.description = description

        # no_category_commands = await self.filter_commands(mapping[None], sort=True)
        del mapping[None]
        for cog, commands in sorted(mapping.items(), key=lambda x: x[0].qualified_name):
            name = "No Category" if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                value = f"{chr(10)}".join(f"{prefix}{c.name}" for c in filtered)
                if cog and cog.description:
                    value = f"{cog.description}\n{value}"
                embed.add_field(name=name, value=value)
        # For commands with no category (does not exist anymore)
        # embed.add_field(name="No category", value=f"{chr(10)}".join(f"{prefix}{c.name}" for c in no_category_commands))

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        embed = discord_utils.create_embed()
        embed.title = f"{cog.qualified_name} Commands"
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=self.get_command_signature(command),
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        """implements group help page and command help page"""
        embed = discord_utils.create_embed()
        embed.title = group.qualified_name
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False,
                )

        await self.get_destination().send(embed=embed)

    # Use the same function as group help for command help
    send_command_help = send_group_help
