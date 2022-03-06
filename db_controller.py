"""
    This module provides an interface to the database. 
"""

from app_factory import mongo

"""
    Controller requirements checklist:
        [] get categories
        [] get threads
        [] get posts
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

def test():
    return mongo.db.test.find_one({"type": "var"})["value"]