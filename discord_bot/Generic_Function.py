import os
import global_value as g
import csv
import json
import itertools

# 自動ダウンロード用モジュール
import requests


# 受け取ったファイル名を、ワーキングディレクトリと連結して返却する。
def dile_path(file_name):
    return os.path.join(r"discord_bot/", file_name)


# CSVファイルの読み込みから配列への格納までを行う関数
def csv_open(file_name):
    # ファイルパスを取得
    file_path = dile_path(file_name)

    # csvファイルの中身をdata変数の中に格納する(配列データ)
    with open(file_path) as f:
        i = 0
        data = list(csv.reader(f))
        f.close()

    return data


# URL先のJSONファイルをダウンロード、または渡されたデータを参照し、様々な処理を行う関数
# 処理内容は上書き保存
def json_write(URL, file_name, decode_type):
    file_path = dile_path(file_name)

    # 上書き保存のみを行うモード
    response = requests.get(URL)
    main_text = response.content.decode(decode_type)

    # ファイルを上書き

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(main_text)

    file.close()


# JSONファイルの読み込みから配列への格納までを行う関数
def json_open(file_name):
    # ファイルパスを取得
    file_path = dile_path(file_name)
    with open(file_path, mode="rt", encoding="utf-8") as file:
        data = json.load(file)

    file.close()
    return data


# URL先のCSVファイルをダウンロード、または渡されたデータを参照し、様々な処理を行う関数
# 処理内容は上書き保存
def csv_write(URL, file_name, decode_type):
    # ファイルパスを取得
    file_path = dile_path(file_name)

    # 上書き保存のみを行うモード
    response = requests.get(URL)
    main_text = response.content.decode(decode_type)

    # ファイルを上書き

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(main_text)

    file.close()

    # データを取得し、範囲を指定して上書き保存を行うモード
    # (出力は引数ファイル名 + _out_put)
    # elif mode == 1:
    # データを取得
    # response = requests.get(URL)

    # csvファイルの中身をreaderの中に格納する
    # with open(file_path, "w") as i_f:
    # reader = csv.reader(i_f)
    # 出力ファイルを開く
    # with open(file_path + "_out_put", "w") as o_f:
    # writer = csv.writer(o_f)
    # [head]行目から[end]行目を抽出し、上書き保存(Listで一行ずつ書き込みをしている点に注意)
    # writer.writerow(reader[head:end])
    # file.close()
    # file.close()

    # URL先のCSVファイルをダウンロードまたは読み込みを行い、指定範囲を抽出して追記を行う関数
    # (出力先は引数ファイル名 + _range_out_put)
    # if mode == 2:
    # ファイルパスを取得
    # file_path = dile_path(file_name)

    # csvファイルの中身をdata変数の中に格納する(配列データ)
    # with open(file_name + "csv", "r") as input_file:
    # reader = csv.reader(input_file)
    # 出力ファイルを開く
    # with open(file_name + "_range_out_put" + "csv", "w") as o_f:
    # writer = csv.writer(o_f)
    # [head]行目から[end]行目を抽出し、上書き保存(Listで一行ずつ書き込みをしている点に注意)
    # writer.writerow(reader[head:end])
    # file.close()
    # file.close()


# dict(辞書型)を分割して別のdictに格納するプログラム(コピペ)
# https://ssrv.net/tech/python-dict-slice/
def dict_chunks(data, size):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k: data[k] for k in itertools.islice(it, size)}


# 辞書型を降順にソートしなおし、辞書型に変換して返却
def dict_sort(dict):
    dict_data = {}

    dict_data.update(next(dict_chunks(dict, 24)))

    # キーと値を同時にソート
    sorted_data = sorted(dict_data.items(), key=lambda x: (x[1]), reverse=True)

    return sorted_data


# 辞書型配列を区切って別変数に格納して返却する
def Dict_set(dict, set, ary1, ary2):
    for i in range(ary1):
        set = {i: (ary1[i], ary2[i])}

    return set
