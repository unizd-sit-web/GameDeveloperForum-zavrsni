/**
 * @file Utility file for commonly used functions
 */

export const API_BASE_URL = "http://localhost:5000/api"
export const STATIC_BASE_URL = "http://localhost:5000"

/**
 * 
 * @param {string} title 
 * @param {string} redirUrl - when the card is clicked, the user is redirected to this url 
 * @param {boolean} addDeleteButton
 * @param {boolean} addEditButton
 * @returns Card as a DOM element
 */
 export function createThreadCard(title, redirUrl, addDeleteButton, addEditButton){
    let card = $("<div>")
    card.addClass("button-card")

    let linkDiv = $("<div>")
    linkDiv.addClass("button-card-other-div")
    let link = $("<a>")
    link.attr("href", redirUrl)
    link.text(title)
    link.addClass("list-group-item list-group-item-action p-3")
    linkDiv.append(link)

    card.append(linkDiv)

    let buttonDiv = $("<div>")
    buttonDiv.addClass("button-card-buttons-div")

    if (addEditButton === true){
        let editBtnDiv = $("<div>")
        editBtnDiv.addClass("card-button edit-button-div-thread bordered-button")
        let editIcon = $("<i>")
        editIcon.addClass("fa-solid fa-pen p-3")
        editBtnDiv.append(editIcon)

        buttonDiv.append(editBtnDiv)
    }

    card.append(buttonDiv)
    
    if (addDeleteButton === true){
        let delBtnDiv = $("<div>")
        delBtnDiv.addClass("card-button delete-button-div-thread bordered-button")
        let deleteIcon = $("<i>")
        deleteIcon.addClass("fa-solid fa-trash p-3")
        delBtnDiv.append(deleteIcon)

        buttonDiv.append(delBtnDiv)
    }

    return card.get(0)
}

/**
 * 
 * @param {HTMLElement} buttonCard - the card to add the menu to
 * @param {string} yesBtnText - the text on the yes button
 * @param {string} noBtnText - the text on the no button
 * @param {Function} yesBtnCallback - called when the yes button is clicked
 * @param {Function} noBtnCallback - called when the no button is clicked
 */
export function createCardConfirmMenu(buttonCard, isPost, yesBtnText, noBtnText, yesBtnCallback, noBtnCallback){
    let cardButtonDiv = $(buttonCard).find(".button-card-buttons-div")[0]
    let yesBtn = $("<button>")
    yesBtn.addClass("btn btn-danger")
    yesBtn.text(yesBtnText)
    yesBtn.css("margin-right", "10px")
    let noBtn = $("<button>")
    noBtn.addClass("btn btn-success")
    noBtn.text(noBtnText)
    let dialogDiv = $("<div>")
    dialogDiv.addClass("button-card-buttons-div bordered-button")
    if (isPost === true){
        dialogDiv.addClass("confirm-menu-post")
    } else {
        dialogDiv.addClass("confirm-menu-thread")
    }
    dialogDiv.append(yesBtn)
    dialogDiv.append(noBtn)
    dialogDiv.css("display", "flex")
    dialogDiv.css("justify-content", "center")
    dialogDiv.css("align-items", "center")
    yesBtn.click(() => {
        yesBtnCallback()
        dialogDiv.remove()
        $(cardButtonDiv).show()
    })
    noBtn.click(() => {
        noBtnCallback()
        dialogDiv.remove()
        $(cardButtonDiv).show()
    })
    $(buttonCard).append(dialogDiv)
    dialogDiv.show()
    $(cardButtonDiv).hide()
}

/**
 * 
 * @param {string} content 
 * @param {string} author 
 * @param {string} createDate 
 * @param {string} editDate 
 * @param {boolean} addDeleteButton
 * @returns Card as a DOM element
 */
export function createPostCard(content, author, createDate, editDate, addDeleteButton, addEditButton){
    let card = $("<div>")
    card.addClass("card")
    let cardBody = $("<div>")
    cardBody.addClass("card-body")
    let cardTitle = $("<h5>")
    cardTitle.addClass("card-title")
    cardTitle.text(author)
    let cardText = $("<p>")
    cardText.addClass("card-text")
    cardText.text(content)
    let cardFooter = $("<div>")
    cardFooter.addClass("card-footer button-card")
    let cardFooterTextDiv = $("<div>")
    cardFooterTextDiv.addClass("button-card-other-div-post")
    let cardFooterText = $("<small>")
    cardFooterText.addClass("text-muted")
    if (createDate == editDate){
        cardFooterText.text("Created: " + createDate)
    } else {
        cardFooterText.text("Created: " + createDate + " Edited: " + editDate)
    }
    cardFooterTextDiv.append(cardFooterText)
    
    let buttonDiv = $("<div>")
    buttonDiv.addClass("button-card-buttons-div")
    if (addEditButton === true){
        let editBtnDiv = $("<div>")
        editBtnDiv.addClass("edit-button-div-post")
        if (addDeleteButton === true){
            editBtnDiv.addClass("me-3")
        }
        let editIcon = $("<i>")
        editIcon.addClass("fa-solid fa-pen card-footer-button hover-black-foreground")
        editBtnDiv.append(editIcon)

        buttonDiv.append(editBtnDiv)
    }
    if (addDeleteButton === true){
        let delBtnDiv = $("<div>")
        delBtnDiv.addClass("delete-button-div-post")
        let deleteIcon = $("<i>")
        deleteIcon.addClass("fa-solid fa-trash card-footer-button hover-black-foreground")
        delBtnDiv.append(deleteIcon)

        buttonDiv.append(delBtnDiv)
    }
    
    cardFooter.append(cardFooterTextDiv)
    cardFooter.append(buttonDiv)
    cardBody.append(cardTitle)
    cardBody.append(cardText)
    card.append(cardBody)
    card.append(cardFooter)
    return card
}

export function createTitledCard(title, createdDate, redirUrl){
    var card = document.createElement("a");
    card.className = "list-group-item list-group-item-action flex-column align-items-start";
    card.href = redirUrl;
    var cardHeader = document.createElement("div");
    cardHeader.className = "d-flex w-100 justify-content-between";
    var cardTitle = document.createElement("h5");
    cardTitle.className = "mb-1";
    cardTitle.innerHTML = title;
    var cardDate = document.createElement("small");
    cardDate.className = "text-muted";
    cardDate.innerHTML = createdDate;
    cardHeader.appendChild(cardTitle);
    cardHeader.appendChild(cardDate);
    card.appendChild(cardHeader);
    var cardBody = document.createElement("p");
    cardBody.className = "mb-1";
    cardBody.innerHTML = "Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.";
    card.appendChild(cardBody);
    var cardFooter = document.createElement("small");
    cardFooter.className = "text-muted";
    cardFooter.innerHTML = "Donec id elit non mi porta.";
    card.appendChild(cardFooter);
    return card;
}

export function createEditCardDialog(buttonCard, textElement, isPost, yesButtonText, noButtonText, yesButtonCallback, noButtonCallback){
    let otherDiv = $($(buttonCard).find(".button-card-other-div")[0])
    otherDiv.addClass("border")
    let editField
    if (isPost === true){
        editField = $("<textarea>")
        editField.addClass("form-control")
        editField.val(textElement.innerHTML)
        editField.css("resize", "none")
    } else {
        editField = $("<input>")
        editField.addClass("m-1 list-group-item list-group-item-action border")
        editField.attr("style", "width: 40%")
        editField.attr("type", "text")
        editField.val(textElement.innerHTML)
    }
    $(textElement).parent().append(editField)
    editField.focus()
    $(textElement).hide()

    createCardConfirmMenu(buttonCard, isPost, yesButtonText, noButtonText, () => {
        editField.remove()
        $(textElement).show()
        otherDiv.removeClass("border")
        yesButtonCallback(editField.val())
    }, () => {
        editField.remove()
        $(textElement).show()
        otherDiv.removeClass("border")
        noButtonCallback()
    })
}