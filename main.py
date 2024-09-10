from customClasses import *
from dotenv import load_dotenv
from discord.ext import commands, tasks

# Step 0: Load the Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", owner_id=os.getenv("OWNER_ID"), intents=discord.Intents.all()) # Bot is kind of a subclass of Client. We can use commands with it.
discord.Intents.message_content = True # Normally Python doesn't like it? We set it True to let bot see the messages.
bot.remove_command("help") # We remove the default help command to create our own.


# Step 3: Startup
# Global dictionary to store views associated with message IDs
views = {
    "activity_join_button_id": os.getenv("ACTIVITY_JOIN_BUTTON_ID")
}


@bot.event
async def on_ready(): # This function is called when the bot is ready to be used.
    print(f"{bot.user} is alive!")

    channel_id = int(os.getenv("ACTIVITY_JOIN_TEXTCHANNEL_ID"))  # text channel id
    channel = bot.get_channel(channel_id)

    # await channel.send("Rastgele Oda Açma Kontrol Paneli", view=ControlPanel())

    # await channel.send("Bir sonraki etkinliğe kaydolmak için aşağıdaki butona tıklayın!", view=SingleButton())


# Handle interactions globally
@bot.event
async def on_interaction(interaction: discord.Interaction): # This function is called when an interaction is made with the bot.

    if interaction.type == discord.InteractionType.component: # If the interaction is a component interaction


        message_id = str(interaction.data["custom_id"])

        if message_id == views["activity_join_button_id"]:
            # await view.children[0].callback(interaction)  # Call the callback for the button
            # await interaction.response.send_message("Etkinliğe kaydoldun!", ephemeral=True)

            modal = ActivityModal(title="Modal via Button")
            await interaction.response.send_modal(modal)
            # print(views)

        else:
            # await interaction.response.send_message("This button is no longer active.", ephemeral=True)
            print(views)

#TODO: @commands.is_owner() use this to restrict the command to the owner of the bot.


# Step 5: Main Entry Point
def main():
    bot.run(token=TOKEN)

if __name__ == "__main__":
    main()