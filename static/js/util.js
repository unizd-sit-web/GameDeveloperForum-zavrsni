/**
 * @file Utility file for commonly used functions
 */

/**
 * 
 * @param {string} title 
 * @param {string} redirUrl - when the card is clicked, the user is redirected to this url 
 * @returns Card as a DOM element
 */
 export function createThreadCard(title, redirUrl){
    let a = $("<a>")
    a.attr("href", redirUrl)
    a.addClass("list-group-item list-group-item-action p-3")
    a.text(title)
    return a
}

/**
 * 
 * @param {string} content 
 * @param {string} author 
 * @param {string} createDate 
 * @param {string} editDate 
 * @returns Card as a DOM element
 */
export function createPostCard(content, author, createDate, editDate){
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
    cardFooter.addClass("card-footer")
    let cardFooterText = $("<small>")
    cardFooterText.addClass("text-muted")
    if (createDate == editDate){
        cardFooterText.text("Created: " + createDate)
    } else {
        cardFooterText.text("Created: " + createDate + " Edited: " + editDate)
    }
    cardFooter.append(cardFooterText)
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