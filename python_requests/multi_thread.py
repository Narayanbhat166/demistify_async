import requests

from threading import Thread


def make_request(url):
    response = requests.get(url)
    print(url, response)
    return response.json()


posts = make_request("https://jsonplaceholder.typicode.com/posts")

threads = []

for post in posts[:10]:
    post_id = post.get('id')
    comments_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"

    thread = Thread(target=make_request, args=(comments_url,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Done")
