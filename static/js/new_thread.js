import {createThread, createPost} from "./storage.js"

// load navbar template
$("#navbar-placeholder").load("navbar.html");
// load footer template
$("#footer-placeholder").load("footer.html");

// constants
const titleField = $("#title-field");
const contentField = $("#content-field");
const btn = $("#new-thread-btn");
const searchParams = new URLSearchParams(window.location.search);
const sectionId = searchParams.get("section_id");
const categoryId = searchParams.get("category_id");
const redirUrl = searchParams.get("redir");

btn.click(() => {
    let title = titleField.val();
    let content = contentField.val();
    if (!(title.length > 0 && content.length > 0)) {
        alert("Title and content cannot be empty!");
        return
    }
    createThread(sectionId, categoryId, title).then((tid) => {
        createPost(sectionId, categoryId, tid, content, "Admin").then((pid) => {
            window.location.href = redirUrl
        }).catch(console.error);
    }).catch(console.error);
})