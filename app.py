import db
from flask import Flask, abort, url_for
from converters import RegexConverter, ListConverter

app =Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.url_map.converters['list'] = ListConverter

@app.route('/')
def index():
    html = ['<ul>']
    for username, user in db.users.items():
        html.append(
            f"<li><a href='{url_for('user', username=username)}'>{user['name']}</a></li>"
        )
    html.append('</ul>')
    return '\n'.join(html)

def profile(username):
    user = db.users.get(username)

    if user:
        return f"""
            <h1>{user['name']}</h1></br>
            <h2>{user['age']}</h2></br>
            <h3>{user['tel']}</h3></br>
            <a href="/">Voltar</a>
        """
    else:
        return abort(404, "User not found")
# Como não utilizamos o @app.route para a view profile, utilizamos o add_url_rule
app.add_url_rule('/user/<username>/', view_func=profile, endpoint='user')

@app.route('/user/<username>/<int:quote_id>/')
# Utilizando conversor de URL - no caso, um 'int'
def quote(username, quote_id):
    user = db.users.get(username, {})
    quote = user.get('quotes').get(quote_id)

    if user and quote:
        return f"""
            <h1>{user['name']}</h1></br>
            <p>
                <q>{ quote }</q>
            </p>
            <a href="/">Voltar</a>
        """
    else:
        return abort(404, "User or quote not found")

# Utilizando conversor de URL - no caso, um 'path', ou seja,
# ele identifica um caminho de arquivo como um todo
@app.route('/file/<path:filename>/')
def file_path(filename):
    return f"Argumento recebido: { filename }"

# Utilizando conversor de URL customizado, no caso
# ele aceita qualquer nome que seja iniciado pela letra 'a'
@app.route('/reg/<regex("a.*"):name>/')
def reg(name):
    return f"Argumento iniciado com a letra 'a': { name }"

# Utilizando conversor de URL customizado, no caso
# ele aceita qualquer nome que seja iniciado pela letra 'b'
@app.route('/reg/<regex("b.*"):name>/')
def reg_b(name):
    return f"Argumento iniciado com a letra 'b': { name }"

# Utilizando conversor de URL customizado, no caso
# ele aceita qualquer lista de nomes divididos pelo sinal '+'
@app.route('/list/<list:names>/')
def list(names):
    html = ''
    for name in set(names):
        user = db.users.get(name)
        if user:
            html += f"""
                <h1>{user['name']}</h1></br>
                <h2>{user['age']}</h2></br>
                <h3>{user['tel']}</h3></br>
                "<a href="/">Voltar</a>"
                <hr />
            """
    return html or abort(404, "Users not found")

if __name__ == '__main__':
    app.run(use_reloader=True)
