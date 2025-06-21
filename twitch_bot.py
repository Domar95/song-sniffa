import os
from dotenv import load_dotenv
from twitchio.ext import commands

load_dotenv()

bot = commands.Bot(
    token=os.getenv("TWITCH_ACCES_TOKEN"),
    prefix="!",
    initial_channels=[os.getenv("TWITCH_CHANNEL")],
)


@bot.command(name="sniffa")
async def song_command(ctx):
    from sniff import sniff

    result = sniff(
        f"https://www.twitch.tv/{os.getenv("TWITCH_CHANNEL")}",
        mode="buffer",
        duration=10,
    )

    if not result:
        result = "Kappa no song sniffed"
    else:
        result = f"sniffed song: {result}"

    user = ctx.author.name
    await ctx.send(f"@{user}, {result}")


if __name__ == "__main__":
    bot.run()
