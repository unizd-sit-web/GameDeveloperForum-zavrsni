import {getThreadsIds, getThreadByIdFiltered, getCategoryByIdFiltered} from "./storage.js"
import {createThreadCard} from "./util.js"

// load navbar template
$("#navbar-placeholder").load("navbar.html");
// load footer template
$("#footer-placeholder").load("footer.html");

// constants
const searchParams = new URLSearchParams(window.location.search);
const sectionId = searchParams.get("section_id");
const categoryId = searchParams.get("category_id");
const noThreadsLabel = $("#no-threads-label");
const threadContainer = $("#thread-container");
const categoryTitle = $("#category-title");

async function fetchTitle(){
    let category = await getCategoryByIdFiltered(sectionId, categoryId, ["title"]).catch(console.error);
    categoryTitle.text(category["title"]);
}

async function fetchThreads(){
    let ids = await getThreadsIds(sectionId, categoryId, 10).catch(console.error);
    if (ids.length > 0){
        noThreadsLabel.hide();
    }
    for (let id of ids){
        let thread = await getThreadByIdFiltered(sectionId, categoryId, id, ["title"]).catch(console.error);
        let queryString = `section_id=${sectionId}&category_id=${categoryId}&thread_id=${id}`;
        let card = createThreadCard(thread["title"], "./thread.html?" + queryString);
        threadContainer.append(card);
    }
}

fetchTitle().catch(console.error);
fetchThreads().catch(console.error);
$("#new-thread-btn").click(() => {
    var searchParams = new URLSearchParams(window.location.search)
    searchParams.set("section_id", sectionId)
    searchParams.set("category_id", categoryId)
    searchParams.set("redir", window.location.href)
    window.location.href = "./new_thread.html?" + searchParams.toString()
})