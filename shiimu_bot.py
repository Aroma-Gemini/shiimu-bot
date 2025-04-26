import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import os
from dotenv import load_dotenv

# .envからトークンを読み込む
load_dotenv()

# 色をつける関数
def get_colored_role(role):
    color_map = {
        "デュエリスト": "🔴 **デュエリスト**",
        "イニシエーター": "🟢 **イニシエーター**",
        "コントローラー": "🔵 **コントローラー**",
        "センチネル": "🟡 **センチネル**",
        "フレックス": "⚪ **フレックス**"
    }
    return color_map.get(role, role)

# Bot設定
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 配置する役職
roles_basic = ["デュエリスト", "イニシエーター", "コントローラー", "センチネル"]
roles_flex = roles_basic + ["フレックス"]

class StartButtonView(View):
    def __init__(self, ctx, voice_members):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.voice_members = voice_members

    @discord.ui.button(label="🎲START🎲", style=discord.ButtonStyle.success)
    async def start(self, interaction: discord.Interaction, button: Button):
        if interaction.user.voice is None:
            await interaction.response.send_message("ボイスチャンネルに参加していないと使えません！", ephemeral=True)
            return

        # ボイスチャンネルにいる人数を数える
        member_count = len(self.voice_members)

        if member_count == 1:
            roles = [get_colored_role("フレックス")]
            members = list(self.voice_members)
            text = f"{members[0].mention} ➔ {roles[0]}"
            await interaction.response.send_message(f"🎲 1人プレイ\n{text}")

        elif 2 <= member_count <= 4:
            selected_roles = random.sample(roles_basic, member_count)
            members = list(self.voice_members)
            random.shuffle(members)
            text = "\n".join(f"{m.mention} ➔ {get_colored_role(r)}" for m, r in zip(members, selected_roles))
            await interaction.response.send_message(f"🎲 {member_count}人プレイ\n{text}")

        elif member_count == 5:
            selected_roles = random.sample(roles_flex, 5)
            members = list(self.voice_members)
            random.shuffle(members)
            text = "\n".join(f"{m.mention} ➔ {get_colored_role(r)}" for m, r in zip(members, selected_roles))
            await interaction.response.send_message(f"🎲 5人プレイ\n{text}")

        elif 6 <= member_count <= 9:
            await interaction.response.send_message("⚠ プレイできる人数ではありません！")

        elif member_count == 10:
            team_members = list(self.voice_members)
            random.shuffle(team_members)

            team_a = team_members[:5]
            team_b = team_members[5:]

            selected_roles_a = random.sample(roles_flex, 5)
            selected_roles_b = random.sample(roles_flex, 5)

            team_a_text = "\n".join(f"{m.mention} ➔ {get_colored_role(r)}" for m, r in zip(team_a, selected_roles_a))
            team_b_text = "\n".join(f"{m.mention} ➔ {get_colored_role(r)}" for m, r in zip(team_b, selected_roles_b))

            await interaction.response.send_message(f"🎲 10人プレイ\n\n**Aチーム**\n{team_a_text}\n\n**Bチーム**\n{team_b_text}")

        else:
            await interaction.response.send_message("⚠ 人数が多すぎます！")

# !shiimu コマンド
@bot.command()
async def shiimu(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("ボイスチャンネルに参加してからコマンドを使ってください！")
        return

    voice_channel = ctx.author.voice.channel
    voice_members = voice_channel.members

    view = StartButtonView(ctx, voice_members)
    await ctx.send("🎲START🎲ボタンを押して役割を振り分けましょう！", view=view)


import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
