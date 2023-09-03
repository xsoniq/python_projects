import requests

import config
from config import TG_TOKEN

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from background import keep_alive


bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher(bot)


def get_info():
    response = requests.get(url="https://yobit.net/api/3/info")

    with open("info.txt", "w") as file:
        file.write(response.text)

    return response.text


def get_ticker(coin1="btc", coin2="usd", coin3="eth", coin4="usdttrc20"):
    # response = requests.get(url="https://yobit.net/api/3/ticker/eth_btc-btc_usdttrc20")
    response = requests.get(url=f"https://yobit.net/api/3/ticker/{coin1}_{coin2}-{coin3}_{coin2}?ignore_invalid=1")

    with open("ticker.txt", "w") as file:
        file.write(response.text)

    return response.text


# получаем цену всех выставленных на закупку монет
def get_depth(coin1="btc", coin2="usd", coin3="eth", limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/depth/{coin1}_{coin2}-{coin3}_{coin2}?limit={limit}, "
                                f"ignore_invalid=1")

    with open("depth.txt", "w") as file:
        file.write(response.text)

    total_bids_amount = 0
    bids = response.json()[f"{coin1}_{coin2}-{coin3}_{coin2}"]["bids"]
    for item in bids:
        price = item[0]
        coin_amount = item[1]

        total_bids_amount += price * coin_amount

    return f"Total bids: {total_bids_amount} $"


# получаем цену всех проданных монет
def get_trades(coin1="btc", coin2="usd", coin3="eth", limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/trades/{coin1}_{coin2}-{coin3}_{coin2}?limit={limit}, "
                                f"ignore_invalid=1")

    with open("trades.txt", "w") as file:
        file.write(response.text)

    total_trade_ask_btc = 0
    total_trade_bid_btc = 0
    total_trade_ask_eth = 0
    total_trade_bid_eth = 0

    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == "ask":
            total_trade_ask_btc += item["price"] * item["amount"]
        else:
            total_trade_bid_btc += item["price"] * item["amount"]

    for item in response.json()[f"{coin3}_{coin2}"]:
        if item["type"] == "ask":
            total_trade_ask_eth += item["price"] * item["amount"]
        else:
            total_trade_bid_eth += item["price"] * item["amount"]

    info = f"[-]  {coin1} SELL {round(total_trade_ask_btc, 2)} $\n[+] {coin1} BUY: {round(total_trade_bid_btc, 2)} $\n\n" \
           f"[-]  {coin3} SELL {round(total_trade_ask_eth, 2)} $\n[+] {coin3} BUY: {round(total_trade_bid_eth, 2)} $"

    return info


@dp.message_handler(commands=['start'])
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, f"{get_trades()}")

# def main():
    # get_info()
    # print(get_ticker())
    # print(get_ticker())
    # print(get_depth(coin1="doge", limit=2000))
    # print(get_trades())


if __name__ == '__main__':
    executor.start_polling(dp)
