import {API_BASE_URL, createCardConfirmMenu, createEditCardDialog, createPostCard} from "./util.js"

const postContainer = $("#post-container")
const noPostsLabel = $("#no-posts-label")
// set the domain of the current url to API_BASE_URL
const threadEndpointUrl = removeTidFromUrl(API_BASE_URL + window.location.href.replace(/^.*\/\/[^\/]+/, '').replace("/posts", ""))
const postsEndpointUrl = API_BASE_URL + window.location.href.replace(/^.*\/\/[^\/]+/, '')
const threadId = window.location.href.replace(/^.*\/\/[^\/]+/, '').replace("/posts", "").split("/").pop()

function removeTidFromUrl(url){
    let arr = url.split("/")
    arr.pop()
    return arr.join("/")
}

function createPost(content){
    return fetch(postsEndpointUrl, {
        method: "POST",
        body: JSON.stringify({"content": content}),
        headers: {
            "Content-Type": "application/json"
        }
    })
}

$("#new-post-btn").click((e) => {
    e.preventDefault();
    let content = $("#content-field").val();
    $("#content-field").val("");
    if (content.length == 0) {
        alert("You cannot post an empty post!");
        return;
    }
    createPost(content).then((pid) => {
        window.location.reload();
    }).catch((err) => {
        console.log(err)
        alert("Failed to create post")
    })
})

async function loadTitle(){
    let titleRaw = await fetch(threadEndpointUrl + "?tid=" + threadId, {
        "method": "GET",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    })
    let json = await titleRaw.json()
    let title = json["threads"][0]["title"]
    $("#thread-title").text(title)
}

async function loadPosts(){
    let postsRaw = await fetch(postsEndpointUrl, {
        "method": "GET",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    })
    let json = await postsRaw.json()
    let posts = json["posts"]
    if (posts.length > 0){
        noPostsLabel.hide()
    } else {
        noPostsLabel.show()
    }
    for (let post of posts){
        let card = createPostCard(post["content"], post["author"], post["creation_date"], post["last_edit_date"], true, true)
        let delBtn = $(card).find(".delete-button-div-post")[0]
        let btnCard = $(card).find(".button-card")[0]
        $(delBtn).on("click", () => {
            createCardConfirmMenu(btnCard, true, "Delete", "Cancel", () => {
                deletePost(post["post_id"])
            }, () => {})
        })
        let editBtn = $(card).find(".edit-button-div-post")[0]
        $(editBtn).on("click", () => {
            let p = $(card).find(".card-text")[0]
            createEditCardDialog(btnCard, p, true, "Edit", "Cancel", (newText) => {
                updatePost(post["post_id"], newText)
            }, () => {})
        })
        postContainer.append(card)
    }
}

function deletePost(pid){
    fetch(postsEndpointUrl + "/" + pid, {
        "method": "DELETE",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    }).then(() => {
        window.location.reload();
    }).catch((err) => {
        console.log(err)
        alert("Failed to delete post")
    })
}

function updatePost(pid, newContent){
    fetch(postsEndpointUrl + "/" + pid, {
        "method": "PUT",
        "body": JSON.stringify({"content": newContent}),
        "headers": {
            "Content-Type": "application/json"
        }
    }).then(() => {
        window.location.reload();
    }).catch((err) => {
        console.log(err)
        alert("Failed to update post")
    })
}

loadTitle().catch((err) => {
    console.error(err)
    alert("Failed to load title")
})
loadPosts().catch((err) => {
    console.error(err)
    alert("Failed to load posts")
})