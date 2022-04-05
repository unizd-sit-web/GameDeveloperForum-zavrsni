from flask import render_template, request, Response
import json
from app_factory import create_app
from db_controller import *
from datetime import datetime

config = {
    "MONGO_URI" : "mongodb://localhost:27017/GameDevForum"
}

app = create_app(config)

# constants
PAGE_ELEMENT_COUNT = 10

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

def get_formated_time():
    # format: day-month-year
    return datetime.now().strftime("%d-%m-%Y")

# list news threads
@app.route("/", methods=["GET"])
def get_news_threads():    
    news_categories = get_categories_in_section("news", 1, 0)
    if news_categories == None:
        return "", 404

    news_category = None
    if len(news_categories) > 0:
        news_category = news_categories[0]
    else:
        return "", 404

    page = request.args.get("page", 0, type=int)
    news_threads = get_threads_in_category(news_category["category_id"], PAGE_ELEMENT_COUNT, page * PAGE_ELEMENT_COUNT)

    return render_template("index.html", threads=news_threads)

# form for creating news threads
@app.route("/new", methods=["GET"])
def new_news_thread_form():
    return render_template("new_thread.html")

# create news thread
@app.route("/", methods=["POST"])
def create_news_thread():
    thread_data = request.get_json()

    if not "title" in thread_data:
        return json.dumps({"error": "Title is required"}), 400

    news_categories = get_categories_in_section("news", 1, 0)
    if news_categories == None:
        return json.dumps("Main news category does not exist"), 404

    news_category = None
    if len(news_categories) > 0:
        news_category = news_categories[0]
    else:
        return json.dumps("Main news category does not exist"), 404

    try:
        thread_id = create_thread(thread_data["title"], news_category["category_id"])
    except NoSuchElementException | ValueError:
        return json.dumps({"error": "Internal error"}), 500

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
    if thread_data == None or len(thread_data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400
    
    try:
        update_thread(thread_id, thread_data)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return Response(status=204)

# delete news thread
@app.route("/news/threads/<thread_id>", methods=["DELETE"])
def delete_news_thread(thread_id):
    try:
        delete_thread(thread_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404

    return Response(status=204)
   
# get news posts
@app.route("/news/threads/<thread_id>/posts", methods=["GET"])
def get_news_posts(thread_id):    
    page = request.args.get("page", 0, type=int)
    try:
        posts = get_posts_in_thread(thread_id, PAGE_ELEMENT_COUNT, page * PAGE_ELEMENT_COUNT)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404

    return render_template("thread.html", posts=posts)

# create post in news thread
@app.route("/news/threads/<thread_id>/posts", methods=["POST"])
def create_news_post(thread_id):
    post_data = request.get_json()
    if post_data == None or len(post_data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400

    if not "content" in post_data:
        return json.dumps({"error": "Invalid request body"}), 400

    # TODO: Using "Admin" for now, but username should be fetched from the 
    # login system once it is implemented.
    try:
        post_id = create_post("Admin", post_data["content"], get_formated_time(), thread_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return json.dumps({"new_post_id": post_id}), 201

# update news post
@app.route("/news/threads/<thread_id>/posts/<post_id>", methods=["PUT"])
def update_news_post(thread_id, post_id):
    """
        request payload:
        {
            "content": "new_content_here"
        }
    """
    post_data = request.get_json()
    if post_data == None or len(post_data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400

    try:
        update_post(post_id, post_data)
    except NoSuchElementException:
        return json.dumps({"error": f"Post with id {post_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return Response(status=204)


# delete post in a news thread
@app.route("/news/threads/<thread_id>/posts/<post_id>", methods=["DELETE"])
def delete_news_post(thread_id, post_id):    
    try:
        delete_post(post_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Post with id {post_id} does not exist"}), 404
    
    return Response(status=204)


# get forum categories
@app.route("/forum/categories", methods=["GET"])
def get_forum_categories():
    page = request.args.get("page", 0, type=int)
    try:
        forum_categories = get_categories_in_section("forum", PAGE_ELEMENT_COUNT, page * PAGE_ELEMENT_COUNT)
    except NoSuchElementException:
        return json.dumps({"error": f"Forum section does not exist"}), 404
    
    return render_template("forum.html", categories=forum_categories)

# create forum category
@app.route("/forum/categories", methods=["POST"])
def create_forum_category():
    data = request.get_json()
    if data == None or len(data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400
    
    if not "title" in data:
        return json.dumps({"error": "Invalid request body"}), 400

    try:
        category_id = create_category(data["title"], "forum")
    except NoSuchElementException:
        return json.dumps({"error": f"Forum section does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return json.dumps({"new_category_id": category_id}), 201

# form for creating forum categories
@app.route("/forum/categories/new", methods=["GET"])
def new_forum_category_form():
    return render_template("new_category.html")

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
    if data == None or len(data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400

    if not "title" in data:
        return json.dumps({"error": "Invalid request body"}), 400

    try:
        update_category(category_id, data)
    except NoSuchElementException:
        return json.dumps({"error": f"Category with id {category_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return Response(status=204)

# delete forum category
@app.route("/forum/categories/<category_id>", methods=["DELETE"])
def delete_forum_category(category_id):
    try:
        delete_category(category_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Category with id {category_id} does not exist"}), 404
    
    return Response(status=204)
    
# get threads from forum category
@app.route("/forum/categories/<category_id>/threads", methods=["GET"])
def get_forum_threads(category_id):
    page = request.args.get("page", 0, type=int)
    try:
        threads = get_threads_in_category(category_id, PAGE_ELEMENT_COUNT, page * PAGE_ELEMENT_COUNT)
    except NoSuchElementException:
        return json.dumps({"error": f"Category with id {category_id} does not exist"}), 404
    return render_template("category.html", threads=threads)

# create forum thread
@app.route("/forum/categories/<category_id>/threads", methods=["POST"])
def create_forum_thread(category_id):
    data = request.get_json()
    if data == None or len(data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400

    if not "title" in data:
        return json.dumps({"error": "Invalid request body"}), 400

    try:
        thread_id = create_thread(data["title"], category_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Category with id {category_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return json.dumps({"new_thread_id": thread_id}), 201

# form for creating forum threads
@app.route("/forum/categories/<category_id>/threads/new", methods=["GET"])
def new_forum_thread_form(category_id):
    return render_template("new_thread.html")

# delete thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>", methods=["DELETE"])
def delete_forum_thread(category_id, thread_id):
    try:
        delete_thread(thread_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404

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
    if data == None or len(data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400

    if not "title" in data:
        return json.dumps({"error": "Invalid request body"}), 400

    try:
        update_thread(thread_id, data)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return Response(status=204)

# create new post in thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts", methods=["POST"])
def create_forum_post(category_id, thread_id):
    post_data = request.get_json()
    if post_data == None or len(post_data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400
    
    if not "content" in post_data:
        return json.dumps({"error": "Invalid request body"}), 400

    try:
        post_id = create_post("Admin", post_data["content"], get_formated_time(), thread_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400
        
    return json.dumps({"new_post_id": post_id}), 201

# get posts from thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts", methods=["GET"])
def get_forum_posts(category_id, thread_id):
    page = request.args.get("page", 0, type=int)
    try:
        posts = get_posts_in_thread(thread_id, PAGE_ELEMENT_COUNT, page * PAGE_ELEMENT_COUNT)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404

    return render_template("thread.html", posts=posts)

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
    if data == None or len(data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400

    try:
        update_post(post_id, data)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400

    return Response(status=204)

# delete post in thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts/<post_id>", methods=["DELETE"])
def delete_forum_post(category_id, thread_id, post_id):
    try:
        delete_post(post_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404

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
