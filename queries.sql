-- SQL quiries for User Model 

-- Create User 
INSERT INTO user (email, name,password)
VALUES ('sunil@gmail.com', 'Sunil Nepali','sunil123');

-- Get User 
SELECT * FROM user;


-- Queries for Book

-- insert 
INSERT INTO library_book (title, isbn, published_date, genre) 
VALUES ('Atomic Habit', '9781234567890', '2022-01-30', 'fiction');

-- get 
SELECT * FROM library_book;

-- update 
UPDATE library_book SET title = 'RIch Dad Poor Dad' WHERE id = 1;



-- SQL Queries for BookDetail
-- insert 
INSERT INTO library_bookdetails (book_id, number_of_pages, publisher, language)
VALUES (1, 300, 'Penguin Books', 'English');


-- get 
SELECT * FROM library_bookdetails;

-- update 
UPDATE library_bookdetails SET number_of_pages = 350 WHERE id = 1;




-- SQL Queries for Borrowed
-- insert 
INSERT INTO library_borrowedbooks (user_id, book_id)
VALUES (1, 1);

-- get 
SELECT * FROM library_borrowedbooks;

-- update 
DELETE FROM library_bookdetails WHERE id = 1;
