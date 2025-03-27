DROP TABLE IF EXISTS bucket_list;
DROP TABLE IF EXISTS users;

CREATE TABLE bucket_list (
    bucket_id SERIAL PRIMARY KEY,
    title TEXT,
    contact TEXT,
    area TEXT,
    descrip TEXT, 
    category TEXT,
    cloudinary_id TEXT
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT,
    email TEXT,
    major TEXT,
    class_year TEXT,
    descrip TEXT, 
    cloudinary_id TEXT,
    bucket_id TEXT
);

INSERT INTO bucket_list (title, contact, area, descrip, category, cloudinary_id)
    VALUES ('Ceramics Studio', '903-328-1390', 'New College West', 'Make clay pots.', 'Creative', 'XXX');
INSERT INTO bucket_list (title, contact, area, descrip, category, cloudinary_id)
    VALUES ('Climbing Wall', '721-675-8932', 'Dillon Gym', 'Scale the rock wall and see how you fare.', 'Athletic', 'XXX');
INSERT INTO bucket_list (title, contact, area, descrip, category, cloudinary_id)
    VALUES ('Maker Space', '888-888-8888', 'Lewis Library', '3D-print and create what you can imagine.', 'Creative', 'XXX');

