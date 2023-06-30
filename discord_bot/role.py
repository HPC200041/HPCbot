import discord

role_1 = 1122714200230330429 # 一年生のロールID


def role_add(Member_ID):
    # 用意したIDから Role オブジェクトを取得
    role = Member_ID.guild.get_role(role_1)

    # 入ってきた Member に役職を付与
    Member_ID.add_roles(role)

    return 0