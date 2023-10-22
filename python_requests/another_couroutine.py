import requests


def fun():
    url = "https://jsonplaceholder.typicode.com/posts"
    print("Make a request to url")
    res = yield url
    print("Got result ", res)
    yield


g = fun()
url = next(g)
response = requests.get(url).json()
g.send(response)
