import os
import global_value as g
import csv


# CSVファイルの読み込みから配列への格納までを行う関数
def scv_open(file_name):
    # 読み込むファイルのワーキングディレクトリを指定
    dir_path = r"discord_bot/"

    # ファイル名を、ワーキングディレクトリと連結する。
    file_path = os.path.join(dir_path, file_name)

    # csvファイルの中身をdata変数の中に格納する(配列データ)
    with open(file_path, "r") as f:
        i = 0
        data = list(csv.reader(f))

    return data
