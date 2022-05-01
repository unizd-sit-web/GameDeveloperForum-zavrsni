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
                    "author_id": "...",
                    "content": "...",
                    "post_id": "...",
                    "parent_thread_id": "...",
                    "creation_date": "...",
                    "last_edit_date": "..."
                }
            * users
                {
                    _id: ObjectId(...),
                    "user_id": "...",
                    "username": "...",
                    "password_hash": "...",
                    "email": "..."
                }

    Note: _id is a internal MongoDB generated field that should not be sent to the client.

    Controller requirements checklist:
        [✔] get categories
        [✔] get threads
        [✔] get posts
        [] get user
        [✔] create category
        [✔] create thread
        [✔] create post
        [] create user
        [✔] update category
        [✔] update thread
        [✔] upate post
        [] update user
        [✔] delete category
        [✔] delete thread
        [✔] delete post
        [] delete user
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
    "author_id": 1,
    "content": 1,
    "post_id": 1,
    "parent_thread_id": 1,
    "creation_date": 1,
    "last_edit_date": 1
}
user_projection_map = {
    "_id": 0,
    "user_id": 1,
    "username": 1,
    "password_hash": 1,
    "email": 1,
}

ID_CHAR_COUNT = 10

# custom exception classes
class NoSuchElementException(Exception):
    """
        Used when the requested element is not found in the database.
    """
    pass

class UsernameInUseException(Exception):
    """
        Used when the username is already in use.
    """
    pass

def generate_random_id(length: int) -> str:
    """
        Generates a random alpha-numeric string of length characters.
    """
    while True:
        id = ""
        for x in range(length):
            is_letter = choice([True, False])
            if is_letter:
                id += choice(list("abcdefghijklmnopqrstuvwxyz"))
            else:
                id += choice(list("0123456789"))
        # prevent id from conflicting with /threads/new or /categories/new routes
        if not id == "new":
            return id

def get_categories_in_section(section_name: str, limit: int, skip: int = 0, filter = None) -> list:
    """
        Returns a list of limit categories in the section or None if the section does not exist.
        If specified, skip makes the controller skip n amount of entries allowing the user to page content.
        The filter field which takes in a category id, is optional and can be used to return a list that contains
        info about the category with the specified id only.
    """
    section = mongo.db.sections.find_one({"title": section_name})
    if section is None:
        raise NoSuchElementException(f"section called {section_name} does not exist")
    section_id = section["section_id"]

    if filter is None:
        return list(mongo.db.categories.find({"parent_section_id": section_id}, category_projection_map).skip(skip).limit(limit))
    else:
        return list(mongo.db.categories.find({"parent_section_id": section_id, "category_id": filter}, category_projection_map).limit(1))

def get_threads_in_category(category_id: str, limit: int, skip: int = 0, filter: str = None) -> list:
    """
        Returns a list of limit threads in the category.
        If specified, skip makes the controller skip n amount of entries allowing the user to page content.
        The filter field which takes in a thread id, is optional and can be used to return a list that contains
        info about the thread with the specified id only.
    """
    category = mongo.db.categories.find_one({"category_id": category_id})
    if category is None:
        raise NoSuchElementException(f"category with id {category_id} does not exist")

    if filter is None:
        return list(mongo.db.threads.find({"parent_category_id": category_id}, thread_projection_map).skip(skip).limit(limit))
    else:
        return list(mongo.db.threads.find({"parent_category_id": category_id, "thread_id": filter}, thread_projection_map).limit(1))

def get_posts_in_thread(thread_id: str, limit: int, skip: int = 0, filter: str = None) -> list:
    """
        Returns a list of limit posts in the thread.
        If specified, skip makes the controller skip n amount of entries allowing the user to page content.
        The filter field which takes in a post id, is optional and can be used to return a list that contains
        info about the post with the specified id only.
    """
    thead = mongo.db.threads.find_one({"thread_id": thread_id})
    if thead is None:
        raise NoSuchElementException(f"thread called {thread_id} does not exist")
        
    if filter is None:
        return list(mongo.db.posts.find({"parent_thread_id": thread_id}, post_projection_map).skip(skip).limit(limit))
    else:
        return list(mongo.db.posts.find({"parent_thread_id": thread_id, "post_id": filter}, post_projection_map).limit(1))
        
def get_user_by_username(username: str) -> dict:
    """
        Returns a dictionary containing user data or returns None if the user does not exist.
    """
    return mongo.db.users.find_one({"username": username})

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
    mongo.db.sections.update_one({"title": section_name}, {"$push": {"categories": category_id}})
    
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

def create_post(author_id: str, content: str, creation_date: str, thread_id: str) -> str:
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
    if author_id is None or len(author_id) == 0:
        raise ValueError("author_id cannot be empty")
    if content is None or len(content) == 0:
        raise ValueError("content cannot be empty")
    if creation_date is None or len(creation_date) == 0:
        raise ValueError("creation_date cannot be empty")

    # create post
    post_id = generate_random_id(ID_CHAR_COUNT)
    post = {
        "author_id": author_id,
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

def create_user(username: str, password_hash: str, email: str):
    """
        Creates a user and returns its id.

        Raises UsernameInUse if username is already being used.

        Raises ValueError if required fields are empty.
    """
    # validate input
    if username is None or len(username) == 0:
        raise ValueError("username cannot be empty")
    if password_hash is None or len(password_hash) == 0:
        raise ValueError("password_hash cannot be empty")
    if email is None or len(email) == 0:
        raise ValueError("email cannot be empty")

    # check if username already exists
    user = mongo.db.users.find_one({"username": username})
    if user is not None:
        raise UsernameInUseException(f"username {username} is already taken")

    # create user
    user_id = generate_random_id(ID_CHAR_COUNT)
    user = {
        "username": username,
        "password_hash": password_hash,
        "email": email,
        "user_id": user_id
    }
    mongo.db.users.insert_one(user)

    return user_id

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

def update_user(user_id: str, new_data: dict) -> None:
    """
        Updates the user data by overwriting fields with new_data.

        Raises NoSuchElementException if user does not exist.
    """
    # check if user exists
    user = mongo.db.users.find_one({"user_id": user_id})
    if user is None:
        raise NoSuchElementException(f"user called {user_id} does not exist")

    # validate input
    if new_data is None or len(new_data) == 0:
        raise ValueError("new_data cannot be empty")    
    
    # filter fields
    to_update = {}
    if "username" in new_data:
        if new_data["username"] is None or len(new_data["username"]) == 0:
            raise ValueError("new_data.username cannot be empty")
        to_update["username"] = new_data["username"]
    if "password_hash" in new_data:
        if new_data["password_hash"] is None or len(new_data["password_hash"]) == 0:
            raise ValueError("new_data.password_hash cannot be empty")
        to_update["password_hash"] = new_data["password_hash"]
    if "email" in new_data:
        if new_data["email"] is None or len(new_data["email"]) == 0:
            raise ValueError("new_data.email cannot be empty")
        to_update["email"] = new_data["email"]
    if len(to_update) == 0:
        raise ValueError("new_data has no valid fields")

    # update user
    mongo.db.users.update_one({"user_id": user_id}, {"$set": to_update})

def delete_post(post_id: str) -> None:
    """
        Deletes the post.

        Raises NoSuchElementException if post does not exist.
    """
    # check if post exists
    post = mongo.db.posts.find_one({"post_id": post_id})
    if post is None:
        raise NoSuchElementException(f"post called {post_id} does not exist")

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
        raise NoSuchElementException(f"thread called {thread_id} does not exist")

    # delete posts
    for post in thread["posts"]:
        delete_post(post)

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
        raise NoSuchElementException(f"category called {category_id} does not exist")

    # delete threads
    for thread_id in category["threads"]:
        delete_thread(thread_id)

    # remove category from section
    mongo.db.sections.update_one({"section_id": category["parent_section_id"]}, {"$pull": {"categories": category_id}})
    
    # delete category
    mongo.db.categories.delete_one({"category_id": category_id})

def delete_user(user_id: str) -> None:
    """
        Deletes the user and all its posts.

        Raises NoSuchElementException if user does not exist.
    """
    # check if user exists
    user = mongo.db.users.find_one({"user_id": user_id})
    if user is None:
        raise NoSuchElementException(f"user called {user_id} does not exist")

    # update user posts
    mongo.db.posts.update_many({"author_id": user_id}, {"$set":{"author_id": None}})

    # delete user
    mongo.db.users.delete_one({"user_id": user_id})