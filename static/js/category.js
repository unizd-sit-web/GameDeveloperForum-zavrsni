import {API_BASE_URL, createThreadCard, STATIC_BASE_URL} from "./util.js"

const threadContainer = $("#thread-container")
const noThreadsLabel = $("#no-threads-label")
const categoryEndpointUrl = removeCidFromUrl(API_BASE_URL + window.location.href.replace(/^.*\/\/[^\/]+/, '').replace("/threads", ""))
const threadEndpointUrl = API_BASE_URL + window.location.href.replace(/^.*\/\/[^\/]+/, '')
const staticThreadEndpointUrl = STATIC_BASE_URL + window.location.href.replace(/^.*\/\/[^\/]+/, '')
const categoryId = window.location.href.replace(/^.*\/\/[^\/]+/, '').replace("/threads", "").split("/").pop()

function removeCidFromUrl(url){
    let arr = url.split("/")
    arr.pop()
    return arr.join("/")
}

$("#new-thread-btn").click(() => {
    let params = new URLSearchParams(window.location.search)
    params.set("redir_url", window.location.href)
    params.set("post_route", threadEndpointUrl + "/<tid>/posts")
    params.set("thread_route", threadEndpointUrl)
    window.location.href = STATIC_BASE_URL +  window.location.href.replace(/^.*\/\/[^\/]+/, '') + "/new?" + params.toString()
})

async function loadTitle(){
    let titleRaw = await fetch(categoryEndpointUrl + "?cid=" + categoryId, {
        "method": "GET",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    })
    let json = await titleRaw.json()
    let title = json["categories"][0]["title"]
    $("#category-title").text(title)
}

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
    for (let thread of json["threads"]){
        let card = createThreadCard(thread["title"], staticThreadEndpointUrl + "/" + thread["thread_id"] + "/posts")
        threadContainer.append(card)
    }
}

loadTitle().catch((err) => {
    console.log(err)
    alert("Failed to load title")
})
loadThreads().catch((err) => {
    console.error(err)
    alert("Failed to load threads")
})