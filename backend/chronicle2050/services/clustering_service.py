import requests

def init_clustering(parsed_entity):
    print("start clustering")
    url = "https://d9c8-34-124-155-12.ngrok.io/"
    response = requests.get(url + "cluster/")
    if response.status_code == 200:
        print("clustering successful")
    else:
        print("clustering UNsuccessful")
