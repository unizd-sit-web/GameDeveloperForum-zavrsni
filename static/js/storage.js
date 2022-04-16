/**
 * @file This module is an interface between the frontend and the upcoming backend api
 *
/*
    Simulated database format:
    {
        "sections": {
            "sectionId": {
                "id": "id",
                "title": "title",
                "categories": {
                    "categoryId": {
                        "id": "id",
                        "title": "title",
                        "threads": {
                            "threadId": {
                                "id": "id",
                                "title": "title",
                                "posts": {
                                    "postId": {
                                        "id": "id",
                                        "author": "author",
                                        "content": "content",
                                        "creation_date": "date",
                                        "edit_date": "date"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
*/
export const ERROR_CODES = {
    "UNINITIALIZED": 0,
    "DB_ERROR": 1
}

let db = {}


 // create methods start here

/**
 * 
 * @param {string} title 
 * @returns {Promise<string|number} id of section on resolve, error code on reject
 */
export async function createSection(title){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let section = {
        "id": generateRandomId(),
        "title": title,
        "categories": {}
    }
    try {
        db["sections"][section["id"]] = section
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
    return section["id"]
}

/**
 * 
 * @param {number} sectionId 
 * @param {string} title 
 * @returns {Promise<number|number>} id of category on resolve, error code on reject
 */
export async function createCategory(sectionId, title) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let category = {
        "id": generateRandomId(),
        "sectionId": sectionId,
        "title": title,
        "threads": {}
    }
    try {
        db["sections"][sectionId]["categories"][category["id"]] = category
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
    return category["id"]
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {string} title 
 * @returns {Promise<number|number>} id of thread on resolve, error code on reject
 */
export async function createThread(sectionId, categoryId, title) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let thread = {
        "id": generateRandomId(),
        "categoryId": categoryId,
        "title": title,
        "posts": {}
    }
    try {
        db["sections"][sectionId]["categories"][categoryId]["threads"][thread["id"]] = thread
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
    return thread["id"]
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {string} content 
 * @param {string} author 
 * @returns {Promise<number|number>} id of post on resolve, error code on reject
 */
export async function createPost(sectionId, categoryId, threadId, content, author) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
    let date = new Date().toLocaleDateString(undefined, dateOptions)
    let post = {
        "id": generateRandomId(),
        "threadId": threadId,
        "content": content,
        "author": author,
        "creation_date": date,
        "last_modified_date": date
    }
    try {
        db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"][post["id"]] = post
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
    return post["id"]
}

// get methods start here

/**
 * 
 * @param {string} sectionTitle 
 * @returns {Promise<number|number>} section id on resolve, error code on reject
 */
 export async function getSectionIdByTitle(sectionTitle){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    for (let sectionId in db["sections"]){
        if (db["sections"][sectionId]["title"] == sectionTitle){
            return sectionId
        }
    }
    return Promise.reject(ERROR_CODES["UNINITIALIZED"])
}

/**
 * 
 * @param {number} sectionId 
 * @returns {Promise<Object|number>} section object on resolve, error code on reject
 */
export async function getSectionById(sectionId){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        return db["sections"][sectionId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
}

/**
 * Get specific fields of a section object
 * @param {number} sectionId 
 * @param {string[]} filterArray 
 * @returns {Promise<Object|number} filtered section object on resolve, error code on reject
 */
export async function getSectionByIdFiltered(sectionId, filterArray){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let section
    try {
        section = db["sections"][sectionId] 
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    let filtered = {}
    for (let key of filterArray) {
        if (section.hasOwnProperty(key)) {
            filtered[key] = section[key]
        }
    }
    return filtered
}

/**
 * 
 * @returns {Promise<string[]|number>} section ids on resolve, error code on reject
 */
export async function getSectionsIds(){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    return Object.keys(db["sections"])
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @returns {Promise<Object|number>} category object on resolve, error code on reject
 */
 export async function getCategoryById(sectionId, categoryId) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        return db["sections"][sectionId]["categories"][categoryId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} limit 
 * @returns {Promise<number[]|number>} first N category ids of section on resolve, error code on reject
 */
export async function getCategoriesIds(sectionId, limit) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let categoryIds
    try {
        categoryIds = db["sections"][sectionId]["categories"]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    categoryIds = Object.keys(categoryIds).slice(0, limit)
    let categories = []
    for (let categoryId of categoryIds) {
        categories.push(parseInt(categoryId))
    }
    return categories
}

/**
 * Get specific fields of a category object
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {string[]} filterArray 
 * @returns {Promise<Object|number>} filtered category object on resolve, error code on reject
 */
export async function getCategoryByIdFiltered(sectionId, categoryId, filterArray){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let category
    try {
        category = db["sections"][sectionId]["categories"][categoryId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    let filtered = {}
    for (let key of filterArray) {
        if (category.hasOwnProperty(key)) {
            filtered[key] = category[key]
        }
    }
    return filtered
}

/**
 * Get specific fields of a thread object
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {string[]} filterArray 
 * @returns {Promise<Object|number>} filtered thread object on resolve, error code on reject
 */
 export async function getThreadByIdFiltered(sectionId, categoryId, threadId, filterArray) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let thread
    try {
        thread = db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    let filtered = {}
    for (let key of filterArray) {
        if (thread.hasOwnProperty(key)) {
            filtered[key] = thread[key]
        }
    }
    return filtered
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @returns {Promise<Object|number>} thread object on resolve, error code on reject
 */
export async function getThreadById(sectionId, categoryId, threadId) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    return db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} limit 
 * @returns {Promise<number[]|number>} first N thread ids of category on resolve, error code on reject
 */
export async function getThreadsIds(sectionId, categoryId, limit) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let threadIds
    try {
        threadIds = db["sections"][sectionId]["categories"][categoryId]["threads"]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    threadIds = Object.keys(threadIds).slice(0, limit)
    let threads = []
    for (let threadId of threadIds) {
        threads.push(parseInt(threadId))
    }
    return threads
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {number} postId 
 * @returns {Promise<Object|number>} post object on resolve, error code on reject
 */
 export async function getPostById(sectionId, categoryId, threadId, postId) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        return db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"][postId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {number} limit 
 * @returns {Promise<number[]|number>} first N post ids of thread on resolve, error code on reject
 */
export async function getPostsIds(sectionId, categoryId, threadId, limit) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let postIds
    try {
        postIds = db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    postIds = Object.keys(postIds).slice(0, limit)
    let posts = []
    for (let postId of postIds) {
        posts.push(parseInt(postId))
    }
    return posts;
}

/**
 * Get specific fields of a post object
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {number} postId 
 * @param {string[]} filterArray 
 * @returns {Promise<Object|number>} filtered post object on resolve, error code on reject
 */
export async function getPostByIdFiltered(sectionId, categoryId, threadId, postId, filterArray){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    let post
    try {
        post = db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"][postId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    let filtered = {}
    for (let key of filterArray) {
        if (post.hasOwnProperty(key)) {
            filtered[key] = post[key]
        }
    }
    return filtered
}

// modify methods start here

/**
 * 
 * @param {number} sectionId 
 * @param {string} newTitle 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function modifySectionTitle(sectionId, newTitle) {
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        db["sections"][sectionId]["title"] = newTitle
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {string} newTitle 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function modifyCategoryTitle(sectionId, categoryId, newTitle){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        db["sections"][sectionId]["categories"][categoryId]["title"] = newTitle
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {string} newTitle 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function modifyThreadTitle(sectionId, categoryId, threadId, newTitle){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["title"] = newTitle
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {number} postId 
 * @param {string} newContent 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function modifyPostContent(sectionId, categoryId, threadId, postId, newContent){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"][postId]["content"] = newContent
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

/**
 * 
 * @param {number} postId 
 * @param {Date} newDate 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function modifyPostEditDate(postId, newDate){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"][postId]["edit_date"] = newDate
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

/**
 * 
 * @param {number} postId 
 * @param {Date} newDate 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function modifyPostCreationDate(postId, newDate){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"][postId]["creation_date"] = newDate
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch((e) => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

// delete methods start here

/**
 * 
 * @param {number} sectionId 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function deleteSectionById(sectionId){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        delete db["sections"][sectionId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch(e => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
} 
/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function deleteCategoryById(sectionId, categoryId){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        delete db["sections"][sectionId]["categories"][categoryId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch(e => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
    
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function deleteThreadById(sectionId, categoryId, threadId){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        delete db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch(e => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

/**
 * 
 * @param {number} sectionId 
 * @param {number} categoryId 
 * @param {number} threadId 
 * @param {number} postId 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
export async function deletePostById(sectionId, categoryId, threadId, postId){
    let db = getDatabase()
    if (db == null){
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    }
    try {
        delete db["sections"][sectionId]["categories"][categoryId]["threads"][threadId]["posts"][postId]
    } catch (e){
        return Promise.reject(ERROR_CODES["UNINITIALIZED"])
    }
    await saveDatabase(db).catch(e => {
        return Promise.reject(ERROR_CODES["DB_ERROR"])
    })
}

// utility functions for simulating the database

/**
 * Internal function used for simulating the database
 * @returns {Object} basic database object
 */
function initDatabase() {
    let newsSectionId = generateRandomId()
    let newsCategoryId = generateRandomId()
    let forumSectionId = generateRandomId()
    let unityCategoryId = generateRandomId()
    let database = {
        "sections": {
            [newsSectionId]: {
                "id": newsSectionId,
                "title": "News",
                "categories": {
                    [newsCategoryId]: {
                        "id": newsCategoryId,
                        "title": "News category",
                        "threads": {
                        }
                    }
                }
            },
            [forumSectionId]: {
                "id": forumSectionId,
                "title": "Forum",
                "categories": {
                    [unityCategoryId]: {
                        "id": unityCategoryId,
                        "title": "Unity",
                        "threads": {
                        }
                    }
                }
            }
        }
    }
    saveDatabase(database)
    return database
}


/**
 * Attempts to load the database from local storage and cache it in memory. If it fails to load, it initializes a new one.
 * @returns {Object|null} the database object or null if it fails to parse the raw JSON data
 */
function getDatabase(){
    let dbRaw = window.localStorage.getItem('database')
    if (dbRaw == null){
        db = initDatabase()
    } else {
        try {
            db = JSON.parse(dbRaw)
        } catch (e) {
            console.log(e)
            return null;
        }
    }
    return db
}

/**
 * Internal function used for simulating the database.
 * Saves the database to local storage
 * @param {object} database 
 * @returns {Promise<void|number>} void on resolve, error code on reject
 */
async function saveDatabase(database){
    try {
        window.localStorage.setItem('database', JSON.stringify(database))
    } catch (e) {
        console.log(e)
        return Promise.reject(e)
    }
}


/**
 * Internal function used for simulating the database.
 * @returns {number} random id
 */
function generateRandomId() {
    return Math.floor(Math.random() * 1000000);
}