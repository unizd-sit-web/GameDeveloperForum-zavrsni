import {API_BASE_URL, STATIC_BASE_URL, createCardConfirmMenu, createThreadCard} from "./util.js";

const threadContainer = $("#thread-container")
const staticThreadEndpointUrl = STATIC_BASE_URL + "/news/categories/news-category/threads"
const threadEndpointUrl = API_BASE_URL + "/news/categories/news-category/threads"
const noThreadsLabel = $("#no-threads-label")

$("#new-thread-btn").click(() => {
    let params = new URLSearchParams(window.location.search)
    params.set("redir_url", window.location.href)
    params.set("thread_route", "/api/news/categories/news-category/threads")
    params.set("post_route", "/api/news/categories/news-category/threads/<tid>/posts")
    window.location.href = "/news/categories/news-category/threads/new?" + params.toString()
})

async function loadThreads(){
    let threadsRaw = await fetch(threadEndpointUrl, {
        "method": "GET",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    })
    let json = await threadsRaw.json()
    let threads = json["threads"]
    if (threads.length > 0){
        noThreadsLabel.hide()
    } else {
        noThreadsLabel.show()
    }
    for (let thread of threads){
        let card = createThreadCard(thread["title"], staticThreadEndpointUrl + "/" + thread["thread_id"] + "/posts", true)
        let delBtn = $(card).find(".delete-button-div-thread")[0]
        $(delBtn).on("click", () => {
            createCardConfirmMenu(card, false, "Delete", "Cancel", () => {
                deleteThread(thread["thread_id"])
            }, () => {})
        })
        threadContainer.append(card)
    }
}

function deleteThread(tid){
    fetch(threadEndpointUrl + "/" + tid, {
        "method": "DELETE",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    })
    .then(() => {
        window.location.reload()
    }).catch((err) => {
        console.error(err)
        alert("Failed to delete thread")
    })
}

loadThreads().catch((err) => {
    console.error(err)
    alert("Failed to load threads")
})