from csv import reader

def fill_database():
    file = open('books.csv')
    
    for line in reader(file):
        isbn, title, author, year = line

        # do database execute
        # db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {
        #     "isbn": isbn, "title": title, "author": author, "year": year
        # })

    # do database commit
    # db.commit()
