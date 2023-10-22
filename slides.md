---
theme: seriph
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: true
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
drawings:
  persist: false
transition: slide-left
mdc: true
preload: false

fonts:
  # basically the text
  sans: "Robot"
  # use with `font-serif` css class from windicss
  serif: "Robot Slab"
  # for code blocks, inline code, etc.
  mono: "Iosevka Term"
---

# Demistify asynchronous programming

<uim-rocket/> A guide to understanding asynchronous programming. <uim-rocket/>

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---

## Takeaways

<hr>

<v-clicks>

- Gain deeper understanding of how asynchronous programming works and is used in real world to solve various problems.
- Be a better developer. Inspire others.

</v-clicks>

---

# Table of contents

<Toc maxDepth="1"></Toc>

---

# Why do we need asynchronous programming?

Let's try to understand the problem.

<hr>

## Problem statement

Get data from the website https://jsonplaceholder.typicode.com.

- All the posts.
- Comments associated with each post.

<hr>
<br>

<v-clicks>

1. ### Checkpoint - _Starters_

Get the posts made by the all the users. Use the api endpoint https://jsonplaceholder.typicode.com/posts to get the details of posts

2. ### Checkpoint - _Completeness_

<!-- - For each post, get the comments. You can look at the api reference here https://jsonplaceholder.typicode.com -->

3. ### Checkpoint - _Performance_

<!-- - It takes a lot of time to get the data, optimize it. -->

4. ### Checkpoint - _Efficiency_

</v-clicks>
<!-- - The resources are limited, make efficient use of it. -->

---

## Making a single request

To get started, let's get all the posts.

Python

```py {1|2|4-5|7}
import requests
from pprint import pprint

def make_request(url):
  return requests.get(url).json()

pprint(make_request("https://jsonplaceholder.typicode.com/posts"))
```

Output
<v-click>

```json
[{'body': 'quia et suscipit\n'
          'suscipit recusandae consequuntur expedita et cum\n'
          'reprehenderit molestiae ut ut quas totam\n'
          'nostrum rerum est autem sunt rem eveniet architecto',
  'id': 1,
  'title': 'sunt aut facere repellat provident occaecati excepturi optio '
           'reprehenderit',
  'userId': 1}
]
```

</v-click>

---

## Let's complete the solution

Get the comments associated with every post. Use the endpoint https://jsonplaceholder.typicode.com/posts/{post_id}/comments.

Steps

- Get all the posts
- Get the comments associated with each post.

---

## Completeness

<br>

```py {4-7|6|10|12|13|14|15}
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
```

---

Output

```txt {1|1-2|1-3|1-4|1-5|1-6|1-7|1-8|1-9|1-10|1-11}
https://jsonplaceholder.typicode.com/posts <Response [200]>
https://jsonplaceholder.typicode.com/posts/1/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/2/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/3/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/4/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/5/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/6/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/7/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/8/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/9/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/10/comments <Response [200]>
```

<v-click>

We can do better.

</v-click>

---

## Let's improve our code

```py {2-5}
for post in posts[:10]:
  post_id = post.get('id')
  comments_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
  make_request(comments_url)
```

<v-click>

How can we optimize the code?

</v-click>

<br>

<v-click>

Introduce Parallelism

</v-click>

---

# The Fundamentals

| Process                                                     | Thread                                                                   |
| ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| An instance of a program in execution                       | Segment of a process, every process will have atleast one thread         |
| Has a separate memory layout, isolated with other processes | Share the same heap memory as that of a process, but has separate stacks |
| Has creating and switching overhead, slightly heavier       | Quick and easy to crete and context switch                               |
| Difficult to communicate between processes                  | Inter thread communication is easier                                     |
| Difficult to manage                                         | Easier to manage                                                         |

<hr>

<v-click>

So is it threads, or processes that we need?

</v-click>

---

## Checkpoint - Let's make it performant

We can use threads to get the data in parallel since there is no dependency between the data

```py {3|14|20|6-9|20|21|22|24-25|27} {maxHeight:'400px'}
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
```

---

## Output

```txt {1|1-11|1-12|}
https://jsonplaceholder.typicode.com/posts <Response [200]>
https://jsonplaceholder.typicode.com/posts/9/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/6/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/5/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/10/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/2/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/1/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/4/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/8/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/3/comments <Response [200]>
https://jsonplaceholder.typicode.com/posts/7/comments <Response [200]>
Done
```

<br>

<v-click>

It's time to make it efficient now

</v-click>

---

## Types of processes

| CPU bound                                                                               | IO bound                                                                                            |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Program spends most of its time doing CPU operations                                    | Program spends most of its time talking to a slow device, like a network connection or a hard drive |
| CPU is busy all the times                                                               | CPU is idle most of the times                                                                       |
| Speeding it up involves finding ways to do more computations in the same amount of time | Speeding it up involves overlapping the times spent waiting for these devices.                      |

<br>
<br>

<v-click>

So where does our program stand?

</v-click>

<v-click>

IO Bound

</v-click>

---

# Concurrency

A deeper understanding.

---

## Green threads

- In computer programming, a green thread (virtual thread) is a thread that is scheduled by a runtime library or virtual machine (VM) instead of natively by the underlying operating system (OS).
- Green threads emulate multithreaded environments without relying on any native OS abilities

The basic concept is, in IO bound processes since there is no much computation that is required, We need not create OS threads all the time.

A language runtime can be considered as a supervisor for handling concurrency.

---

## Revisiting threads

| OS threads                 | User threads / Green threads            |
| -------------------------- | --------------------------------------- |
| Created at the OS level    | Create at user / languate runtime level |
| Requires a system call     | Does not require a system call          |
| Is run on a dedicated core | Are run on the same thread              |
| Comparatively heavier      | Lighther to create and context switch   |
| Parallel execution         | Concurrent Execution                    |
| **Preemptive scheduling**  | **Cooperative scheduling**              |

Python uses green threads.

<v-click>

Threads are hard to work with

</v-click>

---

## Coroutines

Coroutines are computer program components that allow execution to be suspended and resumed.
These are special functions that can remember the state in between function calls.

Functionality provided by the programming language.

<v-click>

This is exactly what we need

</v-click>

---

## A simple Couroutine

This program simulates making an api call

```py {1|12|5|6|7|13|14|15|7|8|9}
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
```

<v-click>

```txt
Make a request to url
Got result ...
```

</v-click>

---

# Async - let's get started

async means that we don't block the thread waiting for IO to complete.

<!--
You can have `style` tag in markdown to override the style for the current page.
Learn more: https://sli.dev/guide/syntax#embedded-styles
-->

<v-clicks>

- async
- coroutine
- promise
- await
- executor
- event loop

</v-clicks>

<style>
h1 {
background-color: #2B90B6;
background-image: linear-gradient(45deg, #4EC5D4 10%, #146b8c 20%);
background-size: 100%;
-webkit-background-clip: text;
-moz-background-clip: text;
-webkit-text-fill-color: transparent;
-moz-text-fill-color: transparent;
}
</style>

---

## A simple async function in python

```python

async def fun():
    print("Hello, World!")


fun()

```

<v-click>

But this does not work

</v-click>

<v-click>

```txt
RuntimeWarning: coroutine 'fun' was never awaited
```

</v-click>

---

# Let's await

```py
async def fun():
    print("Hello, World!")

await fun()
```

<v-click>

Again, does not work

</v-click>

<v-click>

```txt
SyntaxError: 'await' outside function
```

</v-click>

<br>

<v-clicks>

- So python does not know how to run async functions.
- Let's get someone who knows

</v-clicks>

---

## asyncio to the rescue

```py
import asyncio


async def fun():
    print("Hello, World!")

asyncio.run(fun())
```

<v-click>

```txt
Hello, World!
```

</v-click>

---

## The event loop

The event loop is the core of every asyncio application. Event loops run asynchronous tasks and callbacks, perform network IO operations.

It is a loop that will make IO operations on behalf of you.

---

## Efficiency

```py {1|2|5|6|7|12|13|15|17|19-24|26|28} {maxHeight:'400px'}
import aiohttp
import asyncio


async def make_request(url, session):
    response = await session.get(url)
    data = await response.json()
    print(url, "Done")
    return data


async def main():
    async with aiohttp.ClientSession() as session:

        posts = await make_request("https://jsonplaceholder.typicode.com/posts", session)

        tasks = []

        for post in posts[:10]:
            post_id = post.get('id')
            comments_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"

            task = make_request(comments_url, session)
            tasks.append(task)

        await asyncio.gather(*tasks)

asyncio.run(main())
```

---

Output

```txt {1|1-11}
https://jsonplaceholder.typicode.com/posts Done
https://jsonplaceholder.typicode.com/posts/1/comments Done
https://jsonplaceholder.typicode.com/posts/2/comments Done
https://jsonplaceholder.typicode.com/posts/5/comments Done
https://jsonplaceholder.typicode.com/posts/9/comments Done
https://jsonplaceholder.typicode.com/posts/4/comments Done
https://jsonplaceholder.typicode.com/posts/8/comments Done
https://jsonplaceholder.typicode.com/posts/7/comments Done
https://jsonplaceholder.typicode.com/posts/3/comments Done
https://jsonplaceholder.typicode.com/posts/10/comments Done
https://jsonplaceholder.typicode.com/posts/6/comments Done

```

All the requests are run on a single thread, this can be checked by a very smart way

---

# Other programming languages

Javascript

```js
fetch("https://jsonplaceholder.typicode.com/posts")
  .then((res) => res.json())
  .then((res) => console.log(res));
```

Output
<v-click>

```json
[{'body': 'quia et suscipit\n'
          'suscipit recusandae consequuntur expedita et cum\n'
          'reprehenderit molestiae ut ut quas totam\n'
          'nostrum rerum est autem sunt rem eveniet architecto',
  'id': 1,
  'title': 'sunt aut facere repellat provident occaecati excepturi optio '
           'reprehenderit',
  'userId': 1}
]
```

</v-click>

---

The smart way

```js {2|4|5|8|9|11-15|17|20}
async function make_request(url) {
  let response = await fetch(url).then((res) => res.json());

  console.log(url, "Done");
  return response;
}

async function get_data() {
  let posts = await make_request("https://jsonplaceholder.typicode.com/posts");

  let all_futures = posts.slice(0, 10).map(async (post) => {
    let post_id = post.id;
    let comments_url = `https://jsonplaceholder.typicode.com/posts/${post_id}/comments`;
    return make_request(comments_url);
  });

  await Promise.all(all_futures);
}

get_data().then(() => console.log("Main Done"));
```

---

Output

```txt {1|1-11|1-12}
https://jsonplaceholder.typicode.com/posts Done
https://jsonplaceholder.typicode.com/posts/1/comments Done
https://jsonplaceholder.typicode.com/posts/3/comments Done
https://jsonplaceholder.typicode.com/posts/4/comments Done
https://jsonplaceholder.typicode.com/posts/5/comments Done
https://jsonplaceholder.typicode.com/posts/8/comments Done
https://jsonplaceholder.typicode.com/posts/7/comments Done
https://jsonplaceholder.typicode.com/posts/10/comments Done
https://jsonplaceholder.typicode.com/posts/9/comments Done
https://jsonplaceholder.typicode.com/posts/2/comments Done
https://jsonplaceholder.typicode.com/posts/6/comments Done
Main Done
```

---

# Use cases

<v-clicks>

- Build efficient and scalable web servers.
- Make multiple api calls to endpoints efficiently.
- Make concurrent db calls.

</v-clicks>

<v-click>

All of these are being done in hyperswitch to make it a very performant, efficient and highly scalable product.

</v-click>

---

# Bonus content

- https://hyperswitch.io/
- https://hyperswitch.io/hacktoberfest

# Connect with me

- https://www.linkedin.com/in/narayan-bhat166/
- https://github.com/Narayanbhat166
