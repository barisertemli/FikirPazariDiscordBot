import discord
import os
from pyairtable import Api, Table

api = Api(os.environ.get("AIRTABLE_TOKEN"))
table = api.table(os.environ.get("AIRTABLE_BASE_ID"), "Week1")

#TODO: Create a function to create a new table for each week.

class ButtonView(discord.ui.View): # This is a class for the view of the button.
    def __init__(self):
        super().__init__(timeout=None)  # Keep the view active indefinitely

    @discord.ui.button(label="Etkinlik Kayıt", style=discord.ButtonStyle.primary) # This is the button that will be shown.
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button): # This is the function that will be called when the button is clicked.
        await interaction.response.send_message(content="Bana tıkladın!", ephemeral=True)
        

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # self.add_item(discord.ui.TextInput(label="Short Input"))
        answer = self.add_item(discord.ui.TextInput(label="Bugün ne konuşacaksın?",
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
        
        