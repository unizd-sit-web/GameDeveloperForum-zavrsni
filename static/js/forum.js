import {API_BASE_URL, STATIC_BASE_URL, createCardConfirmMenu, createThreadCard} from "./util.js";

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
        let card = createThreadCard(category["title"], staticCategoryEndpointUrl + "/" + category["category_id"] + "/threads", true)
        let delBtn = $(card).find(".delete-button-div-thread")[0]
        $(delBtn).on("click", () => {
            createCardConfirmMenu(card, false, "Delete", "Cancel", () => {
                deleteCategory(category["category_id"])
            }, () => {})
        })
        categoryContainer.append(card)
    }
}

function deleteCategory(cid){
    fetch(categoryEndpointUrl + "/" + cid, {
        "method": "DELETE",
        "mode": "cors",
        "Access-Control-Allow-Origin": "*"
    })
    .then(() => {
        window.location.reload()
    }).catch((err) => {
        console.error(err)
        alert("Failed to delete category")
    })
}

loadCategories().catch((err) => {
    console.error(err)
    alert("Failed to load categories")
})