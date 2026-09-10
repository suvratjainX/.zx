import requests

def get(url):
    return requests.get(url).text

def download(url,file):
    data = requests.get(url)

    with open(file,"wb") as f:
        f.write(data.content)