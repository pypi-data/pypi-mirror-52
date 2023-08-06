import requests


def read_data(url):
    r = requests.get(url)
    return r.text


