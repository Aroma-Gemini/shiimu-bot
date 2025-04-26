import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import os
from dotenv import load_dotenv

# .envからトークンを読み込む
load_dotenv()

# 色付き役割変換
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
bot = commands.Bot(command_prefix="!", intents=intents)

# 配置する役職
roles_basic = ["デュエリスト", "イニシエーター", "コントローラー", "センチネル"]
roles_flex = roles_basic + ["フレックス"]

class StartButtonView(View):
    def __init__(self, ctx, player_count):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.player_count = player_count

    @discord.ui.button(label="🎲START🎲", style=discord.ButtonStyle.success)
    async def start(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("このボタンはコマンドを使った人専用です！", ephemeral=True)
            return

        player_count = self.player_count

        if player_count == 1:
            roles = [get_colored_role("フレックス")]
            text = f"プレイヤー ➔ {roles[0]}"
            await interaction.response.send_message(f"🎲 1人プレイ\n{text}")

        elif 2 <= player_count <= 4:
            selected_roles = random.sample(roles_basic, player_count)
            text = "\n".join(f"プレイヤー{idx+1} ➔ {get_colored_role(role)}" for idx, role in enumerate(selected_roles))
            await interaction.response.send_message(f"🎲 {player_count}人プレイ\n{text}")

        elif player_count == 5:
            selected_roles = random.sample(roles_flex, 5)
            text = "\n".join(f"プレイヤー{idx+1} ➔ {get_colored_role(role)}" for idx, role in enumerate(selected_roles))
            await interaction.response.send_message(f"🎲 5人プレイ\n{text}")

        elif 6 <= player_count <= 9:
            await interaction.response.send_message("⚠ プレイできる人数ではありません！")

        elif player_count == 10:
            selected_roles = random.sample(roles_flex, 5)
            selected_roles_b = random.sample(roles_flex, 5)

            team_a_text = "\n".join(f"Aチーム プレイヤー{idx+1} ➔ {get_colored_role(role)}" for idx, role in enumerate(selected_roles))
            team_b_text = "\n".join(f"Bチーム プレイヤー{idx+1} ➔ {get_colored_role(role)}" for idx, role in enumerate(selected_roles_b))

            await interaction.response.send_message(f"🎲 10人プレイ\n\n{team_a_text}\n\n{team_b_text}")

        else:
            await interaction.response.send_message("⚠ 人数が多すぎます！")

# !shiimu コマンド
@bot.command()
async def shiimu(ctx, player_count: int):
    if player_count < 1:
        await ctx.send("人数は1人以上を入力してください！")
        return

    view = StartButtonView(ctx, player_count)
    await ctx.send(f"🎲 {player_count}人でスタートする準備ができました！ボタンを押してね！", view=view)

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
