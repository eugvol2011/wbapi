from flask import Flask
from requests import request, Response
from typing import Any
import os

app = Flask(__name__)


@app.route("/get-sku-info/<sku>")
def get_sku_info(sku):
    req: Response = request(
        method="GET",
        url=f"https://card.wb.ru/cards/detail?nm={sku}"
    )

    response: dict[str, Any] = req.json()

    short_id: int = int(sku) // 100000

    if 0 <= short_id <= 143:
        basket: str = '01'
    elif 144 <= short_id <= 287:
        basket: str = '02'
    elif 288 <= short_id <= 431:
        basket: str = '03'
    elif 432 <= short_id <= 719:
        basket: str = '04'
    elif 720 <= short_id <= 1007:
        basket: str = '05'
    elif 1008 <= short_id <= 1061:
        basket: str = '06'
    elif 1062 <= short_id <= 1115:
        basket: str = '07'
    elif 1116 <= short_id <= 1169:
        basket: str = '08'
    elif 1170 <= short_id <= 1313:
        basket: str = '09'
    elif 1314 <= short_id <= 1601:
        basket: str = '10'
    elif 1602 <= short_id <= 1655:
        basket: str = '11'
    elif 1656 <= short_id <= 1919:
        basket: str = '12'
    elif 1920 <= short_id <= 2045:
        basket: str = '13'
    elif 2046 <= short_id <= 2189:
        basket: str = '14'
    elif 2190 <= short_id <= 2405:
        basket: str = '15'
    else:
        basket: str = '16'

    pics: list[str] = []
    for i in range(1, response["data"]["products"][0]["pics"] + 1):
        pics.append(f"https://basket-{basket}.wb.ru/vol{short_id}/part{int(sku) // 1000}/{sku}/images/big/{i}.jpg;")

    response["data"]["products"][0]["pictures"] = pics

    req_feedbacks: Response = request(
        method="GET",
        url=f"https://feedbacks2.wb.ru/feedbacks/v1/{response["data"]["products"][0]["root"]}"
    )

    feedbacks_response: dict[str, Any] = req_feedbacks.json()

    print(len(feedbacks_response["feedbacks"]))
    feedback_texts: list[str] = []
    for feedback in feedbacks_response["feedbacks"]:
        feedback_texts.append(feedback["text"])
    print(len(feedback_texts))

    response["valuationDistribution"] = feedbacks_response["valuationDistribution"]
    response["valuationDistributionPercent"] = feedbacks_response["valuationDistributionPercent"]
    # add reviews
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
