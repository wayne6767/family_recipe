
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# 資料庫位置
os.makedirs("instance", exist_ok=True)
DATABASE = os.path.join("instance", "recipes.db")


# 建立資料庫
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL,
            author TEXT NOT NULL,
            ingredients_and_steps TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# 首頁：顯示所有食譜
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    recipes = conn.execute(
        "SELECT * FROM recipes ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", recipes=recipes)


# 新增食譜
@app.route("/add", methods=["GET", "POST"])
def add_recipe():

    if request.method == "POST":

        recipe_name = request.form["recipe_name"]
        author = request.form["author"]
        ingredients_and_steps = request.form["ingredients_and_steps"]

        conn = sqlite3.connect(DATABASE)

        conn.execute("""
            INSERT INTO recipes
            (recipe_name, author, ingredients_and_steps)
            VALUES (?, ?, ?)
        """, (recipe_name, author, ingredients_and_steps))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_recipe.html")


# 查看食譜詳細內容
@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id = ?",
        (recipe_id,)
    ).fetchone()

    conn.close()

    if recipe is None:
        return "找不到這道食譜", 404

    return render_template(
        "recipe_detail.html",
        recipe=recipe
    )


# 初始化資料庫
init_db()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
