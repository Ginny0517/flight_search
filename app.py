from flask import Flask, request, render_template, redirect, url_for
import requests
import datetime

ENDPOINT = "https://api.tequila.kiwi.com/v2"
CITY_FROM = "TPE"
APIKEY = "your_apikey"

app = Flask(__name__)

def search_flight(city_name):
        today = datetime.datetime.now().strftime("%d/%m/%Y")
        date_to = (datetime.datetime.now() + datetime.timedelta(days=6 * 30)).strftime("%d/%m/%Y")
        search_endpoint = f"{ENDPOINT}/search"
        header = {
            "apikey": APIKEY
        }

        query = {
            "fly_from": f"city:{CITY_FROM}",
            "fly_to": f"city:{city_name}",
            "date_from": today,
            "date_to": date_to,
            "nights_in_dst_from": 5,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "TWD"
        }

        response = requests.get(url=search_endpoint, headers=header, params=query)
        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 2
            response = requests.get(url=search_endpoint, headers=header, params=query)
            data = response.json()["data"][0]
            return data
        else:
            return data

@app.route("/", methods=["POST", "GET"])
def index():
    data = ""
    if request.method == "POST":
        cityCode = request.form.get("cityCode")
        if cityCode:
            try:
                data = search_flight(cityCode)
                return render_template("index.html", data=data)
            except KeyError:
                 data = "not found"
                 return render_template("index.html", data=data)
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
