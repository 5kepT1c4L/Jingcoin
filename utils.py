import json


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Coins"] = 0
        users[str(user.id)]["Jingcoins"] = 0

    with open("jingcoin.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("jingcoin.json", "r") as f:
        users = json.load(f)
    return users
