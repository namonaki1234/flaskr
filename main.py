from flaskr import app
from flask import render_template, request, redirect, url_for, jsonify
import sqlite3
DATABASE = 'database.db'

# 単語一覧表示
@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT * FROM books').fetchall()
    con.close()

    books =[]
    for row in db_books:
        books.append({'title': row[0], 'author': row[1]})
          
    return render_template('index.html', books=books)

@app.route('/add')
def add_word():
    return render_template('add_word.html')

@app.route('/register', methods=['POST'])
def register():
    title = request.form['title']
    author = request.form['author']
    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO books (title, author) VALUES (?, ?)', [title, author])
    con.commit()
    con.close()
    return redirect(url_for('index'))

# 書籍リストをJSON形式で取得するエンドポイント
@app.route('/words', methods=['GET'])
def get_words():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT title FROM books').fetchall()
    con.close()

    words = [row[0] for row in db_books]  # タイトルのみをリストに格納
    return jsonify(words)
    

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
