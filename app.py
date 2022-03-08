from concurrent.futures import thread
from multiprocessing.spawn import import_main_path
from flask import Flask, redirect, render_template, request, Response
from random import randint
import json
from app_factory import create_app
from db_controller import *

config = {
    "MONGO_URI" : "mongodb://localhost:27017/GameDeveloperForum"
}
app = create_app(config)
# sample data for testing
database = {
    "sections": {
        "news": {
            "title": "News",
            "categories": {
                "news_category": {
                    "title": "What's new",
                    "threads": {
                        "751589": {
                            "id": "751589",
                            "title": "Plans for the forum",
                            "posts": {
                                "28510":{
                                    "id": "28510",
                                    "author": "Joda",
                                    "content": "hello world",
                                    "creation_date": "2022-01-01",
                                    "last_edit_date": "2022-01-01"
                                }
                            }
                        }
                    }
                }
            }
        },
        "forum": {
            "title": "Forum",
            "categories": {
                "7825": {
                    "id": "7825",
                    "title": "General",
                    "threads": {
                        "8575236": {
                            "id": "8575236",
                            "title": "How to use the forum",
                            "posts": {
                                "28510":{
                                    "id": "28510",
                                    "author": "Obi-Wan Kenobi",
                                    "content": "hello world",
                                    "creation_date": "2022-01-01",
                                    "last_edit_date": "2022-01-01"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

""" 
    Static/API server structure:

    route requirements checklist:
        news:
            [✔] get threads
            [✔] create thread
            [✔] delete thread
            [✔] update thread
            [✔] get posts in thread
            [✔] create post in thread
            [✔] delete post in thread
            [✔] update post in thread

        forum:
            [✔] get categories
            [✔] create category
            [✔] delete category
            [✔] update category
            [✔] get threads in category
            [✔] create thread in category
            [✔] delete thread in category
            [✔] update thread in category
            [✔] get posts in thread
            [✔] create post in thread
            [✔] delete post in thread
            [✔] update post in thread

    
    news routes:
        /                                                           
            GET:    list all threads
            POST:   create new thread
            
        /news/threads/<thread_id>
            PUT:    update a thread
            DELETE: delete a thread

        /news/threads/<thread_id>/posts                                   
            GET:    list posts in a thread
            POST:   create new post in a thread
            
        /news/threads/<thread_id>/posts/<post_id>
            PUT:    update a post in a thread
            DELETE: delete a post in a thread

    forum routes:
        /forum/categories                                         
            GET:    list all categories
            POST:   create new category

        /forum/categories/<category_id>
            PUT:    update a category
            DELETE: delete a category
            
        /forum/categories/<category_id>/threads                         
            GET:    list threads in category
            POST:   create new thread

        /forum/categories/<category_id>/threads/<thread_id>
            PUT:    update a thread
            DELETE: delete a thread

        /forum/categories/<category_id>/threads/<thread_id>/posts       
            GET:    list posts in a thread
            POST:   create a new post in a thread

        /forum/categories/<category_id>/threads/<thread_id>/posts/<post_id>
            PUT:    update a post in a thread
            DELETE: delete a post in a thread

    other routes:
        /about
        /rules
        /tos
        /privacy
        /login
"""

# TODO debug
@app.route('/debug')
def debug():
    """site = ""
    cats = get_categories_in_section("Forum")
    print(cats)
    for cat in cats:
        site += cat["title"] + "\n"
        threads = get_threads_in_category(cat["category_id"])
        print(threads)
        for thread in threads:
            print(thread)
            site += "\t" + thread["title"] + "\n"
            posts = get_posts_in_thread(thread["thread_id"])
            print(posts)
            for post in posts:
                site += "\t\t" + post["content"] + "\n"
    return site"""
    cats = get_categories_in_section("Forum", 1)
    site = "<ul>"
    for cat in cats:
        ats = "<ul>"
        for at in cat:
            ats += "<li>" + at + "</li>"
            ats += "</ul>"
        site += "<li>" + ats + "</li>"
    site += "</ul>"
    return site

# list news threads
@app.route("/", methods=["GET"])
def index_threads():
    news_threads = database["sections"]["news"]["categories"]["news_category"]["threads"]
    threads_filtered = []
    for thread_id in news_threads:
        threads_filtered.append({
            "id": thread_id,
            "title": news_threads[thread_id]["title"],
            "redir_url": f"/news/threads/{thread_id}/posts"
        })
    return render_template("index.html", threads=threads_filtered)

# create news thread
@app.route("/", methods=["POST"])
def index_post_thread():
    thread_data = request.get_json()
    thread_id = str(randint(0, 1000000))
    # TODO: currently not checking if data is valid for simplicity
    database["sections"]["news"]["categories"]["news_category"]["threads"][thread_id] = thread_data
    return json.dumps({"new_thread_id": thread_id}), 201

# update news thread
@app.route("/news/threads/<thread_id>", methods=["PUT"])
def update_news_thread(thread_id):
    """
        receive a request with the following payload and update the thread:
        {
            "title": "new_title_here"
        }
    """
    thread_data = request.get_json()
    database["sections"]["news"]["categories"]["news_category"]["threads"][thread_id]["title"] = thread_data["title"]
    return Response(status=204)

# delete news thread
@app.route("/news/threads/<thread_id>", methods=["DELETE"])
def delete_news_thread(thread_id):
    # TODO: check if thread exists first
    del database["sections"]["news"]["categories"]["news_category"]["threads"][thread_id]
    return Response(status=204)
   
# get posts from news thread
@app.route("/news/threads/<thread_id>/posts", methods=["GET"])
def news_thread(thread_id):
    thread = database["sections"]["news"]["categories"]["news_category"]["threads"][thread_id]
    posts = []
    for post_id in thread["posts"]:
        posts.append(thread["posts"][post_id])
    return render_template("thread.html", title=thread["title"], posts=posts)

# create post in news thread
@app.route("/news/threads/<thread_id>/posts", methods=["POST"])
def news_post_post(thread_id):
    # save post
    post_data = request.get_json()
    post_id = str(randint(0, 1000000))
    # TODO currently not checking if data is valid for simplicity
    database["sections"]["news"]["categories"]["news_category"]["threads"][thread_id]["posts"][post_id] = post_data
    return json.dumps({"new_post_id": post_id}), 201

# update post in news thread
@app.route("/news/threads/<thread_id>/posts/<post_id>", methods=["PUT"])
def update_news_post(thread_id, post_id):
    """
        request payload:
        {
            "content": "new_content_here"
        }
    """
    post_data = request.get_json()
    database["sections"]["news"]["categories"]["news_category"]["threads"][thread_id]["posts"][post_id]["content"] = post_data["content"]
    return Response(status=204)

# delete post in a news thread
@app.route("/news/threads/<thread_id>/posts/<post_id>", methods=["DELETE"])
def delete_news_post(thread_id, post_id):
    # TODO: check if post exists first
    del database["sections"]["news"]["categories"]["news_category"]["threads"][thread_id]["posts"][post_id]
    return Response(status=204)

# get forum categories
@app.route("/forum/categories", methods=["GET"])
def forum_categories():
    forum_categories = database["sections"]["forum"]["categories"]
    categories_filtered = []
    for category_id in forum_categories:
        categories_filtered.append({
            "id": category_id,
            "title": forum_categories[category_id]["title"],
            "redir_url": f"/forum/categories/{category_id}/threads"
        })
    return render_template("forum.html", categories=categories_filtered)

# create forum category
@app.route("/forum/categories", methods=["POST"])
def forum_post_category():
    data = request.get_json()
    category_id = str(randint(0, 1000000))
    # TODO: currently not checking if data is valid for simplicity
    database["sections"]["forum"]["categories"][category_id] = data
    return json.dumps({"new_category_id": category_id}), 201

# get forum category
@app.route("/forum/categories/<category_id>/threads", methods=["GET"])
def forum_category(category_id):
    category = database["sections"]["forum"]["categories"][category_id]
    threads_filtered = []
    for thread_id in category["threads"]:
        threads_filtered.append({
            "id": thread_id,
            "title": category["threads"][thread_id]["title"],
            "redir_url": f"/forum/categories/{category_id}/threads/{thread_id}/posts"
        })
    return render_template("category.html", title=category["title"],threads=threads_filtered)

# update forum category
@app.route("/forum/categories/<category_id>", methods=["PUT"])
def update_forum_category(category_id):
    """
        request payload:
        {   
            "title": "new_title_here"
        }
    """
    data = request.get_json()
    # TODO: check data (only allow title to be updated)
    database["sections"]["forum"]["categories"][category_id]["title"] = data["title"]
    return Response(status=204)

@app.route("/forum/categories/<category_id>", methods=["DELETE"])
def delete_forum_category(category_id):
    # TODO: check if category exists first
    del database["sections"]["forum"]["categories"][category_id]
    return Response(status=204)

# create forum thread
@app.route("/forum/categories/<category_id>/threads", methods=["POST"])
def forum_post_thread(category_id):
    data = request.get_json()
    thread_id = str(randint(0, 1000000))
    # TODO: currently not checking if data is valid for simplicity
    database["sections"]["forum"]["categories"][category_id]["threads"][thread_id] = data
    return json.dumps({"new_thread_id": thread_id}), 201

# delete thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>", methods=["DELETE"])
def delete_forum_thread(category_id, thread_id):
    data = request.get_json()
    # TODO: check if thread exists first
    del database["sections"]["forum"]["categories"][category_id]["threads"][thread_id]
    return Response(status=204)

# update thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>", methods=["PUT"])
def update_forum_thread(category_id, thread_id):
    """
        request payload:
        {
            "title": "new_title_here"
        }
    """
    data = request.get_json()
    # TODO: check data (only allow title to be updated)
    database["sections"]["forum"]["categories"][category_id]["threads"][thread_id]["title"] = data["title"]
    return Response(status=204)

# get posts from thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts", methods=["GET"])
def forum_thread(category_id, thread_id):
    thread = database["sections"]["forum"]["categories"][category_id]["threads"][thread_id]
    posts = []
    for post_id in thread["posts"]:
        posts.append(thread["posts"][post_id])
    return render_template("thread.html", title=thread["title"], posts=posts)

# create new post ni thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts", methods=["POST"])
def forum_post_post(category_id, thread_id):
    # save post
    post_data = request.get_json()
    post_id = str(randint(0, 1000000))
    # TODO currently not checking if data is valid for simplicity
    database["sections"]["forum"]["categories"][category_id]["threads"][thread_id]["posts"][post_id] = post_data
    return json.dumps({"new_post_id": post_id}), 201

# update post in thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts/<post_id>", methods=["PUT"])
def update_forum_post(category_id, thread_id, post_id):
    """
        request payload:
        {
            "title": "new_title_here"
        }
    """
    data = request.get_json()
    # TODO: check data (only allow title to be updated)
    database["sections"]["forum"]["categories"][category_id]["threads"][thread_id]["posts"][post_id]["content"] = data["content"]
    return Response(status=204)
    
# delete post in thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts/<post_id>", methods=["DELETE"])
def delete_forum_post(category_id, thread_id, post_id):
    # TODO: check if post exists first
    del database["sections"]["forum"]["categories"][category_id]["threads"][thread_id]["posts"][post_id]
    return Response(status=204)

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/rules", methods=["GET"])
def rules():
    return render_template("rules.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")

@app.route("/tos", methods=["GET"])
def tos():
    return render_template("tos.html")
