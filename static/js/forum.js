import {getSectionIdByTitle, getCategoriesIds, getCategoryByIdFiltered} from "./storage.js"
import {createThreadCard} from "./util.js"

// load navbar template
$("#navbar-placeholder").load("navbar.html");
// load footer template
$("#footer-placeholder").load("footer.html");

// constants
const categoryContainer = $("#category-container")
const noCategoriesLabel = $("#no-categories-label")

let sectionId
/**
 * Sets sectionId to the id of this section
 */
async function fetchId(){
    sectionId = await getSectionIdByTitle("Forum").catch(console.error)
}

/**
 * Fetches all categories and adds them to the DOM
 */
async function fetchCategories(){
    let ids = await getCategoriesIds(sectionId, 10).catch(console.error)
    if (ids.length > 0){
        noCategoriesLabel.hide()
    }
    for (let id of ids){
        let category = await getCategoryByIdFiltered(sectionId, id, ["title"]).catch(console.error)
        let queryString = `section_id=${sectionId}&category_id=${id}`
        let card = createThreadCard(category["title"], "./category.html?" + queryString)
        categoryContainer.append(card)
    }
}

fetchId().then(() => {
    fetchCategories().catch(console.error)
}).catch(console.error)