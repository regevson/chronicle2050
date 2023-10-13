import requests

def init_classification(parsed_entity):
    print("start classification")
    url = "https://d9c8-34-124-155-12.ngrok.io/"
    response = requests.get(url + "classify/")
    if response.status_code == 200:
        print("classification successful")
    else:
        print("classification UNsuccessful")
