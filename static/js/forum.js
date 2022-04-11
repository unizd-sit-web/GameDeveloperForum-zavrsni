import {API_BASE_URL, STATIC_BASE_URL, createThreadCard} from "./util.js";

const categoryContainer = $("#category-container")
const staticCategoryEndpointUrl = STATIC_BASE_URL + "/forum/categories"
const categoryEndpointUrl = API_BASE_URL + "/forum/categories"
const noCategoriesLabel = $("#no-categories-label")
console.log(categoryEndpointUrl)
$("#new-category-btn").click(() => {
    let params = new URLSearchParams(window.location.search)
    params.set("redir_url", window.location.href)
    params.set("category_route", categoryEndpointUrl)
    window.location.href = "/forum/categories/new?" + params.toString()
})

async function loadCategories(){
    let categoriesRaw = await fetch(categoryEndpointUrl, {
        "method": "GET",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    })
    let json = await categoriesRaw.json()
    let categories = json["categories"]
    if (categories.length > 0){
        noCategoriesLabel.hide()
    } else {
        noCategoriesLabel.show()
    }
    for (let category of categories){
        let card = createThreadCard(category["title"], staticCategoryEndpointUrl + "/" + category["category_id"] + "/threads")
        categoryContainer.append(card)
    }
}

loadCategories().catch((err) => {
    console.error(err)
    alert("Failed to load categories")
})