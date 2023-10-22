import requests


def make_request(url):
    response = requests.get(url)
    print(url, response)
    return response.json()


posts = make_request("https://jsonplaceholder.typicode.com/posts")

for post in posts[:10]:
    post_id = post.get('id')
    comments_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    make_request(comments_url)
