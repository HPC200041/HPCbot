import os
import difflib
import global_value as g

def login():
    i = 0

    print(os.getcwd())

    # ファイルへのパスを登録
    dir_path = r"E:"

    file_name = "pass_data.txt"
    file_path = os.path.join(dir_path, file_name)

    # file = open(".discord_bot/pass_data.txt")

    file = open(file_path)
    diff = difflib.Differ()

    output_diff = diff.compare(file.readlines(), g.val)

    for data in output_diff:
        if data[0:1] not in ["+", "-", "?"]:
            i += 1
            return data

    if i < 1:
        return 0

    file.close()