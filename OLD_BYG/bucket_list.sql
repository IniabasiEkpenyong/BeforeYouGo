DROP TABLE IF EXISTS bucket_list;

CREATE TABLE bucket_list (
    isbn TEXT PRIMARY KEY, 
    title TEXT, 
    category TEXT
);

INSERT INTO bucket_list (isbn, title, category)
    VALUES ('123', 'Ceramics Studio', 'creative');
INSERT INTO bucket_list (isbn, title, category)
    VALUES ('234', 'Climbing Wall', 'athletic');
INSERT INTO bucket_list (isbn, title, category)
    VALUES ('345', 'Maker Space', 'creative');
