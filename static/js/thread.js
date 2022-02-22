import {getThreadByIdFiltered, getPostsIds, getPostById, createPost} from "./storage.js"
import {createPostCard} from "./util.js"

// load navbar template
$("#navbar-placeholder").load("navbar.html")
// load footer template
$("#footer-placeholder").load("footer.html")

const searchParams = new URLSearchParams(window.location.search)
const sectionId = searchParams.get("section_id")
const categoryId = searchParams.get("category_id")
const threadId = searchParams.get("thread_id")
const postContainer = $("#post-container")
const noPostsLabel = $("#no-posts-label")
const threadTitle = $("#thread-title")
const newPostBtn = $("#new-post-btn")
const contentField = $("#content-field")

async function fetchPageTitle(){
    let thread = await getThreadByIdFiltered(sectionId, categoryId, threadId, ["title"]).catch(console.error)
    threadTitle.text(thread["title"])
    document.head.title = thread["title"]
}

async function fetchPosts(){
    let ids = await getPostsIds(sectionId, categoryId, threadId, 10).catch(console.error)
    if (ids.length > 0){
        noPostsLabel.hide()
    }
    for (let pid of ids){
        let post = await getPostById(sectionId, categoryId, threadId, pid);
        let card = createPostCard(post["content"], post["author"], post["creation_date"], post["last_modified_date"])
        postContainer.append(card);
    }
}

newPostBtn.click((e) => {
    e.preventDefault();
    let content = contentField.val();
    if (content.length > 0) {
        createPost(sectionId, categoryId, threadId, content, "Admin").then(() => {
            contentField.val("");
            window.location.reload();
        }).catch(console.error);
    }
})

fetchPageTitle().catch(console.error)
fetchPosts().catch(console.error)