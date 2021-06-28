import requests
import json
import csv

# An example using DigiCert's API to parse order details for specific details. 
# In this case the goal was to get the api_key name and type per active order ("not renewed" and has an "issued" order status). 
# Usage: Just enter your DigiCert api key below. A report called "order.csv" will be exported locally. This may take a few minutes to generate depending on account size.

api_key = ""  # DigiCert API Key

headers = {
    'X-DC-DEVKEY': f'{api_key}',
    'Content-Type': "application/json"
}


def all_order_details():
    with open('orders.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "api_key_name", "key_type"])
        all_orders_url = f'https://www.digicert.com/services/v2/order/certificate?filters[status]=issued&content_type=json'
        res = requests.request("GET", all_orders_url, headers=headers)
        data = res.text
        all_order_data = json.loads(data)
        print(json_data)

        for orders in all_order_data["orders"]:
            order_id = orders["id"]
            order_url = f'https://www.digicert.com/services/v2/order/certificate/{order_id}'
            res = requests.request("GET", order_url, headers=headers)
            data_2 = res.text
            order_data = json.loads(data_2)
            
            if not order_data["is_renewed"] and order_data["status"] == "issued":
                if "api_key" in order_data:
                    print(order_id, order_data["api_key"])
                    writer.writerow([order_id, order_data["api_key"]["name"], order_data["api_key"]["key_type"]])
                else:
                    print(order_id, "none")
                    writer.writerow([order_id, "none"])


all_order_details()
