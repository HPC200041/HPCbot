import os

# 自動ダウンロード用モジュール
import requests
import global_value as g
import csv

Rain = 1
Wind_Speed = 2


def Wf_download(mode):
    # 降水量(一時間あたり)取得処理
    if mode == Rain:
        response = requests.get(
            "https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/pre1h00_rct.csv"
        )

        # 降水量ファイルを上書き
        file = open("Precipitation.csv", "w")

        # ファイルを上書き保存(100kBごと)
        for chunk in response.iter_content(100 * 1024):
            file.write(chunk)

        # ファイル保存完了
        file.close()

    # 風速取得処理(最大風速(風速/10min)と、瞬間最大風速(風速/3sec))
    elif mode == Wind_Speed:
        # 最大風速データを取得
        response = requests.get(
            "https://www.data.jma.go.jp/obd/stats/data/mdrr/wind_rct/alltable/mxwsp00_rct.csv"
        )

        # 最大風速ファイルを上書き
        file = open("Wind_speed.csv", "w")

        # ファイルを上書き保存(100kBごと)
        for chunk in response.iter_content(100 * 1024):
            file.write(chunk)

        # ファイル保存完了
        file.close()

        # 瞬間最大風速データを取得
        response = requests.get(
            "https://www.data.jma.go.jp/obd/stats/data/mdrr/wind_rct/alltable/gust00_rct.csv"
        )

        # 最大風速ファイルを上書き
        file = open("Wind_Max_speed.csv", "w")

        # ファイルを上書き保存(100kBごと)
        for chunk in response.iter_content(100 * 1024):
            file.write(chunk)

        # ファイル保存完了
        file.close()


def Weather_forecast():
    # 降水量データをダウンロード
    Wf_download(Rain)
    # Precipitation.csv


Weather_forecast()
