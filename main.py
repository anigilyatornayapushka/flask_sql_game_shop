from flask import (
    Flask, 
    request,
    render_template,
    redirect,
)

from services import Connection


app: Flask = Flask(__name__)
conn: Connection = Connection()

conn.create_tables()
conn.create_user('admin', 'root')

@app.route('/', methods=['POST', 'GET'])
def online_shop():
    
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        for user in conn.get_users():
            if login == user[1] and password == user[2]:
                return redirect('/game-shop')
        return render_template('login.html', invalid='Password or login is invalid')

    return render_template('login.html', invalid='')

@app.route('/game-shop', methods=['POST', 'GET'])
def game_shop():

    all_colors: list[str] = [
        'null', 'rgb(255, 0, 0)', 'rgb(255, 60, 0)',
        'rgb(255, 140, 0)', 'rgb(255, 200, 0)', 'rgb(255, 255, 0)',
        'rgb(210, 255, 0)', 'rgb(180, 255, 0)', 'rgb(110, 255, 0)',
        'rgb(0, 255, 0)', 'rgb(150, 50, 200)'
        ]

    if request.method == 'POST':
        game_title = request.form.get('game_title')
        game_description = request.form.get('game_description')
        game_rating = request.form.get('rating')
        genre_id = request.form.get('choose_genre')

        genre_title = request.form.get('genre_title')
        genre_description = request.form.get('genre_description')

        if game_title != None:
            conn.create_game(
                game_title,
                game_description,
                game_rating,
                genre_id
            )

            redirect('/game-shop')
        if genre_title != None:
            conn.create_genre(genre_title, genre_description)
            redirect('/game-shop')

    all_genres = conn.get_genres()
    all_games = conn.get_games()
    return render_template('shop.html', games=all_games, genres=all_genres, all_colors=all_colors, range=range)

if __name__ == "__main__":
    app.run(port=8080, debug=True)