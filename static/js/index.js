import { getSectionIdByTitle, getCategoriesIds, getThreadsIds, getThreadByIdFiltered } from './storage.js';
import { createThreadCard } from "./util.js"

// load navbar template
$("#navbar-placeholder").load("navbar.html");
// load footer template
$("#footer-placeholder").load("footer.html");

// constants
const threadContainer = $("#thread-container")
const noThreadsLabel = $("#no-threads-label")

let sectionId
let categoryId
/**
 * Fetches and caches the id of the section this page belongs to and the id of the category that should be displayed
 */
async function fetchids() {
    sectionId = await getSectionIdByTitle("News").catch(console.error)
    let ids = await getCategoriesIds(sectionId, 1).catch(console.error)
    categoryId = ids[0]
}

/**
 * Fetches and displays threads from the category
 */
async function loadThreads() {
    let threadsIds = await getThreadsIds(sectionId, categoryId, 10).catch(console.error)
    if (threadsIds.length > 0) {
        noThreadsLabel.remove()
    }
    for (let threadId of threadsIds) {
        let threadData = await getThreadByIdFiltered(sectionId, categoryId, threadId, ["title"]).catch(console.error)
        let queryString = `section_id=${sectionId}&category_id=${categoryId}&thread_id=${threadId}`
        let threadCard = createThreadCard(threadData["title"], "./thread.html?" + queryString)
        threadContainer.append(threadCard)
    }
}

fetchids().then(() => {
    loadThreads().catch(console.error)
    // new thread button redirects to a form page and supplies the section and category id via urlquery
    $("#new-thread-btn").click(() => {
        var searchParams = new URLSearchParams(window.location.search)
        searchParams.set("section_id", sectionId)
        searchParams.set("category_id", categoryId)
        searchParams.set("redir", window.location.href)
        window.location.href = "./new_thread.html?" + searchParams.toString()
    })
})

