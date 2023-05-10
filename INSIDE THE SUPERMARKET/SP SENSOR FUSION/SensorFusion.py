import cv2
from pyzbar import pyzbar
import requests
import csv
import os
import json


CHANNEL_ID = "2102276"
FIELD_NUM_2 = "2"
FIELD_NUM_1 = "1"
READ_API_KEY = "MMFQCATD3SY8QAB1"
cap = cv2.VideoCapture(0)

currentuser = ""
latestbarcode = 0
weightincart_NODEMCU = 0
weightincart_Local = 0
weight_of_last_item = 0
total = 0
items = []


def get_data():
    try:
        response = requests.get(
            f"https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD_NUM_2}.json?api_key={READ_API_KEY}&results=1"
        )
        if response.status_code == 200:
            data = response.json()["feeds"][0]["field{}".format(FIELD_NUM_2)]
            global weightincart_NODEMCU
            weightincart_NODEMCU = float(data)
            print(f"Latest value in Field {FIELD_NUM_2}: {data}")
    except Exception as e:
        print(f"Exception in get_data: {e}")


def read_barcode():
    try:
        ret, frame = cap.read()

        # convert the frame to grayscale for barcode detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect barcodes in the grayscale frame
        barcodes = pyzbar.decode(gray)

        # loop through detected barcodes and print data
        for barcode in barcodes:
            # extract the barcode data as a byte string
            barcode_data = barcode.data.decode("utf-8")
            print("Found barcode:", barcode_data)
            global latestbarcode
            latestbarcode = barcode_data

            # draw a bounding box around the barcode in the frame
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the frame with barcode detection overlay
        cv2.imshow("Barcode Reader", frame)

        # exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            quit
    except Exception as e:
        print(f"Exception in read_barcode: {e}")


def get_item_weight(barcode):
    try:
        with open(
            "./INSIDE THE SUPERMARKET/SP_ITEMS_DATABASE_IN_THE_STORE/database.csv", "r"
        ) as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if barcode == row[1]:
                    return row[2]
    except Exception as e:
        print(f"Exception in get_item_weight: {e}")


def get_item_price(barcode):
    try:
        with open(
            "./INSIDE THE SUPERMARKET/SP_ITEMS_DATABASE_IN_THE_STORE/database.csv", "r"
        ) as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if barcode == row[1]:
                    return row[3]
    except Exception as e:
        print(f"Exception in get_item_price: {e}")


def get_item_Name(barcode):
    try:
        with open(
            "./INSIDE THE SUPERMARKET/SP_ITEMS_DATABASE_IN_THE_STORE/database.csv", "r"
        ) as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if barcode == row[1]:
                    return row[0]
    except Exception as e:
        print("Error while fetching item name: ", e)


def add_items_to_shopping_cart():
    try:
        file_path = "./INSIDE THE SUPERMARKET/SP SHOPPING CART/"
        for file in os.listdir(file_path):
            if file.endswith(".txt"):
                with open(os.path.join(file_path, file), "w") as f:
                    for item in items:
                        f.write(get_item_Name(item))
                        f.write(",")
                        f.write(get_item_price(item) + "\n")
    except Exception as e:
        print("Error while adding items to shopping cart: ", e)


while True:
    url = "https://api.thingspeak.com/channels/CHANNEL_ID/feeds.json?api_key=API_KEY&results=1"
    response = requests.get(url)
    data = json.loads(response.text)

    if data["feeds"][0]["field3"] == "1":
        read_barcode()
        if latestbarcode != 0:
            weight_of_last_item = float(get_item_weight(latestbarcode))
            if (weight_of_last_item + weightincart_Local) >= (
                0.95 * weightincart_NODEMCU
            ) and (weight_of_last_item + weightincart_Local) <= (
                1.05 * weightincart_NODEMCU
            ):
                items.append(latestbarcode)
                add_items_to_shopping_cart()
                weightincart_Local += weight_of_last_item
                weight_of_last_item = 0
                latestbarcode = 0

cap.release()
cv2.destroyAllWindows()
