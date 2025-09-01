<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for sessions

users = {}  # fake "database" (in-memory)

@app.route("/")
def home():
    if "user" in session:
        return f"Welcome back, {session['user']}! <a href='/logout'>Logout</a>"
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users[email] = password
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users and users[email] == password:
            session["user"] = email  # ✅ store login in session
            return redirect(url_for("home"))
        else:
            return "Invalid credentials, try again."
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)  # ✅ remove user from session
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

=======
from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from models import register_user, login_user, create_food_post, get_food_posts, claim_food, get_user_claims

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for sessions

@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if "user_id" not in session or session.get("role") != "donor":
        return redirect(url_for("login"))
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_posts WHERE id = %s AND donor_id = %s", (post_id, session["user_id"]))
    post = cursor.fetchone()
    message = ""
    if request.method == "POST":
        food_name = request.form.get("food_name")
        description = request.form.get("description")
        quantity = request.form.get("quantity")
        expiry_date = request.form.get("expiry_date")
        location = request.form.get("location")
        cursor.execute("UPDATE food_posts SET food_name=%s, description=%s, quantity=%s, expiry_date=%s, location=%s WHERE id=%s", (food_name, description, quantity, expiry_date, location, post_id))
        conn.commit()
        message = "Post updated!"
        cursor.execute("SELECT * FROM food_posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit_post.html", post=post, message=message, user=session)

@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "user_id" not in session or session.get("role") != "donor":
        return redirect(url_for("login"))
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_posts WHERE id = %s AND donor_id = %s", (post_id, session["user_id"]))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Post deleted!")
    return redirect(url_for("donor_dashboard"))
@app.route("/donor_home")
def donor_home():
    if "user_id" not in session or session.get("role") != "donor":
        return redirect(url_for("login"))
    donor_id = session["user_id"]
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) FROM food_posts WHERE donor_id = %s", (donor_id,))
    total_posts = cursor.fetchone()["COUNT(*)"]
    cursor.execute("SELECT SUM(quantity) FROM food_posts WHERE donor_id = %s", (donor_id,))
    total_quantity = cursor.fetchone()["SUM(quantity)"] or 0
    # Motivational quote
    quote = "Sharing food is sharing love. Thank you for making a difference!"
    # Leaderboard: top 5 donors by quantity
    cursor.execute("""
        SELECT u.name AS donor_name, SUM(f.quantity) AS total
        FROM food_posts f
        JOIN users u ON f.donor_id = u.id
        GROUP BY u.name
        ORDER BY total DESC
        LIMIT 5
    """)
    leaderboard = cursor.fetchall()
    # Notifications: recent posts/claims
    cursor.execute("SELECT description, created_at FROM food_posts WHERE donor_id = %s ORDER BY created_at DESC LIMIT 3", (donor_id,))
    notifications = cursor.fetchall()
    # Recent food posts (carousel)
    cursor.execute("SELECT food_name, description, image_url FROM food_posts WHERE status = 'approved' ORDER BY id DESC LIMIT 5")
    recent_posts = cursor.fetchall()
    # Recipient testimonials (feedback from claims)
   
    # Calculate progress percent for the progress bar
    try:
        progress_percent = int((total_quantity / 100) * 100) if total_quantity < 100 else 100
    except Exception:
        progress_percent = 0
    cursor.close()
    conn.close()
    return render_template(
        "donor_home.html",
        total_posts=total_posts,
        total_quantity=total_quantity,
        user=session,
        quote=quote,
        leaderboard=leaderboard,
        notifications=notifications,
        recent_posts=recent_posts,
        progress_percent=progress_percent
    )
@app.route("/donor_dashboard")
def donor_dashboard():
    if "user_id" not in session or session.get("role") != "donor":
        return redirect(url_for("login"))
    donor_id = session["user_id"]
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_posts WHERE donor_id = %s", (donor_id,))
    donor_posts = cursor.fetchall()
    # Get feedback for donor's posts
    post_ids = [post['id'] for post in donor_posts]
    feedback = {}
    if post_ids:
        format_strings = ','.join(['%s'] * len(post_ids))
        cursor.execute(f"SELECT food_post_id,  FROM claims WHERE food_post_id IN ({format_strings}) ", tuple(post_ids))
        for row in cursor.fetchall():
            feedback.setdefault(row['food_post_id'], []).append(row['feedback_text'])
    cursor.execute("SELECT COUNT(*) FROM food_posts WHERE donor_id = %s", (donor_id,))
    total_posts = cursor.fetchone()["COUNT(*)"]
    cursor.execute("SELECT COUNT(*) FROM food_posts WHERE donor_id = %s AND status = 'pending'", (donor_id,))
    pending_posts = cursor.fetchone()["COUNT(*)"]
    cursor.execute("SELECT COUNT(*) FROM food_posts WHERE donor_id = %s AND status = 'approved'", (donor_id,))
    approved_posts = cursor.fetchone()["COUNT(*)"]
    cursor.execute("SELECT SUM(quantity) FROM food_posts WHERE donor_id = %s", (donor_id,))
    total_quantity = cursor.fetchone()["SUM(quantity)"] or 0
    cursor.close()
    conn.close()
    return render_template("donor_dashboard.html", donor_posts=donor_posts, total_posts=total_posts, pending_posts=pending_posts, approved_posts=approved_posts, total_quantity=total_quantity, user=session)

@app.route("/post_food", methods=["GET", "POST"])
def post_food():
    if "user_id" not in session or session.get("role") != "donor":
        return redirect(url_for("login"))
    message = ""
    if request.method == "POST":
        food_name = request.form.get("food_name")
        description = request.form.get("description")
        quantity = request.form.get("quantity")
        expiry_date = request.form.get("expiry_date")
        location = request.form.get("location")
        donor_id = session["user_id"]
        donor_name = session["name"]
        try:
            from models import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO food_posts (food_name, description, quantity, expiry_date, location, donor_id, donor_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (food_name, description, quantity, expiry_date, location, donor_id, donor_name)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash("Food post created!")
            return redirect(url_for("dashboard"))
        except Exception as e:
            message = f"Error posting food: {e}"
    return render_template("post_food.html", user=session, message=message)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    message = ""
    if request.method == "POST":
        new_name = request.form.get("name")
        new_password = request.form.get("password")
        # Update user in database (simple demo, not secure for production)
        from models import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        if new_name:
            cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, session["user_id"]))
            session["name"] = new_name
        if new_password:
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, session["user_id"]))
        conn.commit()
        cursor.close()
        conn.close()
        message = "Profile updated!"
    return render_template("profile.html", user=session, message=message)
@app.route("/claim_food/<int:food_post_id>", methods=["POST"])
def claim_food_route(food_post_id):
    if "user_id" not in session or session.get("role") != "recipient":
        return redirect(url_for("login"))
    recipient_id = session["user_id"]
    from models import get_db_connection
    import datetime
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    today = datetime.date.today()
    # Check if already claimed today (using date_requested column)
    cursor.execute(
        "SELECT * FROM claims WHERE food_post_id = %s AND recipient_id = %s AND DATE(date_requested) = %s",
        (food_post_id, recipient_id, today)
    )
    existing_claim = cursor.fetchone()
    cursor.fetchall()  # Ensure all results are read
    cursor.close()
    if existing_claim:
        conn.close()
        flash("You have already requested this food today.")
        return redirect(url_for("dashboard"))
    try:
        # Use a new cursor for the insert
        cursor2 = conn.cursor()
        claim_food(food_post_id, recipient_id)
        cursor2.close()
        conn.close()
        flash("Food requested successfully!")
        return redirect(url_for("dashboard"))
    except Exception as e:
        conn.close()
        return f"Error claiming food: {e}"

@app.route("/requests")
def requests():
    if "user_id" not in session or session.get("role") != "recipient":
        return redirect(url_for("login"))
    claims = get_user_claims(session["user_id"])
    return render_template("requests.html", claims=claims)



@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")  # default role
        phone = request.form.get("phone")
        address = request.form.get("address")
        # If email is admin@foodshare.com, set role to admin
        if email == "admin@foodshare.com":
            role = "admin"
        try:
            register_user(name, email, password, role, phone, address)
            return redirect(url_for("login"))
        except Exception as e:
            return f"Registration failed: {e}"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = login_user(email, password)
        if user:
            session["user"] = user["email"]
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]
            session["phone"] = user.get("phone", "")
            session["address"] = user.get("address", "")
            if user["role"] == "donor":
                return redirect(url_for("donor_home"))
            else:
                return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials, try again."
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    search = request.args.get("search", "")
    location = request.args.get("location", "")
    donor = request.args.get("donor", "")
    expiry = request.args.get("expiry", "")
    quantity = request.args.get("quantity", "")
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Admin view: show all posts
    if session.get("role") == "admin":
        cursor.execute("SELECT * FROM food_posts")
        posts = cursor.fetchall()
    # Recipient view: show all posts (not just approved)
    elif session.get("role") == "recipient":
        cursor.execute("SELECT * FROM food_posts")
        posts = cursor.fetchall()
    # Donor view: show only approved posts
    else:
        cursor.execute("SELECT * FROM food_posts WHERE status = 'approved'")
        posts = cursor.fetchall()
    # Filter posts in Python (for demo; ideally, filter in SQL)
    if search:
        posts = [p for p in posts if search.lower() in p["food_name"].lower()]
    if location:
        posts = [p for p in posts if location.lower() in p["location"].lower()]
    if donor:
        posts = [p for p in posts if donor.lower() in p["donor_name"].lower()]
    if expiry:
        posts = [p for p in posts if p["expiry_date"] >= expiry]
    if quantity:
        try:
            qty = int(quantity)
            posts = [p for p in posts if int(p["quantity"]) >= qty]
        except:
            pass
    # Dashboard stats
    cursor.execute("SELECT SUM(quantity) FROM food_posts WHERE status = 'approved'")
    total_saved = cursor.fetchone()["SUM(quantity)"] or 0
    cursor.execute("SELECT COUNT(*) FROM claims")
    total_shared = cursor.fetchone()["COUNT(*)"] or 0
    cursor.close()
    conn.close()
    messages = get_flashed_messages()
    return render_template("dashboard.html", posts=posts, user=session, search=search, location=location, donor=donor, expiry=expiry, quantity=quantity, total_saved=total_saved, total_shared=total_shared, messages=messages)

@app.route("/approve_food/<int:food_post_id>", methods=["POST"])
def approve_food(food_post_id):
    if session.get("role") != "admin":
        return "Unauthorized", 403
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE food_posts SET status = 'approved' WHERE id = %s", (food_post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

>>>>>>> f7d95ff (FoodShare)
