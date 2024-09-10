import discord
import os
from pyairtable import Api, Table

api = Api(os.environ.get("AIRTABLE_TOKEN"))
table = api.table(os.environ.get("AIRTABLE_BASE_ID"), "Week1")

#TODO: Create a function to create a new table for each week.

"""class SingleButton(discord.ui.View):
    def _init_(self):
        super()._init_(timeout=None)

    @discord.ui.button(label="Etkinliğe Kaydol",style=discord.ButtonStyle.blurple, custom_id="activity_join_button")
    async def activityJoin(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Etkinliğe kaydoldun!", ephemeral=True)
        print(f"Button {button.custom_id} has been clicked by {interaction.user.name}")"""

class ControlPanel(discord.ui.View):
    def _init_(self):
        super()._init_(timeout=None)

    @discord.ui.button(label="Odaları Aç",style=discord.ButtonStyle.green, custom_id="open_rooms")
    async def openRooms(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Odaları açtım!")
        print(f"Button {button.custom_id} has been clicked by {interaction.user.name}")

    @discord.ui.button(label="Odaları Kapat",style=discord.ButtonStyle.red, custom_id="close_rooms")
    async def closeRooms(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Odaları kapattım!")
        print(f"Button {button.custom_id} has been clicked by {interaction.user.name}")

    @discord.ui.button(label="Son Dakika Duyurusu",style=discord.ButtonStyle.blurple, custom_id="last_minute_announcement")
    async def announcement(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Duyuru geçmeye başlıyorum!")
        print(f"Button {button.custom_id} has been clicked by {interaction.user.name}")
        

class ActivityModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.add_item(discord.ui.TextInput(label="Short Input"))
        self.add_item(discord.ui.TextInput(custom_id="topic",
                                           label="Bugün ne konuşacaksın?",
                                           style=discord.TextStyle.long,
                                           placeholder="Buraya verdiğin bilgiler sosyal medya içeriklerimizde kullanılma amacıyla kaydedilecektir."))
        
    async def on_submit(self, interaction: discord.Interaction):

        #TODO: Use this data to save the user input to a Airtable database.
        #TODO: Her hafta farklı bir etkinlik olacak. Otomatik yeni table'a kaydetmeyi nasıl yaparız?

        print(interaction.data) # This is the data that is sent when the modal is submitted.
        # {'custom_id': '0e7d4802478d24ec4e9f86c5a0ef66fd', 'components': [{'type': 1, 'components': [{'value': 'deneme', 'type': 4, 'custom_id': '1af1929cd7fc33240fb5034b50d5b25c'}]}]}

        print(interaction.user.name) # This is the user that sent the data.

        await interaction.response.send_message("Formunuz gönderildi! Katkınız için teşekkürler.", ephemeral=True) # This is the message that will be sent when the modal is submitted.
        table.create({"Discord Username": interaction.user.name,
                      "Topic": interaction.data["components"][0]["components"][0]["value"]})
        
        