import requests
import json
import csv
from tqdm import tqdm


api_key = ""  # DigiCert API Key

headers = {
    'X-DC-DEVKEY': f'{api_key}',
    'Content-Type': "application/json"
}


class CsvDictWriter:
    def __init__(self):
        self.dicts = []
        self.fields = set()

    def add_dict(self, obj: dict):
        self.dicts.append(obj)
        self.fields.update(obj.keys())

    def write(self, file_name: str):
        with open(file_name, 'w', newline="") as fp:
            dw = csv.DictWriter(fp, self.fields, restval='')
            dw.writeheader()
            for obj in self.dicts:
                dw.writerow(obj)


def all_order_details():
    counter = 1
    cdw = CsvDictWriter()
    all_orders_url = f'https://www.digicert.com/services/v2/order/certificate?filters[status]=issued&content_type=json'
    res = requests.request("GET", all_orders_url, headers=headers)
    data = res.text
    all_order_data = json.loads(data)

    with tqdm(total=len(all_order_data["orders"])) as pbar:
        for orders in all_order_data["orders"]:
            order_id = orders["id"]
            order_url = f'https://www.digicert.com/services/v2/order/certificate/{order_id}'
            res = requests.request("GET", order_url, headers=headers)
            data_2 = res.text
            order_data = json.loads(data_2)
            if not order_data["is_renewed"] and order_data["status"] == "issued":
                cdw.add_dict(order_data)
                pbar.update(1)
                pbar.set_description("Processing.. Orders Found %s" % counter)
                counter = counter + 1
            else:
                pbar.update(1)

        cdw.write('orders.csv')
        print("Complete! File saved as 'orders.csv'")


all_order_details()
