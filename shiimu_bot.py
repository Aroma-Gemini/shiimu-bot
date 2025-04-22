import discord
from discord.ext import commands
from discord.ui import Button, View
import random

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

roles = ["デュエリスト", "イニシエーター", "コントローラー", "センチネル", "フレックス"]
animal_emojis = ["🐶", "🐱", "🐭", "🐹", "🐼"]
joined_users = []

class ResultButtonView(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.results_shown = False

    @discord.ui.button(label="🎲結果を表示する", style=discord.ButtonStyle.primary)
    async def show_results(self, interaction: discord.Interaction, button: Button):
        if self.results_shown:
            await interaction.response.send_message("もう結果は表示されたよ！", ephemeral=True)
            return

        self.results_shown = True
        random.shuffle(roles)
        result_msg = "**🎮 担当発表 🎮**\n"
        for user, role in zip(joined_users, roles):
            result_msg += f"{user.mention} の担当は **{role}** です！\n"
        await interaction.response.send_message(result_msg)

@bot.command()
async def shiimu(ctx):
    global joined_users
    joined_users = []  # 初期化

    msg = await ctx.send(
        "全部表示されてから、好きな動物をクリックしてリアクションして参加してね！\n"
        "人が選んだ動物を選らんでしまうとエラーになっちゃうよ！\n"
        "参加者が揃ったら ボタンで結果を表示してね！"
    )

    for emoji in animal_emojis:
        await msg.add_reaction(emoji)

    view = ResultButtonView(ctx)
    await ctx.send(view=view)

    def check(reaction, user):
        return (
            user != bot.user and
            reaction.message.id == msg.id and
            user not in joined_users and
            str(reaction.emoji) in animal_emojis
        )

    while len(joined_users) < 5:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=300.0, check=check)
            joined_users.append(user)
        except:
            break  # タイムアウトなどで抜ける

    if len(joined_users) == 5 and not view.results_shown:
        view.results_shown = True
        random.shuffle(roles)
        result_msg = "**🎮 担当発表 🎮**\n"
        for user, role in zip(joined_users, roles):
            result_msg += f"{user.mention} の担当は **{role}** です！\n"
        await ctx.send(result_msg)

import os
from dotenv import load_dotenv

# .envの読み込み
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 省略：bot の設定など

bot.run(TOKEN)
