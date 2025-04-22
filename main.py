from customClasses import *
from dotenv import load_dotenv
from discord.ext import commands, tasks
import random

api = Api(os.environ.get("AIRTABLE_TOKEN"))
table = api.table(os.environ.get("AIRTABLE_BASE_ID"), "Week1")

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

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is None:
        print(f"{member} left {before.channel}")
    elif after.channel.id == int(os.getenv("HELP_ID")): #TODO: Yardım kanalı buraya gelecek
        print(f"{member} joined {after.channel}")

# Handle interactions globally
@bot.event
async def on_interaction(interaction: discord.Interaction): # This function is called when an interaction is made with the bot.

    if interaction.type == discord.InteractionType.component: # If the interaction is a component interaction

        interaction_id = str(interaction.data["custom_id"])

        if interaction_id == "open_rooms": # If the interaction is a button click with the custom_id "open_rooms"
            print("Open Rooms Button Clicked")

            # Get the guild object
            guild = bot.get_guild(interaction.guild_id)

            category_name = "Fikir Pazarı"
            category = await guild.create_category(category_name)

            
            group = []
            index = 1
            global roles
            roles = []

            tableDict = table.all()
            random.shuffle(tableDict)
            
            for record in tableDict:

                #TODO: Do we need to randomize the groups? Or is it already randomized in the airtable?

                if len(group) == 5:
                    
                    await group_members(guild, group, category, index)                             

                    #TODO: Adjust voice channel permissions to only allow the role to connect
                    group = []
                    group.append(str(record["fields"]["Discord Username"]))
                    index += 1
                else:
                    group.append(str(record["fields"]["Discord Username"]))

            await group_members(guild, group, category, index) # Last group
                             


            #TODO: Adjust voice channel permissions to only allow the role to connect

        elif interaction_id == "close_rooms": # If the interaction is a button click with the custom_id "close_rooms"
            print("Close Rooms Button Clicked")

            # Get the guild object
            guild = bot.get_guild(interaction.guild_id)

            for channel in guild.voice_channels:
                if channel.category.name == "Fikir Pazarı":
                    await channel.delete()

            for role in roles:
                await role.delete()
            
            for category in guild.categories:
                if category.name == "Fikir Pazarı":
                    await category.delete()
            
            #TODO: Can we send a dm to the participants to get a feedback? Another modal?

        elif interaction_id == "last_minute_announcement":
            print("Last Minute Announcement Button Clicked")
        elif interaction_id == "activity_join_button":
            print("Activity Join Button Clicked")
            modal = ActivityModal(title="Etkinlik Kayıt Formu")
            await interaction.response.send_modal(modal)
        else:
            # await interaction.response.send_message("This button is no longer active.", ephemeral=True)
            print(f"Ben bu butonu tanımıyorum abi, tanıdıklarım bunlar: \n {views}")

#TODO: @commands.is_owner() use this to restrict the command to the owner of the bot.


# Step 5: Main Entry Point
def main():
    bot.run(token=TOKEN)

    

async def group_members(guild, group, category, index):
    print(group)
    channel_name = f"Fikir Pazarı Odası {index}"
    channel = await guild.create_voice_channel(channel_name, category=category)

    role = await guild.create_role(name=channel_name)
    roles.append(role)

    await channel.set_permissions(guild.default_role, connect=False)
    await channel.set_permissions(role, connect=True)

    for username in group:
        try:
            member = guild.get_member_named(username)
            await member.add_roles(role)
        except AttributeError:
            print(f"{username} is not a member of the guild")

    

if __name__ == "__main__":
    main()