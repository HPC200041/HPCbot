import os
import global_value as g
import Generic_Function as GF
import csv


def login(branch, message, index):
    flag = 0
    i = 0

    # csvファイルの中身をdata変数の中に格納する(配列データ)
    data = GF.csv_open("pass_data.csv")

    print(data)

    if branch == 0:
        # dataの中身を一つずつ参照し、入力ユーザーネームと一致したらフラグを返す
        for x in data:
            if data[0][i] == message[8:]:
                flag += 1
                index = i
                break
            i += 1
        pass

    if branch == 1:
        # dataの中身を一つずつ参照し、入力パスワードと一致したらフラグを返す
        for x in data:
            if data[1][i] == message[6:] and index == i:
                flag += 1
                break
            i += 1
        pass

    return flag, index

    file_path.close()
