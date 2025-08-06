#!.venv/bin/python3.12
import discord
from discord.ext import commands
from config import BOT_TOKEN
import gitcord
import json
import study_status


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.display_name}!")


@bot.command()
async def hi(ctx):
    await ctx.send(f"Hi, {ctx.author.display_name}!")


@bot.command()
async def goodbye(ctx):
    await ctx.send(f"Goodbye, {ctx.author.display_name}!")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def add(ctx, *args):
    try: 
        nums = [float(x) for x in args]
        ans = sum(nums)
        await ctx.send(ans)
    except:
        await ctx.send("addition allowed for numbers only")


@bot.command()
async def gitfetch(ctx, git_username, git_repo_name):
    git_info = gitcord.fetch_gitinfo(git_username, git_repo_name)
    if git_info:
        name = git_info["commit"]["author"]["name"]
        commit_id = git_info["sha"][:7]
        commit_message = git_info["commit"]["message"]
        last_commit_date = git_info["commit"]["author"]["date"][:10]
        response = (
            f"Author: {name}\n"
            f"Repository: {git_repo_name}\n"
            f"Last commit ID: {commit_id}\n"
            f"Last commit message: {commit_message}\n"
            f"Last commit date: {last_commit_date}\n"
            f"Link: https://github.com/{git_username}/{git_repo_name}/"
        )
    else:
        response = "Could not fetch GitHub info."
    
    await ctx.send(response)


@bot.command()
async def studying(ctx, topic):
    name = ctx.author.display_name
    study_status.update_status(name, topic)
    await ctx.send(f"Happy studying {topic}, {name}!")


@bot.command()
async def status(ctx):
    response = study_status.get_all_status()
    await ctx.send(response)


if __name__ == "__main__":
    try:
        study_status.create_status_table()
        bot.run(BOT_TOKEN)
    except KeyboardInterrupt:
        study_status.close_status_db()


