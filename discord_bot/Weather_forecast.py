import os

# 自動ダウンロード用モジュール
import requests
import global_value as g
import Generic_Function as GF
import csv

# ピーク検出関係
from scipy.signal import find_peaks

# グラフ関係
from matplotlib import pyplot as pyp
import japanize_matplotlib

from typing import List

import itertools

from datetime import date, timedelta, datetime


NULL = 0
Rain = 1
Wind_Speed = 2


# グラフ画像を作成し画像化して保存する
def Wf_prot(data):
    # figsizeは画像の縦横比を指定するものだが、(横：縦)になっている点に注意
    day = datetime.now()
    fig = pyp.figure(figsize=(6, 3), dpi=300, facecolor="w")
    fig.suptitle(t=str(day.date()) + "日の降水確率推移")
    ax = fig.add_subplot(111)
    ax.set_xlabel("時刻", fontsize=9)
    ax.set_ylabel("降水確率", fontsize=9)
    ax.xaxis.set_major_locator(pyp.MultipleLocator(2))
    ax.plot(data, marker="o", label="red")
    pyp.subplots_adjust(bottom=0.15)
    fig.savefig("discord_bot/plot.png")


def Wf_download(mode):
    # 降水量(一時間あたり)取得処理
    if mode == Rain:
        # 降水量データを取得し、上書き保存
        GF.csv_write(
            "https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/pre1h00_rct",
            "Precipitation.csv",
            "shift_jis",
        )
        print("降水量CSVファイルデータ更新")

    # 風速取得処理(最大風速(風速/10min)と、瞬間最大風速(風速/3sec))
    elif mode == Wind_Speed:
        # 最大風速データを取得し、上書き保存
        GF.csv_write(
            "https://www.data.jma.go.jp/obd/stats/data/mdrr/wind_rct/alltable/mxwsp00_rct",
            "Wind_speed.csv",
            "shift_jis",
        )

        # 瞬間最大風速データを取得し、上書き保存
        GF.csv_write(
            "https://www.data.jma.go.jp/obd/stats/data/mdrr/wind_rct/alltable/gust00_rct",
            "Wind_Max_speed.csv",
            "shift_jis",
        )
        print("風速関係CSVファイル更新")


# 現在の天気を教える
def Weather_Inform():
    # 降水量データをダウンロード

    # WF_Listに降水量データを移す
    WF_List = GF.csv_open("Precipitation.csv")

    # 雨が降っている場合
    if (float(WF_List[61][9]) > 0) and (float(WF_List[88][9]) == 0):
        Pre = "現在、手稲で雨が降っています。帰宅の際は足元に注意してください。\n"
    elif (float(WF_List[61][9]) == 0) and (float(WF_List[88][9]) > 0):
        Pre = "現在、小樽で雨が降っています。帰宅の際は足元に注意してください。\n"
    elif (float(WF_List[61][9]) > 0) and float((WF_List[88][9]) > 0):
        Pre = (
            "現在、銭函周辺地域で雨が降っています。帰宅の際は足元に注意してください。\n"
        )
    elif (float(WF_List[61][9]) == 0) and (float(WF_List[88][9]) == 0):
        Pre = "現在は特に降水は確認されていません。\n"

    # 美国または神恵内で雨が降っている場合
    if (WF_List[86][9] > "0") or (WF_List[87][9] > "0"):
        forecast = "小樽よりさらに西で雨が降っています。\n数時間以内に銭函地域でも雨が降る可能性があるため、外出する方は傘を忘れないようにしましょう。\n"

    WF_List = GF.csv_open("Wind_speed.csv")

    # 各地域の風の段階。詳細はビューフォート風力階級を参照
    Sapporo_Wind = 0
    Otaru_Wind = 0

    if float(WF_List[53][9]) >= 0 and float(WF_List[53][9]) < 5:
        Sapporo_Wind = 0  # 微風
    elif float(WF_List[53][9]) >= 5 and float(WF_List[53][9]) < 10:
        Sapporo_Wind = 1  # やや強い風
    elif float(WF_List[53][9]) >= 10 and float(WF_List[53][9]) < 17:
        Sapporo_Wind = 2  # かなり強い風
    elif float(WF_List[53][9]) >= 17:
        Sapporo_Wind = 3  # 出歩くのが危険なレベルの風

    if float(WF_List[71][9]) >= 0 and float(WF_List[71][9]) < 5:
        Otaru_Wind = 0  # 微風
    elif float(WF_List[71][9]) >= 5 and float(WF_List[71][9]) < 10:
        Otaru_Wind = 1  # やや強い風
    elif float(WF_List[71][9]) >= 10 and float(WF_List[71][9]) < 17:
        Otaru_Wind = 2  # かなり強い風
    elif float(WF_List[71][9]) >= 17:
        Otaru_Wind = 3  # 出歩くのが危険なレベルの風

    if Sapporo_Wind == 0 or Otaru_Wind == 0:
        if Sapporo_Wind == 0 and Otaru_Wind == 0:
            Ws = "現在、銭函周辺で強い風は吹いていません。"
        elif Sapporo_Wind == 1 and Otaru_Wind == 0:
            speed = WF_List[53][9]
            Ws = "現在札幌で" + str(speed) + "m/s程度のやや強い風が吹いています。"
        elif Sapporo_Wind == 2 and Otaru_Wind == 0:
            speed = WF_List[53][9]
            Ws = "現在札幌で" + str(speed) + "m/s程度のかなり強い風が吹いています。"
        elif Sapporo_Wind == 3 and Otaru_Wind == 0:
            speed = WF_List[53][9]
            Ws = "現在札幌で" + str(speed) + "m/s程度の極めて強い風が吹いています。"
        elif Sapporo_Wind == 0 and Otaru_Wind == 1:
            speed = WF_List[71][9]
            Ws = "現在小樽で" + str(speed) + "m/s程度のやや強い風が吹いています。"
        elif Sapporo_Wind == 0 and Otaru_Wind == 2:
            speed = WF_List[71][9]
            Ws = "現在小樽で" + str(speed) + "m/s程度のかなり強い風が吹いています。"
        elif Sapporo_Wind == 0 and Otaru_Wind == 3:
            speed = WF_List[71][9]
            Ws = "現在小樽で" + str(speed) + "m/s程度の極めて強い風が吹いています。"
    elif Sapporo_Wind > 0 or Otaru_Wind > 0:
        if Sapporo_Wind == 1 and Otaru_Wind == 1:
            Ws = "銭函周辺で微風が吹いています。"
        elif Sapporo_Wind == 2 or Otaru_Wind == 2:
            speed = max(WF_List[71][9], WF_List[53][9])
            Ws = (
                "銭函周辺で風が吹いているほか、一部地域で"
                + str(speed)
                + "m/s程度のかなり強い風が吹いています。\n外出の際は気を付けてください。"
            )
        elif Sapporo_Wind == 3 or Otaru_Wind == 3:
            Ws = (
                "銭函周辺で風が吹いているほか、一部地域で"
                + str(speed)
                + "m/s程度のかなり強い風が吹いています。\n外出は可能な限り控えてください"
            )

    """
    float(WF_List[53][9]) > 0 and float(WF_List[53][9]) < 10) and (
        WF_List[71][9] == "0"
    ):
        Ws = "現在、札幌で微風が吹いています。\n"
    elif (WF_List[53][9] == "0") and (WF_List[71][9] > "0"):
        Ws = "現在、小樽で強風が吹いています。帰宅の際は強風に注意してください。\n"
    elif (WF_List[53][9] > "0") and (WF_List[71][9] > "0"):
        Ws = "現在、銭函周辺地域で強風が吹いています。帰宅の際は強風に注意してください。\n"
    elif (WF_List[53][9] == "0") and (WF_List[71][9] == "0"):
        Ws = "現在は特に強風は確認されていません。\n"

    WF_List = GF.csv_open("Wind_Max_speed.csv")

    if (WF_List[53][9] > "0") and (WF_List[71][9] == "0"):
        WMs = "現在、札幌で突発的な強風が吹いています。帰宅の際は強風に注意してください。\n"
    elif (WF_List[53][9] == "0") and (WF_List[71][9] > "0"):
        WMs = "現在、小樽で強風が吹いています。帰宅の際は強風に注意してください。\n"
    elif (WF_List[53][9] > "0") and (WF_List[71][9] > "0"):
        WMs = "現在、銭函周辺地域で強風が吹いています。帰宅の際は強風に注意してください。\n"
    elif (WF_List[61][9] == "0") and (WF_List[88][9] == "0"):
        WMs = "現在は特に強風は確認されていません。\n"
 

    if Ws == WMs:
        x = Pre + Ws + forecast
    elif (
        Ws == WMs
        and Pre == "現在、手稲で雨が降っています。帰宅の際は足元に注意してください。\n"
        or Pre == "現在、小樽で雨が降っています。帰宅の際は足元に注意してください。\n"
        or Pre
        == "現在、銭函周辺地域で雨が降っています。帰宅の際は足元に注意してください。\n"
    ):
        x = Pre + Ws
    else:
        x = Pre + Ws + WMs + forecast
            """

    return Pre + "\n" + Ws

    # Precipitation.csv


#  ######    ####    ##   ##  #######             ####   ##   ##  #######    ####   ###  ## #
#  # ## #     ##     ### ###   ##   #            ##  ##  ##   ##   ##   #   ##  ##   ##  ## #
#    ##       ##     #######   ## #             ##       ##   ##   ## #    ##        ## ## #
#    ##       ##     #######   ####             ##       #######   ####    ##        #### #
#    ##       ##     ## # ##   ## #             ##       ##   ##   ## #    ##        ## ## #
#    ##       ##     ##   ##   ##   #            ##  ##  ##   ##   ##   #   ##  ##   ##  ## #
#   ####     ####    ##   ##  #######             ####   ##   ##  #######    ####   ###  ## #


# 返却値0で日中、返却値1で夜間(朝側か夕側かは問わない)
def Time_Check(data, today):
    str_time = "00:00"
    time = datetime.strptime(str_time, "%H:%M")  # datetimeオブジェクトに変換

    # 一定間隔で時刻を増やし、0時から6時までのチェックをする(return 1)
    for i in range(7):
        if data[0][0] == str(today) + "T" + time.strftime("%H:%M"):
            return 1
        time += timedelta(hours=1)  # 増加量は1時間とする

    str_time = "20:00"
    time = datetime.strptime(str_time, "%H:%M")  # datetimeオブジェクトに変換

    # 一定間隔で時刻を増やし、0時から6時までのチェックをする(return 2)
    for i in range(4):
        if data[0][0] == str(today) + "T" + time.strftime("%H:%M"):
            return 1
        time += timedelta(hours=1)  # 増加量は1時間とする

    return 0


#  ##   ##  #######    ##     ######   ##   ##  #######  ######            #######   #####   ######   #######    ####     ##      #####   ###### #
#  ##   ##   ##   #   ####    # ## #   ##   ##   ##   #   ##  ##            ##   #  ##   ##   ##  ##   ##   #   ##  ##   ####    ##   ##  # ## # #
#  ##   ##   ## #    ##  ##     ##     ##   ##   ## #     ##  ##            ## #    ##   ##   ##  ##   ## #    ##       ##  ##   #          ## #
#  ## # ##   ####    ##  ##     ##     #######   ####     #####             ####    ##   ##   #####    ####    ##       ##  ##    #####     ## #
#  #######   ## #    ######     ##     ##   ##   ## #     ## ##             ## #    ##   ##   ## ##    ## #    ##       ######        ##    ## #
#  ### ###   ##   #  ##  ##     ##     ##   ##   ##   #   ##  ##            ##      ##   ##   ##  ##   ##   #   ##  ##  ##  ##   ##   ##    ## #
#  ##   ##  #######  ##  ##    ####    ##   ##  #######  #### ##           ####      #####   #### ##  #######    ####   ##  ##    #####    #### #
#


# Weather_Forecast付属関数
def Rain_time(rp, sd):
    Rain_time_data = []  # 降水確率順にソートされた配列
    data = (
        []
    )  # 単純な降水確率配列(find_peaks用なので、index:0には確定で0が入っている点に注意)
    peaks_plus_time = []
    peaks_plus_value = []
    peak_sort_list = []
    check1 = 0

    # ハナから追い回して最終値がTOPかBTMかはっきりさせる
    for i in range(24):
        if 0 != rp[0] - rp[i]:
            if 0 > rp[0] - rp[i]:
                data.append(101)  # ボトム
                check1 = 0
                break
            if 0 < rp[0] - rp[i]:
                data.append(-1)  # トップ
                check1 = 1
                break

    for i in range(24):
        data.append(rp[i])

    # ケツから追い回して最終値がTOPかBTMかはっきりさせる
    for i in range(24):
        if 0 != data[24] - data[24 - i]:
            if 0 > data[24] - data[24 - i]:
                data.append(101)  # ボトム
                print(data)
                break
            if 0 < data[24] - data[24 - i]:
                data.append(-1)  # トップ
                print(data)
                break

    # ピークのインデックスを取得(0時のインデックスが1のクソ配列である点に注意)
    peaks_plus, properties = find_peaks(data)
    peaks_plus = [i for i in peaks_plus]

    # 逆ピークのインデックスを取得(0時のインデックスが1のクソ配列である点に注意)
    peaks_minus, properties = find_peaks(list(map(lambda x: x * -1, data)))
    peaks_minus = [i for i in peaks_minus]

    # 時間だけを取り出す
    for i in range(24):
        Rain_time_data.append(sd[i][0][11:13])

    for i in range(len(peaks_plus)):
        peaks_plus_time.append(peaks_plus[i] - 1)

    for i in range(len(peaks_plus)):
        peaks_plus_value.append(data[peaks_plus[i]])

    peaks_plus_dict = dict(zip(peaks_plus_time, peaks_plus_value))

    # ピークの個数が3つ以上あれば組み合わせを捜索する
    if len(peaks_plus) > 2:
        plus_combination = list(itertools.combinations(peaks_plus, 2))

        # ピークを降水確率が高い順にソート
        for i in range(len(plus_combination)):
            if (
                data[plus_combination[i][0] + 1] < data[plus_combination[i][1] + 1]
            ):  # 前述のとおり0時のindexが1のゴミ配列なので1を足す
                peak_sort_list.append(data[plus_combination[i][1]])
            elif data[plus_combination[i][0] + 1] > data[plus_combination[i][1] + 1]:
                peak_sort_list.append(data[plus_combination[i][0]])
            else:
                peak_sort_list.append(-1)  # 同値の場合例外措置として-1

    # 最大値が含まれる山を捜索する
    rp_index = rp.index(max(rp))

    # ピークの降水確率をXに格納する
    X = []
    X = [data[i] for i in peaks_plus]

    Begin_and_End = []

    # 山の始まりの部分と終わりの部分を代入
    Begin_and_End.append(peaks_minus[X.index(max(X))])
    Begin_and_End.append(peaks_minus[(X.index(max(X))) - 1])

    peaks_max = rp.index(max(rp))

    Wf_prot(rp)

    if check1 == 1:
        return (
            str(peaks_minus[0] - 1)
            + "時から"
            + str(peaks_minus[1] - 1)
            + "時の間に雨が降るでしょう。\n最大降水確率は"
            + str(peaks_plus[1] - 1)
            + "時の"
            + str(data[peaks_plus[1]])
            + "%です。"
        )
    elif check1 == 0:
        return (
            str(peaks_minus[0])
            + "時から"
            + str(peaks_minus[1] - 1)
            + "時の間に雨が降るでしょう。\n最大降水確率は"
            + str(peaks_max)
            + "時の"
            + str(data[peaks_max + 1])
            + "%です。"
        )

    # 山がいくつあるかを確認する(山の端にあたる最小値の部分が一致するなら、その最大値は同じ山にある)


# 天気予報用関数
def Weather_Forecast():
    # 今日と三日後の日付を取得
    today = date.today()
    day_end = timedelta(days=3)

    # 3日後までの降水確率データを取得するためのURL
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=43.1333&longitude=141.1667&hourly=precipitation_probability&windspeed_unit=ms&timezone=Asia%2FTokyo&start_date="
        + str(today)
        + "&end_date="
        + str(today + day_end)
    )

    z = GF.json_open("prediction_probability.json")

    composition = {}

    i = 0
    for precipitation_probability in z["hourly"]["precipitation_probability"]:
        Z = z["hourly"]["time"][i]
        composition[Z] = precipitation_probability
        i += 1
        if i >= 24:
            break

    sorted_data = GF.dict_sort(composition)

    # 最も降水確率が高い部分で降水確率が0%ではないかを確認(一日中晴天かを精査)
    if sorted_data[0][1] > 0:
        # 降水確率が高い時刻が学校に関係ない時間帯でないかを確認(0:00~6:00、20:00~23:00が該当)
        if Time_Check(sorted_data, today) == 0:  # 日中の降水量が最大である場合の処理
            return (
                "本日は" + Rain_time(list(dict.values(composition)), sorted_data)
            ), 1
        elif Time_Check(sorted_data, today) == 1:  # 夜間の降水量が最大である場合の処理
            for i in range(24):
                if (
                    sorted_data[i][1] != 0
                ):  # データのn個目の降水確率が0%ではないかを確認
                    if Time_Check(sorted_data[i:], today) == 0:  # 昼間の時の処理
                        return_data = (
                            "本日は"
                            + str(sorted_data[0][0][11:16])
                            + "に"
                            + str(sorted_data[0][1])
                            + "%の確率で雨が降るでしょう。\nまた、日中では"
                            + str(sorted_data[i][0][11:16])
                            + "に"
                            + str(sorted_data[i][1])
                            + "%の確率で雨が降るでしょう。"
                        ), 1
                        Wf_prot(list(dict.values(composition)))
                        break
                    else:
                        pass
                else:  # n個目の降水確率が0%であった場合
                    return_data = (
                        "本日は"
                        + str(sorted_data[0][0][11:16])
                        + "に"
                        + str(sorted_data[0][1])
                        + "%の確率で雨が降るでしょう。\nまた、日中は雨の心配はせずに済みそうです。"
                    ), 0
                    break
    else:  # 一日中雨の心配がない場合の処理
        Wf_prot(list(dict.values(composition)))
        return_data = "本日は雨のない一日になりそうです", 0

    return return_data


# "hourly"{"time":,"precipitation_probability":}


# 3列目に地域名(カナ読みつき)、6~9列目に月:日:時:分、10行目に降水量が記載されている
# 風速と降水量はデータの位置が異なっている(降水量のみ観測している場所があるため)。
# 降水に関しての連絡は62の「手稲山観測所」と89の「小樽観測所」の二つを直接の降水予測に使用する
# 58～63、65、67(新篠津から千歳まで)、80(岩見沢)、88と89(余市と小樽)を直接の天気予報に使用する。
# 86と87(美国と神恵内)は雨予報として使用する（風向き的にここで降るなら銭函でも降るため）

# 降水「予測用」のURL。URLの後半に入っている2023-08-21の数字を今日の日付にすることで、その日から7日間の気象予測データを手に入れられるらしい。なおJSON形式。えっまたGFに新関数を！？
# https://api.open-meteo.com/v1/forecast?latitude=43.1333&longitude=141.1667&hourly=precipitation_probability,rain,windspeed_10m&windspeed_unit=ms&start_date=2023-08-21&end_date=2023-08-21
