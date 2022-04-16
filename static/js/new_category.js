// constants
const titleField = $("#title-field");
const btn = $("#new-category-btn");

async function createCategory(route, title){
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
    return json["new_category_id"]
}

btn.click(() => {
    let title = titleField.val();
    if (!(title.length > 0)) {
        alert("Title cannot be empty!");
        return
    }
    // POST category to backend
    let params = new URLSearchParams(window.location.search)
    console.log(params.get("category_route"))
    createCategory(params.get("category_route"), title)
    .then(() => {
        window.location.href = params.get("redir_url")
    }).catch((err) => {
        alert("Failed to create category")
    })
})