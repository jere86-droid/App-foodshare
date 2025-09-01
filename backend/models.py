# models.py
from config import get_db_connection

# Register a new user
def register_user(name, email, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
        (name, email, password, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Login user
def login_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # fetch results as dicts
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Post food (for donors)
def create_food_post(donor_id, food_name, description, quantity, expiry_date, location):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO food_posts (donor_id, food_name, description, quantity, expiry_date, location) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (donor_id, food_name, description, quantity, expiry_date, location)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Get available food posts
def get_food_posts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT food_posts.*, users.name AS donor_name FROM food_posts "
        "JOIN users ON food_posts.donor_id = users.id"
    )
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

# Claim food (for recipients)
def claim_food(food_post_id, recipient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO claims (food_post_id, recipient_id) VALUES (%s, %s)",
        (food_post_id, recipient_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Get claims for a recipient
def get_user_claims(recipient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT claims.*, food_posts.food_name, food_posts.location "
        "FROM claims JOIN food_posts ON claims.food_post_id = food_posts.id "
        "WHERE claims.recipient_id = %s",
        (recipient_id,)
    )
    claims = cursor.fetchall()
    cursor.close()
    conn.close()
    return claims
