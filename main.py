import os

from dotenv import load_dotenv
import discord
from responses import get_response

# Step 0: Load the Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Step 1: Bot Setup
intents = discord.Intents.default() # Intents are the permissions to see the messages.
intents.message_content = True # Normally Python doesn't like it? We set it True to let bot to see the messages.
client = discord.Client(intents=intents)

# Step 2: Message Functionality


# Step 3: Startup
@client.event
async def on_ready():
    print(f"{client.user} is alive!")

# Step 4: Handling Incoming Messages



# Step 5: Main Entry Point
def main():
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()