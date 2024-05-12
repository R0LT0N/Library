import sqlite3

def create_table():
    #Создаем таблицу если её нету
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            genre TEXT NOT NULL
        )
    ''')
    conn.commit() 
    conn.close()

def add_book():
    #Добавление книги
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    description = input("Введите описание книги: ")

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT genre FROM books")
    genres = [row[0] for row in cursor.fetchall()]

    print("Доступные жанры:")
    for i, genre in enumerate(genres):
        print(f"{i+1}. {genre}")

    while True:
        choice = input("Выберите жанр из списка или введите новый: ")
        if choice.isdigit() and 1 <= int(choice) <= len(genres):
            genre = genres[int(choice) - 1]
            break
        else:
            genre = choice
            break

    cursor.execute("INSERT INTO books (title, author, description, genre) VALUES (?, ?, ?, ?)", 
                   (title, author, description, genre))
    conn.commit()
    conn.close()
    print("Книга успешно добавлена!")

def view_all_books():
    #Вывод всех книг
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author FROM books")
    books = cursor.fetchall()
    conn.close()

    if books:
        for book in books:
            print(f"{book[0]}. {book[1]} - {book[2]}")
    else:
        print("В библиотеке пока нет книг.")


def search_book():
    #Поиск книг по клбчевому слову
    keyword = input("Введите ключевое слово для поиска: ")
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author FROM books WHERE title LIKE ? OR author LIKE ?", 
                   ('%' + keyword + '%', '%' + keyword + '%'))
    books = cursor.fetchall()
    conn.close()

    if books:
        for book in books:
            print(f"{book[0]}. {book[1]} - {book[2]}")
    else:
        print("Книги по вашему запросу не найдены.")

def delete_book():
    #Удаление книги
    book_id = input("Введите ID книги для удаления: ")
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    print("Книга успешно удалена!")

def view_books_by_genre():
    #Вывод книг по жанру
    genre = input("Введите жанр: ")
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author FROM books WHERE genre = ?", (genre,))
    books = cursor.fetchall()
    conn.close()

    if books:
        for book in books:
            print(f"{book[0]}. {book[1]} - {book[2]}")
    else:
        print(f"Книг жанра '{genre}' не найдено.")


if __name__ == "__main__":
    create_table()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Просмотреть список книг")
        print("3. Поиск книги")
        print("4. Удалить книгу")
        print("5. Просмотреть книги по жанру")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_all_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            view_books_by_genre()
        elif choice == '0':
            break
        else:
            print("Неверный ввод.")