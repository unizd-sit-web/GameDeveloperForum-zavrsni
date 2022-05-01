from flask import render_template, request, Response, redirect
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json
from app_factory import create_app
from db_controller import *
from datetime import datetime

config = {
    "MONGO_URI" : "mongodb://localhost:27017/GameDevForum",
}

app = create_app(config)
app.secret_key = "abc"
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

# constants
PAGE_ELEMENT_COUNT = 10

# user loading (for login)
class User(UserMixin):
    def __init__(self, username, password_hash, email, id) -> None:
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.id = id
        
users = []

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == user_id:
            return user
    return None
""" 
    Static/API server structure:

    (Both servers are running on the same machine and on the same port for simplicity)

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


    STATIC: 

    news routes:
        /                                                           
            GET: homepage
            
        /news/categories/<category_id>/threads
            GET: index page (list of threads)

        /news/categories/<category_id>/threads/new                                  
            GET: form for creating a new thread
            
        /news/categories/<category_id>/threads/<thread_id>/posts
            GET: thread page (list of posts)

    forum routes:
        /forum/categories                                         
            GET: forum page

        /forum/categories/new
            GET: form for creating a new category
            
        /forum/categories/<category_id>/threads                         
            GET: category page (list of threads)

        /forum/categories/<category_id>/threads/new
            GET: form for creating a new thread

        /forum/categories/<category_id>/threads/<thread_id>/posts       
            GET:    list posts in a thread
            POST:   create a new post in a thread

        /forum/categories/<category_id>/threads/<thread_id>/posts
            GET: thread page (list of posts)

        /about
            GET: about page

        /rules
            GET: rules page

        /tos
            GET: terms of service page

        /privacy
            GET: privacy policy page

        /login
            GET: login page

    API:
        /api/<section_name>/categories/<category_id>/threads
            POST: create a new thread
        
        /api/<section_name>/categories/<category_id>/threads/<thread_id>/posts
            POST: create a new post in a thread

        /api/<section_name>/categories
            POST: create a new category

        /api/<section_name>/categories/<category_id>/threads/<thread_id>
            PUT: update a thread

        /api/<section_name>/categories/<category_id>/threads/<thread_id>/posts/<post_id>
            PUT: update a post in a thread
        
        /api/<section_name>/categories/<category_id>
            PUT: update a category

        /api/<section_name>/categories/<category_id>/threads/<thread_id>
            DELETE: delete a thread

        /api/<section_name>/categories/<category_id>/threads/<thread_id>/posts/<post_id>
            DELETE: delete a post in a thread

        /api/<section_name>/categories/<category_id>
            DELETE: delete a category

        /api/<section_name>/categories
            GET: get all categories in section

        /api/<section_name>/categories/<category_id>/threads
            GET: get all threads in category

        /api/<section_name>/categories/<category_id>/threads/<thread_id>/posts
            GET: get all posts in thread

        /api/login
            POST: request to authenticate with the api
        
        /api/logout
            GET: request to logout
"""

"""
    Static server starts here
"""
def get_formated_time():
    # format: day-month-year
    return datetime.now().strftime("%d-%m-%Y")

# Redirect to main news category
@app.route("/", methods=["GET"])
def root():
    return render_template("home.html")
    
# list news threads
@app.route("/news/categories/<category_id>/threads", methods=["GET"])
def get_news_threads(category_id):    
    return render_template("index.html")

# form for creating news threads
@app.route("/news/categories/<category_id>/threads/new", methods=["GET"])
def new_news_thread_form(category_id):
    return render_template("new_thread.html")

# get news posts
@app.route("/news/categories/<category_id>/threads/<thread_id>/posts", methods=["GET"])
def get_news_posts(category_id, thread_id):    
    return render_template("thread.html")

# get forum categories
@app.route("/forum/categories", methods=["GET"])
def get_forum_categories():
    return render_template("forum.html")

# form for creating forum categories
@app.route("/forum/categories/new", methods=["GET"])
def new_forum_category_form():
    return render_template("new_category.html")
 
# get threads from forum category
@app.route("/forum/categories/<category_id>/threads", methods=["GET"])
def get_forum_threads(category_id):
    return render_template("category.html")

# form for creating forum threads
@app.route("/forum/categories/<category_id>/threads/new", methods=["GET"])
def new_forum_thread_form(category_id):
    return render_template("new_thread.html")

# get posts from thread in forum category
@app.route("/forum/categories/<category_id>/threads/<thread_id>/posts", methods=["GET"])
def get_forum_posts(category_id, thread_id):
    return render_template("thread.html")

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

"""
    API server starts here
"""
# create thread
@app.route("/api/<section_name>/categories/<category_id>/threads", methods=["POST"])
def api_create_news_thread(section_name, category_id):
    thread_data = request.get_json()

    if not "title" in thread_data:
        return json.dumps({"error": "Title is required"}), 400

    try:
        thread_id = create_thread(thread_data["title"], category_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Category {category_id} does not exist"}), 500
    except ValueError:
        return json.dumps({"error": "Invalid title"}), 400
        
    return json.dumps({"new_thread_id": thread_id}), 201
    
# create post
@app.route("/api/<section_name>/categories/<category_id>/threads/<thread_id>/posts", methods=["POST"])
def api_create_post(section_name, category_id, thread_id):
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

# create category
@app.route("/api/<section_name>/categories", methods=["POST"])
def api_create_category(section_name):
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

# update thread
@app.route("/api/<section_name>/categories/<category_id>/threads/<thread_id>", methods=["PUT"])
def api_update_news_thread(section_name, category_id, thread_id):
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

# update post
@app.route("/api/<section_name>/categories/<category_id>/threads/<thread_id>/posts/<post_id>", methods=["PUT"])
def api_update_news_post(section_name, category_id, thread_id, post_id):
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

# update category
@app.route("/api/<section_name>/categories/<category_id>", methods=["PUT"])
def api_update_forum_category(section_name, category_id):
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

# delete thread
@app.route("/api/<section_name>/categories/<category_id>/threads/<thread_id>", methods=["DELETE"])
def api_delete_news_thread(section_name, category_id, thread_id):
    try:
        delete_thread(thread_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404

    return Response(status=204)

# delete post
@app.route("/api/<section_name>/categories/<category_id>/threads/<thread_id>/posts/<post_id>", methods=["DELETE"])
def api_delete_news_post(section_name, category_id, thread_id, post_id):    
    try:
        delete_post(post_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Post with id {post_id} does not exist"}), 404
    
    return Response(status=204)

# delete category
@app.route("/api/<section_name>/categories/<category_id>", methods=["DELETE"])
def api_delete_forum_category(section_name, category_id):
    try:
        delete_category(category_id)
    except NoSuchElementException:
        return json.dumps({"error": f"Category with id {category_id} does not exist"}), 404
    
    return Response(status=204)

# get categories in section
@app.route("/api/<section_name>/categories", methods=["GET"])
def api_get_categories(section_name):
    page = request.args.get("page", 0, type=int)
    # this allows the frontend to fetch info about a specific category
    category_id_filter = request.args.get("cid", None)
    if not category_id_filter == None:
        page = 0

    try:
        page = request.args.get("page", 0, type=int)
        categories = get_categories_in_section(section_name, page, page * PAGE_ELEMENT_COUNT, category_id_filter)
        return json.dumps({"categories": categories})
    except NoSuchElementException:
        return json.dumps({"error": f"Section {section_name} does not exist"}), 404
        
# get threads in category
@app.route("/api/<section_name>/categories/<category_id>/threads", methods=["GET"])
def api_get_threads(section_name, category_id):
    page = request.args.get("page", 0, type=int)
    # this allows the frontend to fetch info about a specific thread
    thread_id_filter = request.args.get("tid", None)
    if not thread_id_filter == None:
        page = 0

    try:
        threads = get_threads_in_category(category_id, PAGE_ELEMENT_COUNT, page * PAGE_ELEMENT_COUNT, thread_id_filter)
        return json.dumps({"threads": threads})
    except NoSuchElementException:
        return json.dumps({"error": f"Category with id {category_id} does not exist"}), 404

# get posts in thread
@app.route("/api/<section_name>/categories/<category_id>/threads/<thread_id>/posts", methods=["GET"])
def api_get_posts(section_name, category_id, thread_id):
    page = request.args.get("page", 0, type=int)
    # this allows the frontend to fetch info about a specific post
    post_id_filter = request.args.get("pid", None)
    if not post_id_filter == None:
        page = 0

    try:
        posts = get_posts_in_thread(thread_id, PAGE_ELEMENT_COUNT, page * PAGE_ELEMENT_COUNT, post_id_filter)
        return json.dumps({"posts": posts}) 
    except NoSuchElementException:
        return json.dumps({"error": f"Thread with id {thread_id} does not exist"}), 404

# request to create account
@app.route("/api/users", methods=["POST"])
def api_create_account():
    """
        request payload:
        {
            "username": "username_here",
            "password": "password_here",
            "email": "email_here"
        }
    """
    data = request.get_json()
    if data == None or len(data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400
    if not "username" in data or not "password" in data or not "email" in data:
        return json.dumps({"error": "Invalid request body"}), 400
    if len(data["username"]) == 0 or len(data["password"]) == 0 or len(data["email"]) == 0:
            return json.dumps({"error": "Invalid request body"}), 400

    try:
        create_user(data["username"], generate_password_hash(data["password"]), data["email"])
    except ValueError:
        return json.dumps({"error": "Invalid request body"}), 400
    except UsernameInUseException:
        return json.dumps({"error": "Username already exists"}), 400

    return Response(status=204)

# reguest to delete account
@app.route("/api/users/<user_id>", methods=["DELETE"])
@login_required
def api_delete_account(user_id):
    if not current_user.id == user_id:
        return json.dumps({"error": "You are not authorized to delete this account"}), 403

    try:
        delete_user(user_id)
        logout_user()
    except NoSuchElementException:
        return json.dumps({"error": f"User with id {user_id} does not exist"}), 404

    return Response(status=204)
    

# authentication request handler
@app.route("/api/login", methods=["POST"])
def api_login():
    auth_data = request.get_json()
    if auth_data == None or len(auth_data) == 0:
        return json.dumps({"error": "Invalid request body"}), 400
    username = auth_data["username"]
    password = auth_data["password"]
    try:
        db_user = get_user_by_username(username)
        if db_user == None:
            return json.dumps({"error": "Invalid username or password"}), 401
        if check_password_hash(db_user["password_hash"], password):
            user = User(db_user["username"], db_user["password_hash"], db_user["email"], db_user["user_id"])
            login_user(user)
            users.append(user)
            return json.dumps({"success": "Logged in successfully"}), 200
        else:
            return json.dumps({"error": "Invalid username or password"}), 401
    except NoSuchElementException:
        return json.dumps({"error": "Invalid username or password"}), 401

# logout request handler
@app.route("/api/logout", methods=["POST"])
@login_required
def api_logout():
    logout_user()
    return json.dumps({"success": "Logged out successfully"}), 200

# login system test
@app.route(("/api/secret"), methods=["GET"])
@login_required
def api_secret():
    return json.dumps({"secret": "This is a secret"})
