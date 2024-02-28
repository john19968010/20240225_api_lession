import requests
from datetime import datetime
from dotenv import load_dotenv
import os

"""
透過"https://yfapi.net/v8/finance/spark"這隻API
取得AAPL, TSLA為期一個月且間格為一天的股價, 並整理成下方資料格式
{
    "AAPL": {
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5"
    },
    "TSLA": {
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5"
    }
}
"""

"""
Steps:
1. 將timestamp轉換成datetime(2021/12/21)
2. 將轉換過的timestamp_list 與close的price list合成上放的dict
3. 將股票代號設為key, value為整理過後的dict並return.
"""


if __name__ == "__main__":
    pass
