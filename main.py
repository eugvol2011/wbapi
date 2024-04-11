from flask import Flask
from requests import request, Response
import os

app = Flask(__name__)


@app.route("/get-sku-info/<sku>")
def get_sku_info(sku):
    req: Response = request(
        method="GET",
        url=f"https://card.wb.ru/cards/detail?nm={sku}"
    )
    return req.json()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
