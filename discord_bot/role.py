import discord
import os
import csv
import global_value as g
import Generic_Function as GF

role_1 = 1122713232386314341  # 一年生(電情1年)のロールID
role_2 = 1196346136567492689  # 二年生(電情2年)のロールID
role_3 = 1196346423344644136  # 三年生(生産1年)のロールID
role_4 = 1196346701309546567  # 四年生(生産2年)のロールID


def role_add(User_name):
    # csvファイルに関する処理（詳細はGeneric_Function.pyを参照）
    flag = 0
    i = 0

    data = GF.csv_open("pass_data.csv")

    # dataの中身を一つずつ参照し、入力ユーザーネームと一致したら、ユーザーネームに紐づけされたロール用データを参照し、ロールを付与する。
    for x in data:
        if data[0][i] == User_name:
            if data[2][i] == "1":
                return role_1
        i += 1
    pass
