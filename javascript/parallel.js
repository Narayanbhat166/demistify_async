async function make_request(url) {
    let response = await fetch(url)
        .then((res) => res.json());

    console.log(url, "Done")
    return response
}

async function get_data() {
    let posts = await make_request("https://jsonplaceholder.typicode.com/posts");

    let all_futures = posts.slice(0, 10).map(async (post) => {
        let post_id = post.id;
        let comments_url = `https://jsonplaceholder.typicode.com/posts/${post_id}/comments`;
        return make_request(comments_url)
    });

    await Promise.all(all_futures);
}

get_data().then(() => console.log("Main Done"));
