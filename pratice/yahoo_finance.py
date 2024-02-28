import os
import requests
from datetime import datetime
from dotenv import load_dotenv


def get_raw_data_from_yahoo_finance(symbols: str) -> dict:
    """
    Args:
        symbols(str): split with comma, ex: "AAPL,MSFT"
    """
    url = "https://yfapi.net/v8/finance/spark"
    querystring = {"symbols": symbols, "interval": "1d", "range": "1mo"}
    headers = {"x-api-key": os.getenv("API_KEY")}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def convert_timestamp_to_datetime(timestamps: list[int]) -> list[str]:
    for index, timestamp in enumerate(timestamps):
        timestamps[index] = datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d")
    return timestamps


def merge_two_list_to_dict(fir_list: list[str], sec_list: list[float]) -> dict:
    new_dict = dict(zip(fir_list, sec_list))
    return new_dict


def get_stock_history(symbols: str) -> dict:
    """
    Args:
        symbols(str): split with comma, ex: "AAPL,MSFT"
    """
    ret = {}
    results = get_raw_data_from_yahoo_finance(symbols)

    for symbol in symbols.split(","):
        timestamps = results[symbol]["timestamp"]
        timestamps = convert_timestamp_to_datetime(timestamps)
        close_piece = results[symbol]["close"]
        symbol_info_mapping = merge_two_list_to_dict(timestamps, close_piece)
        ret[symbol] = symbol_info_mapping

    return ret


if __name__ == "__main__":
    load_dotenv()
    ret = get_stock_history("AAPL,MSFT")
    print(ret)
