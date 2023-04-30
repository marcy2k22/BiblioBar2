from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

app = Flask(__name__, template_folder='templates')

# impostazione della chiave segreta per la sessione
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# funzione per controllare le credenziali
def CREDENZIALI(filename, username, password):
    with open(filename, 'r') as f:
        for line in f:
            # split the line into username and password
            line_parts = line.strip().split(',')
            if len(line_parts) == 2:
                file_username = line_parts[0]
                file_password = line_parts[1]

                # check if the username and password match
                if username == file_username and password == file_password:
                    return True

    # if no matching username and password were found, return False
    return False

@app.route('/about')
def about():
    return render_template('info.html')

@app.route('/')
def index():
    try:
        with open('book.txt', 'r') as f:
            books = f.readlines()
    except Exception as e:
        return f"Errore durante la lettura del file: {str(e)}"

    book_list = []
    for book in books:
        book_parts = book.strip().split(',')
        book_dict = {
            'title': book_parts[0],
            'author': book_parts[1],
            'isbn': book_parts[2],
            'cover': book_parts[3]
        }
        book_list.append(book_dict)

    return render_template('index.html', book_list=book_list, logged_in=session.get('logged_in'))

@app.route('/form')
def form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return render_template('form.html')

@app.route('/accesso')
def accesso():
    return render_template('accesso.html')



from flask import flash

@app.route('/check-login', methods=['POST'])
def check_login():
    # recupera i valori inseriti dall'utente
    username = request.form['username']
    password = request.form['password']

    # controlla le credenziali
    if CREDENZIALI('accessi.txt', username, password):
        # se le credenziali sono corrette, imposta la sessione dell'utente come autenticata
        session['logged_in'] = True
        # reindirizza l'utente alla pagina "form"
        return redirect(url_for('form'))
    else:
        # altrimenti, reindirizza l'utente alla pagina "accesso" e mostra un messaggio di errore
        flash('Credenziali non valide, riprova.')
        return redirect(url_for('accesso'))

from flask import jsonify, redirect, url_for

@app.route('/delete-book', methods=['POST'])
def delete_book():
    # recupera il titolo del libro da eliminare dal form
    title = request.form['title']

    # controlla se il file "book.txt" esiste
    if not os.path.isfile('book.txt'):
        message = "Errore: il file 'book.txt' non esiste."
        return jsonify({'message': message, 'redirect': url_for('form')})

    # legge i dati dei libri dal file "book.txt"
    with open('book.txt', 'r') as f:
        books = f.readlines()

    # cerca il libro da eliminare
    book_index = None
    for i, book in enumerate(books):
        book_parts = book.strip().split(',')
        if book_parts[0] == title:
            book_index = i
            break

    # se il libro è stato trovato, lo elimina dalla lista dei libri
    if book_index is not None:
        del books[book_index]

        # scrive la lista aggiornata dei libri nel file "book.txt"
        with open('book.txt', 'w') as f:
            f.writelines(books)

        # crea un messaggio di successo da mostrare in un alert
        message = f"Il libro '{title}' è stato eliminato."
        return jsonify({'message': message})
    else:
        # crea un messaggio di errore da mostrare in un alert
        message = f"Non è stato trovato nessun libro con il titolo '{title}'."
        return jsonify({'message': message, 'redirect': url_for('form')})
    
@app.route('/logout')
def logout():
    # rimuove la chiave 'logged_in' dalla sessione
    session.pop('logged_in', None)
    # reindirizza l'utente alla pagina principale
    return redirect(url_for('form')) #index

@app.route('/add-book', methods=['POST'])
def add_book():
    # recupera i valori inseriti dall'utente nel form
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    cover = request.form['cover']

    # scrive i dati del nuovo libro nel file "book.txt"
    with open('book.txt', 'a') as f:
        f.write(f"{title},{author},{isbn},{cover}\n")

    # reindirizza l'utente alla pagina principale
    return redirect(url_for('form'))

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)