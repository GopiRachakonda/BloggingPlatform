from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Update with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Karna$200513'  # Update with your MySQL password
app.config['MYSQL_DB'] = 'blog_platform'

mysql = MySQL(app)

# Home page - List all posts
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cur.fetchall()
    return render_template('home.html', posts=posts)

# View a single post with comments
@app.route('/post/<int:post_id>')
def post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", [post_id])
    post = cur.fetchone()

    if post:
        cur.execute("SELECT * FROM comments WHERE post_id = %s ORDER BY created_at DESC", [post_id])
        comments = cur.fetchall()
        return render_template('post.html', post=post, comments=comments)
    else:
        flash("Post not found", "danger")
        return redirect(url_for('home'))

# Create a new post
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title and content:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
            mysql.connection.commit()
            flash("Post created successfully", "success")
            return redirect(url_for('home'))
        else:
            flash("Title and Content are required", "danger")

    return render_template('create_post.html')

# Edit an existing post
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", [post_id])
    post = cur.fetchone()

    if post:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            if title and content:
                cur.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
                mysql.connection.commit()
                flash("Post updated successfully", "success")
                return redirect(url_for('post', post_id=post_id))
            else:
                flash("Title and Content are required", "danger")

        return render_template('create_post.html', post=post)
    else:
        flash("Post not found", "danger")
        return redirect(url_for('home'))

# Delete a post
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s", [post_id])
    mysql.connection.commit()
    flash("Post deleted successfully", "success")
    return redirect(url_for('home'))

# Add a comment to a post
@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    content = request.form['content']

    if content:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comments (post_id, content) VALUES (%s, %s)", (post_id, content))
        mysql.connection.commit()
        flash("Comment added successfully", "success")
    else:
        flash("Comment cannot be empty", "danger")

    return redirect(url_for('post', post_id=post_id))

if __name__ == "__main__":
    app.run(debug=True)

