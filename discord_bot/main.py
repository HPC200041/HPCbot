import discord

# アクセストークンを読み込み
import env

# ログイン用関数を読み込み
import Login

# ロール付与関数を読み込み
import role

# 天気予報用ファイルを読み込み
import Weather_forecast as WF

# 運行状況用関数を読み込み
import Sculpation as Sc

# グローバル変数用ファイルを「g」として読み込み
import global_value as g

# csv管理用のcsvを読み込み
import csv

import json

from typing import List

# 時間指定系を読み込み
from discord.ext import tasks

from datetime import date, timedelta, datetime

from time import sleep

import schedule

import os

from concurrent.futures import ThreadPoolExecutor

import Generic_Function as GF

from discord import Intents, Client, Interaction
from discord import app_commands

from discord.ext import commands


# インテントの設定
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# ログイン関数に必要な変数を定義
Login_List: List[str] = []  # ログイン関数の返却内容を一時保存するためのリスト

# ロール付与関数に必要な変数を定義
Role_List: List[int] = []  # ロール付与関数の返却内容を一時保存するためのリスト

# サーバーID(ギルドID)を登録
Sever_ID = 1115861243035652156

tree = app_commands.CommandTree(client)


# CSVファイルの方の処理
@tree.command(name="wf_now", description="一時間以内の気象状況をお知らせします。")
async def default_command(interaction: discord.Interaction):

    Des = WF.Weather_Inform()
    embed = discord.Embed(title="> **現在の天気**", description=Des, color=0xFF0000)
    await interaction.response.send_message(embed=embed)


# JSONファイルの方の処理
@tree.command(name="wf_day", description="今日の天気予報をお知らせします。")
async def default_command(interaction: discord.Interaction):

    description = WF.Weather_Forecast()
    embed = discord.Embed(
        title="> 本日24時間の天気", description=description[0], color=0xFF0000
    )
    file = discord.File(fp="discord_bot/plot.png", filename="plot.png", spoiler=False)
    embed.set_image(url=f"attachment://plot.png")
    if description[1] == 0:
        embed.set_thumbnail(
            url="https://3.bp.blogspot.com/-93EsFuhpCKo/UNbgb6ZaNHI/AAAAAAAAJPE/ZIVJ0VqJSRM/s180/mark_tenki_hare.png"  # 晴れ
        )
    elif description[1] == 1:
        embed.set_thumbnail(
            url="https://3.bp.blogspot.com/-a148-_9uwxU/UNbgiw9khuI/AAAAAAAAJP4/c5FPmhaSKhc/s180/mark_tenki_umbrella.png"
        )  # 雨

    # 結果を返信します。
    await interaction.response.send_message(file=file, embed=embed)


@bot.command()
async def test(ctx):
    pass


@tasks.loop(seconds=60)
async def loop():
    # botが起動するまで待つ
    await client.wait_until_ready()
    channel = client.get_channel(1177415968222351411)
    await channel.send("時間だよ")


"""
# 01 定期実行する関数を準備
def task(work):
    print(work + "タスク実行中")
"""


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print(f"{client.user}がログインしました")

    for channel in client.get_all_channels():
        print("----------")
        print("チャンネル名：" + str(channel.name))
        print("チャンネルID：" + str(channel.id))
        print("----------")

    WF.Wf_download(1)
    WF.Wf_download(2)
    download_API()

    await tree.sync()  # スラッシュコマンドを同期


# メンバー新規参加者取得
@client.event
async def on_member_join(member):
    embed = discord.Embed(
        title="> **電情Discord支部へようこそ！**",
        description="本サーバーにはログイン機能が存在しています。\n学校で配布されたユーザー名を、以下のフォーマットに従って送信してください。\n\nユーザーネーム：\nパスワード：\n\n投稿例\nユーザーネーム：za2200000\nパスワード：2200000za",
        color=0xFF0000,
    )
    await member.send(embed=embed)


# メッセージ受信時に動作する処理
@client.event
async def on_message(message: discord.Message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author == client.user:
        return

    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content.startswith("/neko"):
        await message.channel.send("にゃーん")

    if message.content.startswith("天気予報"):
        await message.channel.send(WF.Weather_Inform())

    if message.content.startswith("運行状況"):
        box = Sc.delay_information()
        if type(box[0]) == int:  # 最初に区別用の数字があれば分岐
            box = list(box)

            embed = discord.Embed(
                title="札幌近郊の鉄道運行状況",
                description="現在の札幌近郊の鉄道遅延状況です。\n詳細はタイトルから確認するようお願いします",
                color=0x000000,
                url="https://transit.yahoo.co.jp/diainfo/area/2",
            )

            for i in range(len(box[1])):  # 遅延が発生している路線を全てFieldで出力
                embed.add_field(name=box[1][i], value=box[2][i], inline=False)

            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="札幌近郊の鉄道運行状況",
                description=box,
                color=0x000000,
                url="https://transit.yahoo.co.jp/diainfo/area/2",
            )
            await message.channel.send(embed=embed)

    if message.content.startswith("JSON"):
        description = WF.Weather_Forecast()
        embed = discord.Embed(title="", description=description[0], color=0xFF0000)
        file = discord.File(
            fp="discord_bot/plot.png", filename="plot.png", spoiler=False
        )
        embed.set_image(url=f"attachment://plot.png")
        if description[1] == 0:
            embed.set_thumbnail(
                url="https://3.bp.blogspot.com/-93EsFuhpCKo/UNbgb6ZaNHI/AAAAAAAAJPE/ZIVJ0VqJSRM/s180/mark_tenki_hare.png"  # 晴れ
            )
        elif description[1] == 1:
            embed.set_thumbnail(
                url="https://3.bp.blogspot.com/-a148-_9uwxU/UNbgiw9khuI/AAAAAAAAJP4/c5FPmhaSKhc/s180/mark_tenki_umbrella.png"
            )  # 雨
        await message.channel.send(file=file, embed=embed)

        # https://1.bp.blogspot.com/-3_9UVV8GT_4/UR2iwuHZcSI/AAAAAAAAMx8/dSxZ8XCFaes/s180/tenki_snow.png

    # DMに送信されたメッセージの場合、処理を行う。
    if isinstance(message.channel, discord.DMChannel):
        # メッセージの内容を疑似グローバル関数に格納
        g.str = message.content

        member = client.get_guild(Sever_ID).get_member(
            message.author.id
        )  # ギルドオブジェクトを取得し、サーバー内にユーザーがいるか捜索。捜索結果を保存する。

        if member is not None:
            # フォーマットに従っているか確認
            if message.content[0:8] == "ユーザーネーム：":
                Username = message.content[
                    : message.content.find("\n")
                ]  # ユーザー名部分のみを抽出
                Password = message.content[
                    message.content.find("\n") + 1 :
                ]  # パスワード部分のみを抽出

                Login_List = Login.login(0, Username, 0)
                if (
                    Login_List[0] == 1
                ):  # login関数のフラグ部分が1を返したならば、パスワードを確認する
                    Login_List = Login.login(1, Password, Login_List[1])
                    if (
                        Login_List[0] == 1
                    ):  # パスワード認証処理でlogin関数のフラグが1であるならば、権限付与処理を行う
                        await member.add_roles(
                            member.guild.get_role(role.role_add(Username[8:]))
                        )  # ユーザーネームをロール付与関数に渡し、返却されたロールIDを使ってロールを付与する。
                        await message.channel.send(
                            "ログインに成功しました。\nパスワードの入力ログを削除してください"
                        )

                        # メンバーにロールを付与する。
                        # channel = client.get_channel(チャンネルID)
                        # member = channel.guild.get_member(メンバーID)
                        # await channel.set_permissions(member,read_messages=True,send_messages=True)
                pass

            else:
                print("フォーマットにしたがって送信してください。")
            pass

        else:
            print(
                "あなたは北海道職業能力開発大学校公式Discordチャンネルに所属していません。\nまずは配布されたURLからサーバーに参加してください。"
            )


def download_API():
    # 3日後までの降水確率データを取得するためのURL
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=43.1333&longitude=141.1667&hourly=precipitation_probability&windspeed_unit=ms&timezone=Asia%2FTokyo&start_date="
        + str(date.today())
        + "&end_date="
        + str(date.today() + timedelta(days=3))
    )

    print(str(datetime.now()) + "[[JSON]]")

    # APIデータファイル上書き
    GF.json_write(url, "prediction_probability.json", "utf-8")


def download_CSV():
    Rain = 1
    Wind_Speed = 2

    print(str(datetime.now()) + "[[CSV]]")

    WF.Wf_download(Rain)
    WF.Wf_download(Wind_Speed)


# asyncio.run(async_func())


def main():
    pid_list = []

    pid_list.append(os.getpid())
    child_pid = (
        os.fork()
    )  # 『注意』Linux環境以外では動作しない！！！！！！！(じゃあなんでこのプログラム動いてんの....)

    if child_pid == 0:
        # scheduleはグリニッジ標準時でしか動かないカスであるためグリニッジ標準時に合わせる必要あり
        # 厳密には動作環境での時刻を参照しているらしく、動作環境の時刻を確認する必要がある。

        schedule.every().day.at("15:00").do(download_API)  # 日本時間0時に更新
        schedule.every().day.at("18:00").do(download_API)  # 日本時間3時に更新
        schedule.every().day.at("21:00").do(download_API)  # 日本時間6時に更新
        schedule.every().day.at("00:00").do(download_API)  # 日本時間9時に更新
        schedule.every().day.at("03:00").do(download_API)  # 日本時間12時に更新
        schedule.every().day.at("06:00").do(download_API)  # 日本時間15時に更新
        schedule.every().day.at("09:00").do(download_API)  # 日本時間18時に更新
        schedule.every().day.at("12:00").do(download_API)  # 日本時間21時に更新

        schedule.every(1).hours.do(download_CSV)  # 1時間ごとに更新

        while 1:
            schedule.run_pending()
            sleep(10)

    # client = Client()

    client.run(env.BOT_TOKEN)


schedule.run_pending()

# client = Client()

if __name__ == "__main__":
    main()


# Botの起動とDiscordサーバーへの接続
