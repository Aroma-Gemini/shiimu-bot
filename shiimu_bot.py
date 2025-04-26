import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Botの基本設定
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 役職リスト
roles_base = ["デュエリスト", "イニシエーター", "コントローラー", "センチネル"]
extra_roles = ["フレックス", "コーチ"]

# 役職と色絵文字の対応表
role_emojis = {
    "デュエリスト": "🔴",
    "イニシエーター": "🟢",
    "コントローラー": "🔵",
    "センチネル": "🟡",
    "フレックス": "⚪",
    "コーチ": "🎓"
}

class AssignRolesButtonView(View):
    def __init__(self, ctx, vc_members):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.vc_members = vc_members
        self.results_shown = False

    @discord.ui.button(label="🎲START🎲", style=discord.ButtonStyle.success)
    async def start_assigning(self, interaction: discord.Interaction, button: Button):
        if self.results_shown:
            await interaction.response.send_message("もう結果は表示されてるよ！", ephemeral=True)
            return

        self.results_shown = True

        member_count = len(self.vc_members)
        selected_roles = []

        if member_count == 1:
            selected_roles = ["フレックス"]
        elif member_count == 2:
            selected_roles = random.sample(roles_base, 2)
        elif member_count == 3:
            selected_roles = random.sample(roles_base, 3)
        elif member_count == 4:
            selected_roles = roles_base.copy()
        elif member_count == 5:
            selected_roles = roles_base + ["フレックス"]
        elif member_count == 6:
            selected_roles = roles_base + extra_roles
        else:
            await interaction.response.send_message("❌ 人数が多すぎます！7人以上には対応していません。", ephemeral=True)
            return

        # メッセージ作成
        result_msg = "**🎮 役割発表 🎮**\n"
        for member, role in zip(self.vc_members, selected_roles):
            emoji = role_emojis.get(role, "")
            result_msg += f"{member.mention} ➔ {emoji} **{role}**\n"

        await interaction.response.send_message(result_msg)

@bot.command()
async def shiimu(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        vc = ctx.author.voice.channel
        vc_members = [member for member in vc.members if not member.bot]

        if not vc_members:
            await ctx.send("ボイスチャンネルに誰もいないよ！")
            return

        await ctx.send("🎮 ボイスチャンネルの人数を確認したよ！\n🎲START🎲 ボタンを押して役割を決めよう！", view=AssignRolesButtonView(ctx, vc_members))
    else:
        await ctx.send("まずボイスチャンネルに参加してね！")

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
