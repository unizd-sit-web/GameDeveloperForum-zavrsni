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
        [] create category
        [] create thread
        [] create post
        [] update category
        [] update thread
        [] upate post
        [] delete category
        [] delete thread
        [] delete post
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

def get_categories_in_section(section_name: str, limit: int) -> list:
    """
        Returns a list of limit categories in the section.
    """
    section = mongo.db.sections.find_one({"title": section_name})
    if section is None:
        return None
    section_id = section["section_id"]

    return list(mongo.db.categories.find({"parent_section_id": section_id}, category_projection_map).limit(limit))

def get_threads_in_category(category_id: str, limit: int) -> list:
    """
        Returns a list of limit threads in the category.
    """
    return list(mongo.db.threads.find({"parent_category_id": category_id}, thread_projection_map).limit(limit))

def get_posts_in_thread(thread_id: str, limit: int) -> list:
    """
        Returns a list of limit posts in the thread.
    """
    return list(mongo.db.posts.find({"parent_thread_id": thread_id}, post_projection_map).limit(limit))