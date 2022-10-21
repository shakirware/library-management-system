



INSERT INTO book (authorid, genre, title)
VALUES ('2', 'fiction', 'football book');


INSERT INTO bookCopies (bookid, purchaseDate, purchasePrice)
VALUES(last_insert_rowid(), '2020/05/13', '2022/06/34');