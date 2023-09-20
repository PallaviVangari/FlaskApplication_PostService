from flask import Flask, jsonify, request, abort
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return jsonify([dict(post) for post in posts])

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return jsonify(dict(post))

@app.route('/api/posts', methods=['POST'])
def create_post():
    if not request.json or not 'title' in request.json or not 'content' in request.json:
        abort(400)
    new_post = {
        'title': request.json['title'],
        'content': request.json['content']
    }
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                 (new_post['title'], new_post['content']))
    conn.commit()
    conn.close()
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    if not request.json or not 'title' in request.json or not 'content' in request.json:
        abort(400)
    updated_post = {
        'title': request.json['title'],
        'content': request.json['content']
    }
    conn = get_db_connection()
    conn.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?",
                 (updated_post['title'], updated_post['content'], post_id))
    conn.commit()
    conn.close()
    return jsonify(updated_post)

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(port=5000)