-- tables
-- Table: book
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    authorID INT NOT NULL,
    genre TEXT NOT NULL,
    title TEXT NOT NULL
);

-- Table: bookCopies

CREATE TABLE IF NOT EXISTS bookCopies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	bookID INT NOT NULL,
    purchaseDate TEXT NOT NULL,
    purchasePrice TEXT NOT NULL
);

-- Table: loans

CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	bookCopiesID INT NOT NULL,
    memberID INT NOT NULL,
	checkoutDate TEXT,
	returnDate TEXT,
    reservationDate TEXT
);

-- Table: authors

CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	authorName TEXT NOT NULL
);

-- Table: recommendations

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    authorID INT NOT NULL,
    genre TEXT NOT NULL,
    title TEXT NOT NULL,
	purchasePrice TEXT NOT NULL
);