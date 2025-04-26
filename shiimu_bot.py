intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Modal, TextInput
import random
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

roles = {
    "デュエリスト": discord.Color.red(),
    "イニシエーター": discord.Color.green(),
    "コントローラー": discord.Color.blue(),
    "センチネル": discord.Color.yellow(),
    "フレックス": discord.Color.light_grey()
}

class NumberInputModal(Modal, title="人数を入力してください"):
    number = TextInput(label="人数", placeholder="1～10", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.number_value = int(self.number.value)
        except ValueError:
            await interaction.response.send_message("数字を入力してね！", ephemeral=True)
            return

        if self.number_value < 1 or self.number_value > 10:
            await interaction.response.send_message("1〜10人の間で入力してね！", ephemeral=True)
            return

        view = StartButtonView(self.number_value)
        await interaction.response.send_message("人数設定完了！🎲START🎲ボタンを押してね！", view=view, ephemeral=True)

class StartButtonView(View):
    def __init__(self, number_value):
        super().__init__(timeout=None)
        self.number_value = number_value

    @discord.ui.button(label="🎲START🎲", style=discord.ButtonStyle.primary)
    async def start(self, interaction: discord.Interaction, button: Button):
        vc = interaction.guild.voice_client
        voice_channel = None
        for vc in interaction.guild.voice_channels:
            if interaction.user in vc.members:
                voice_channel = vc
                break

        if not voice_channel:
            await interaction.response.send_message("あなたはボイスチャンネルにいないよ！", ephemeral=True)
            return

        members = [member for member in voice_channel.members if not member.bot]

        if len(members) < self.number_value:
            # 人数少ない場合はそのまま指定人数だけ選ぶ
            selected_members = random.sample(members, len(members))
        elif len(members) == self.number_value:
            selected_members = members
        else:
            await interaction.response.send_message("人数が合わないよ！", ephemeral=True)
            return

        result = ""

        if self.number_value == 1:
            role_list = ["フレックス"]
        elif self.number_value in [2, 3, 4]:
            role_list = random.sample(["デュエリスト", "イニシエーター", "コントローラー", "センチネル"], k=self.number_value)
        elif self.number_value == 5:
            role_list = random.sample(["デュエリスト", "イニシエーター", "コントローラー", "センチネル", "フレックス"], k=5)
        elif 6 <= self.number_value <= 9:
            await interaction.response.send_message("プレイ出来る人数ではありません！", ephemeral=True)
            return
        elif self.number_value == 10:
            random.shuffle(members)
            team_a = members[:5]
            team_b = members[5:]

            roles_list = ["デュエリスト", "イニシエーター", "コントローラー", "センチネル", "フレックス"]

            result += "**Aチーム**\n"
            for member, role in zip(team_a, roles_list):
                result += f"{member.mention} → `{role}`\n"

            result += "\n**Bチーム**\n"
            for member, role in zip(team_b, roles_list):
                result += f"{member.mention} → `{role}`\n"

            await interaction.response.send_message(result)
            return
        else:
            await interaction.response.send_message("人数が多すぎます！", ephemeral=True)
            return

        # 通常表示
        for member, role in zip(selected_members, role_list):
            color = roles[role]
            result += f"{member.mention} → `{role}`\n"

        await interaction.response.send_message(result)

@bot.command()
async def shiimu(ctx):
    modal = NumberInputModal()
    await ctx.send_modal(modal)

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
