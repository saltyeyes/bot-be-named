import string

from discord.ext import commands

import constants
from utils import discord_utils
from modules.perfect_pitch import perfect_pitch_utils, perfect_pitch_constants
import discord
import random
import os
import shutil
import glob

class PerfectPitch(commands.Cog, name="Perfect Pitch"):
    """Identify the note being played!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="playtune")
    @commands.has_any_role(
        constants.SONI_SERVER_TESTER_ROLE,
        constants.KEV_SERVER_TESTER_ROLE
    )
    async def playtune(self, ctx, *args):
        """Play a string of notes together"""

        # TODO:
        # how to structure input?
        # ~playtune meter? octave? chain of notes?
        # getnote function?
        # ADVANCED: put it in a key? no, no.
        tune_dir = os.path.join(os.getcwd(), "modules", "perfect_pitch", "music", "tunes", ctx.channel.name)
        if not os.path.exists(tune_dir):
            os.mkdir(tune_dir)

        tune = perfect_pitch_utils.Tune(ctx.channel.name)
        tune.process_args(args)

        output_path = await tune.create_tune()
        try:
            await ctx.send(file=discord.File(output_path, filename="tune.mp3"))
        except FileNotFoundError:
            embed = discord_utils.create_embed()
            embed.add_field(name=f"{constants.FAILED}",
                            value=f"Sorry, we had a problem creating your tune! Check out `{ctx.prefix}help` "
                                  f"to see how to use the command, or try: "
                                  f"`{ctx.prefix}playtune meter=1 octave=5 C D E F` as an example")
            await ctx.send(embed=embed)

    @commands.command(name="chord")
    @commands.has_any_role(
        constants.SONI_SERVER_TESTER_ROLE,
        constants.KEV_SERVER_TESTER_ROLE
    )
    async def chord(self, ctx):
        """Sends the user a random chord. Note: all chords come from the 4th octave (middle C)"""
        chord = random.choice(glob.glob(os.path.join(os.getcwd(), "modules", "perfect_pitch", "music", "piano", "chords", "*.mp3")))
        await ctx.send(file=discord.File(chord, filename="random_chord.mp3"))
        await ctx.send(f"Answer: ||{chord.split('/')[-1].replace('.mp3', '').replace('_', ' ').center(15)}||")

    # TODO: CLEAN PLS for the love of christ
    @commands.command(name="note")
    @commands.has_any_role(
        constants.SONI_SERVER_TESTER_ROLE,
        constants.KEV_SERVER_TESTER_ROLE
    )
    async def note(self, ctx, *args):
        """Send the user a random note for them to identify.
        Arguments:
            - Octave (int): The specific octave you want a random note from
            - Flat_or_Nat (str): Whether you want the note to be flat/sharp or natural
            - Note (str): A specific note (e.g. G4)
        """
        print("Received note")
        # User-selected parameters for which notes will appear
        octave = None
        flat_or_nat = ''
        note = ''
        for arg in args:
            # If the user supplied an exact note, send it
            if os.path.exists(os.path.join(os.getcwd(), "modules", "perfect_pitch", "music", "piano", "notes", arg + ".mp3")):
                await ctx.send(file=discord.File(os.path.join(os.getcwd(), "modules", "perfect_pitch", "music", "piano", "notes", arg+".mp3")))
                return
            # Don't redefine octave multiple times; only take first int argument passed
            if not isinstance(octave, int):
                try:
                    octave = int(arg)
                except ValueError:
                    pass
            # Similarly, only first flat or nat passed
            if (arg == 'flat' or arg == 'nat') and not flat_or_nat:
                flat_or_nat = arg

        if octave is not None and (octave < 0 or octave > 7):
            embed = discord_utils.create_embed()
            embed.add_field(name="Failed!",
                            value="Make sure your octave value is between 0 and 7!")
            await ctx.send(embed=embed)
            return
        # The user can specify which octave they want to hear, in which case we only get a note from that octave
        filenames = f"{note if note else '*'}{'b' if flat_or_nat == 'flat' else '*'}{octave if isinstance(octave, int) else '*'}.mp3"

        mp3_paths = glob.glob(os.path.join(os.getcwd(), "modules", "perfect_pitch", "music", "piano", "notes", filenames))

        # Make sure flat symbol is not in filename
        if flat_or_nat == 'nat':
            mp3_paths = list(filter(lambda x: 'b' not in x.split('/')[-1], mp3_paths))

        notepath = random.choice(mp3_paths)

        note = discord.File(notepath, filename="random_note.mp3")
        await ctx.send(file=note)
        await ctx.send(f"Answer: ||{notepath.split('/')[-1].split('.')[0].center(10)}||")


def setup(bot):
    bot.add_cog(PerfectPitch(bot))