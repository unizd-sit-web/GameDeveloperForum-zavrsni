"""
    This module provides an interface to the database. 
"""

from app_factory import mongo
from random import choice

"""
    MogoDB data structure:
        Collections:
            * sections
                {
                    _id: ObjectId(...),
                    "title": "Forum",
                    "section_id": "...",
                    "categories": [
                        "category_id",
                        "category_id",
                        "category_id"
                    ]
                }
            * categories
                {
                    _id: ObjectId(...),
                    "title": "Unity",
                    "category_id": "...",
                    "parent_section_id": "...",
                    "threads": [
                        "thread_id",
                        "thread_id",
                        "thread_id"
                    ]
                }
            * threads
                {
                    _id: ObjectId(...),
                    "title": "How to multiply two Vector3s",
                    "thread_id": "...",
                    "parent_category_id": "...",
                    "posts": [
                        "post_id",
                        "post_id",
                        "post_id"
                    ]
                }
            * posts
                {
                    _id: ObjectId(...),
                    "author": "...",
                    "content": "...",
                    "post_id": "...",
                    "parent_thread_id": "...",
                    "creation_date": "...",
                    "last_edit_date": "..."
                }

    Note: _id is a internal MongoDB generated field that should not be sent to the client.

    Controller requirements checklist:
        [✔] get categories
        [✔] get threads
        [✔] get posts
        [✔] create category
        [✔] create thread
        [✔] create post
        [✔] update category
        [✔] update thread
        [✔] upate post
        [✔] delete category
        [✔] delete thread
        [✔] delete post
"""

"""
    Field projection maps

    Projection maps specify whether a field should be included or excluded from queries.
    1 - include
    0 - exclude
"""
section_projection_map = {
    "_id": 0,
    "title": 1,
    "section_id": 1,
    "categories": 1
}
category_projection_map = {
    "_id": 0,
    "title": 1,
    "category_id": 1,
    "parent_section_id": 1,
    "threads": 1
}
thread_projection_map = {
    "_id": 0,
    "title": 1,
    "thread_id": 1,
    "parent_category_id": 1,
    "posts": 1
}
post_projection_map = {
    "_id": 0,
    "author": 1,
    "content": 1,
    "post_id": 1,
    "parent_thread_id": 1,
    "creation_date": 1,
    "last_edit_date": 1
}

ID_CHAR_COUNT = 10

# custom exception classes
class NoSuchElementException(Exception):
    """
        Used when the requested element is not found in the database.
    """
    pass

def generate_random_id(length: int) -> str:
    """
        Generates a random alpha-numeric string of length characters.
    """
    id = ""
    for x in range(length):
        is_letter = choice([True, False])
        if is_letter:
            id += choice(list("abcdefghijklmnopqrstuvwxyz"))
        else:
            id += choice(list("0123456789"))

    return id

def get_categories_in_section(section_name: str, limit: int, skip: int = 0) -> list | None:
    """
        Returns a list of limit categories in the section or None if the section does not exist.
        If specified, skip makes the controller skip n amount of entries allowing the user to page content.
    """
    section = mongo.db.sections.find_one({"title": section_name})
    if section is None:
        return None
    section_id = section["section_id"]

    return list(mongo.db.categories.find({"parent_section_id": section_id}, category_projection_map).skip(skip).limit(limit))

def get_threads_in_category(category_id: str, limit: int, skip: int = 0) -> list:
    """
        Returns a list of limit threads in the category.
        If specified, skip makes the controller skip n amount of entries allowing the user to page content.
    """
    return list(mongo.db.threads.find({"parent_category_id": category_id}, thread_projection_map).skip(skip).limit(limit))

def get_posts_in_thread(thread_id: str, limit: int, skip: int = 0) -> list:
    """
        Returns a list of limit posts in the thread.
        If specified, skip makes the controller skip n amount of entries allowing the user to page content.
    """
    return list(mongo.db.posts.find({"parent_thread_id": thread_id}, post_projection_map).skip(skip).limit(limit))

def create_category(title: str, section_name: str) -> str:
    """
        Creates a category in the section.

        Returns the category id.

        Raises NoSuchElementException if section does not exist.
        Raises ValueError if
    """
    # check if parent section exists
    parent_section = mongo.db.sections.find_one({"title": section_name})
    if parent_section is None:
        raise NoSuchElementException(f"section called {section_name} does not exist")
 
    # validate input
    if title is None or len(title) == 0:
        raise ValueError("title cannot be empty")

    # create category
    category_id = generate_random_id(ID_CHAR_COUNT)
    category = {
        "title": title,
        "category_id": category_id,
        "parent_section_id": parent_section["section_id"],
        "threads": []
    }
    mongo.db.categories.insert_one(category)

    # insert category into section
    mongo.db.sections.update_one({"section_name": section_name}, {"$push": {"categories": category_id}})
    
    return category_id

def create_thread(title: str, category_id: str) -> str:
    """
        Creates a thread in the category.

        Returns the thread id.

        Raises NoSuchElementException if category does not exist.
    """
    # check if parent category exists
    parent_category = mongo.db.categories.find_one({"category_id": category_id})
    if parent_category is None:
        raise NoSuchElementException(f"category called {category_id} does not exist")

    # validate input
    if title is None or len(title) == 0:
        raise ValueError("title cannot be empty")
    
    # create thread
    thread_id = generate_random_id(ID_CHAR_COUNT)
    thread = {
        "title": title,
        "thread_id": thread_id,
        "parent_category_id": parent_category["category_id"],
        "posts": []
    }
    mongo.db.threads.insert_one(thread)

    # insert thread into category
    mongo.db.categories.update_one({"category_id": parent_category["category_id"]}, {"$push": {"threads": thread_id}})

    return thread_id

def create_post(author: str, content: str, creation_date: str, thread_id: str) -> str:
    """
        Creates a post in the thread.

        Returns the post id.

        Raises NoSuchElementException if thread does not exist.
    """
    # check if thread exists
    parent_thread = mongo.db.threads.find_one({"thread_id": thread_id})
    if parent_thread is None:
        raise NoSuchElementException(f"thread called {thread_id} does not exist")
    
    # validate input
    if author is None or len(author) == 0:
        raise ValueError("author cannot be empty")
    if content is None or len(content) == 0:
        raise ValueError("content cannot be empty")
    if creation_date is None or len(creation_date) == 0:
        raise ValueError("creation_date cannot be empty")

    # create post
    post_id = generate_random_id(ID_CHAR_COUNT)
    post = {
        "author": author,
        "content": content,
        "post_id": post_id,
        "parent_thread_id": parent_thread["thread_id"],
        "creation_date": creation_date,
        "last_edit_date": creation_date
    }
    mongo.db.posts.insert_one(post)

    # insert post into thread
    mongo.db.threads.update_one({"thread_id": parent_thread["thread_id"]}, {"$push": {"posts": post_id}})

    return post_id

def update_category(category_id: str, new_data: str) -> None:
    """
        Updates the category data by overwriting fields with new_data.

        Raises NoSuchElementException if category does not exist.
    """
    # check if category exists
    category = mongo.db.categories.find_one({"category_id": category_id})
    if category is None:
        raise NoSuchElementException(f"category called {category_id} does not exist")

    # validate input
    if new_data is None or len(new_data) == 0:
        raise ValueError("new_data cannot be empty")    
    
    # filter fields
    to_update = {}
    if "title" in new_data:
        if new_data["title"] is None or len(new_data["title"]) == 0:
            raise ValueError("new_data.title cannot be empty")
        to_update["title"] = new_data["title"]
    if len(to_update) == 0:
        raise ValueError("new_data has no valid fields")

    # update category
    mongo.db.categories.update_one({"category_id": category_id}, {"$set": to_update})

def update_thread(thread_id: str, new_data: dict) -> None:
    """
        Updates the thread data by overwriting fields with new_data.

        Raises NoSuchElementException if thread does not exist.
    """
    # check if thread exists
    thread = mongo.db.threads.find_one({"thread_id": thread_id})
    if thread is None:
        raise NoSuchElementException(f"thread called {thread_id} does not exist")

    # validate input
    if new_data is None or len(new_data) == 0:
        raise ValueError("new_data cannot be empty")    
    
    # filter fields
    to_update = {}
    if "title" in new_data:
        if new_data["title"] is None or len(new_data["title"]) == 0:
            raise ValueError("new_data.title cannot be empty")
        to_update["title"] = new_data["title"]
    if len(to_update) == 0:
        raise ValueError("new_data has no valid fields")

    # update thread
    mongo.db.threads.update_one({"thread_id": thread_id}, {"$set": to_update})

def update_post(post_id: str, new_data: dict) -> None:
    """
        Updates the post data by overwriting fields with new_data.

        Raises NoSuchElementException if post does not exist.
    """
    # check if post exists
    post = mongo.db.posts.find_one({"post_id": post_id})
    if post is None:
        raise NoSuchElementException(f"post called {post_id} does not exist")

    # validate input
    if new_data is None or len(new_data) == 0:
        raise ValueError("new_data cannot be empty")    
    
    # filter fields
    to_update = {}
    if "content" in new_data:
        if new_data["content"] is None or len(new_data["content"]) == 0:
            raise ValueError("new_data.content cannot be empty")
        to_update["content"] = new_data["content"]
    if "last_edit_date" in new_data:
        if new_data["last_edit_date"] is None or len(new_data["last_edit_date"]) == 0:
            raise ValueError("new_data.last_edit_date cannot be empty")
        to_update["last_edit_date"] = new_data["last_edit_date"]
    if len(to_update) == 0:
        raise ValueError("new_data has no valid fields")

    # update post
    mongo.db.posts.update_one({"post_id": post_id}, {"$set": to_update})

def delete_post(post_id: str) -> None:
    """
        Deletes the post.

        Raises NoSuchElementException if post does not exist.
    """
    # check if post exists
    post = mongo.db.posts.find_one({"post_id": post_id})
    if post is None:
        raise ValueError(f"post called {post_id} does not exist")

    # remove post from thread
    mongo.db.threads.update_one({"thread_id": post["parent_thread_id"]}, {"$pull": {"posts": post_id}})

    # delete post
    mongo.db.posts.delete_one({"post_id": post_id})

def delete_thread(thread_id: str) -> None:
    """
        Deletes the thread and all its posts.

        Raises NoSuchElementException if thread does not exist.
    """
    # check if thread exists
    thread = mongo.db.threads.find_one({"thread_id": thread_id})
    if thread is None:
        raise ValueError(f"thread called {thread_id} does not exist")

    # delete posts
    mongo.db.posts.delete_many({"parent_thread_id": thread_id})

    # remove thread from category
    mongo.db.categories.update_one({"category_id": thread["parent_category_id"]}, {"$pull": {"threads": thread_id}})

    # delete thread
    mongo.db.threads.delete_one({"thread_id": thread_id})

def delete_category(category_id: str) -> None:
    """
        Deletes the category and all its threads and posts.

        Raises NoSuchElementException if category does not exist.
    """
    # check if category exists
    category = mongo.db.categories.find_one({"category_id": category_id})
    if category is None:
        raise ValueError(f"category called {category_id} does not exist")

    # delete threads
    for thread_id in category["threads"]:
        delete_thread(thread_id)

    # remove category from section
    mongo.db.sections.update_one({"section_id": category["parent_section_id"]}, {"$pull": {"categories": category_id}})
    
    # delete category
    mongo.db.categories.delete_one({"category_id": category_id})