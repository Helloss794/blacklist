import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

class ReportModal(discord.ui.Modal, title="รายงานบัญชีดำ"):

    name = discord.ui.TextInput(label="ชื่อผู้ถูกรายงาน")
    reason = discord.ui.TextInput(
        label="เหตุผล",
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction):

        embed = discord.Embed(
            title="🚫 รายงานบัญชีดำ",
            color=discord.Color.red()
        )

        embed.add_field(
            name="ผู้ถูกรายงาน",
            value=self.name.value,
            inline=False
        )

        embed.add_field(
            name="เหตุผล",
            value=self.reason.value,
            inline=False
        )

        embed.add_field(
            name="ผู้รายงาน",
            value=interaction.user.mention,
            inline=False
        )

        channel = bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ ส่งรายงานแล้ว",
            ephemeral=True
        )

class ReportView(discord.ui.View):

    @discord.ui.button(
        label="รายงาน",
        emoji="🚫",
        style=discord.ButtonStyle.danger
    )
    async def report(self, interaction, button):
        await interaction.response.send_modal(
            ReportModal()
        )

@bot.tree.command(name="blacklistpanel")
async def blacklistpanel(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🚫 รายงานบัญชีดำ",
        description="กดปุ่มด้านล่าง",
        color=discord.Color.red()
    )

    await interaction.response.send_message(
        embed=embed,
        view=ReportView()
    )

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(bot.user)

bot.run(TOKEN)