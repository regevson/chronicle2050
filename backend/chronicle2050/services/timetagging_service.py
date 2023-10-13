import requests

def init_tagging(parsed_entity):
    print("start tagging")
    url = "https://91e9-34-125-70-82.ngrok.io/"
    response = requests.get(url + "tag/")
    if response.status_code == 200:
        print("tagging successful")
    else:
        print("tagging UNsuccessful")
