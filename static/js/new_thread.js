// constants
const titleField = $("#title-field");
const contentField = $("#content-field");

async function createThread(route, title){
    let res = await fetch(route, {
        method: "POST",
        body: JSON.stringify({"title": title}),
        headers: {
            "Content-Type": "application/json"
        }
    })
    let json = await res.json()
    if (res.status != 201){
        return Promise.reject(json["error"])
    }
    return json["new_thread_id"]
}

async function createPost(route, content){
    let res = await fetch(route, {
        method: "POST",
        body: JSON.stringify({"content": content}),
        headers: {
            "Content-Type": "application/json"
        }
    })
    let json = await res.json()
    if (res.status != 201){
        return Promise.reject(json["error"])
    }
    return json["new_thread_id"]
}

async function sendPostRequests(thread_route, post_route, thread_title, post_content){
    let tid = await createThread(thread_route, thread_title).catch((err) => {
        return Promise.reject()
    })
    await createPost(post_route.replace("<tid>", tid), post_content)
}

$("#new-thread-btn").click(() => {
    let title = titleField.val();
    let content = contentField.val();
    if (!(title.length > 0 && content.length > 0)) {
        alert("Title and content cannot be empty!");
        return
    }
    // POST thread and post to backend
    let params = new URLSearchParams(window.location.search)
    sendPostRequests(params.get("thread_route"), params.get("post_route"), title, content)
    .then(() => {
        window.location.href = params.get("redir_url")
    }).catch((err) => {
        alert("Failed to create thread")
    })
})