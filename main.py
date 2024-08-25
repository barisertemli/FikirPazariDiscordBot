import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

# Step 0: Load the Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # Bot is kind of a subclass of Client. We can use commands with it.
discord.Intents.message_content = True # Normally Python doesn't like it? We set it True to let bot see the messages.
bot.remove_command("help") # We remove the default help command to create our own.

# Step 2: Message Functionality

# Step 3: Startup
@bot.event
async def on_ready():
    print(f"{bot.user} is alive!")

    channel_id = 1277280892485894297  # etkinlik kayit id
    channel = bot.get_channel(channel_id)

    await channel.send("Selam!")


class Button(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Send Message", style=discord.ButtonStyle.primary)
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Bana tıkladın!", ephemeral=True)

@bot.command()
async def menu(ctx):
    view = Button()
    await ctx.reply(view=view)



# Step 4: Handling Incoming Messages



# Step 5: Main Entry Point
def main():
    bot.run(token=TOKEN)

if __name__ == "__main__":
    main()