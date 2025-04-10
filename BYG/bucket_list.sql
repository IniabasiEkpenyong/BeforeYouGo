DROP TABLE IF EXISTS bucket_list;
DROP TABLE IF EXISTS users;

CREATE TABLE bucket_list (
    bucket_id SERIAL PRIMARY KEY,
    item TEXT,
    contact TEXT,
    area TEXT,
    descrip TEXT, 
    category TEXT,
    cloudinary_id TEXT
);


CREATE TABLE user_bucket (
    id SERIAL PRIMARY KEY,
    user_netid VARCHAR NOT NULL,
    bucket_id INTEGER REFERENCES bucket_list(bucket_id),
    completed BOOLEAN DEFAULT FALSE
);

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Ceramics Studio', '903-328-1390', 'New College West', 'Make clay pots.', 'creative', 'ceramic.jpg');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Climbing Wall', '721-675-8932', 'Dillon Gym', 'Scale the rock wall and see how you fare.', 'athletic', 'climbing');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Maker Space', '888-888-8888', 'Lewis Library', '3D-print and create what you can imagine.', 'creative', '3dprinter');



INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Princeton Tunnels', '609-555-1001', 'Campus', 'Explore the mysterious underground tunnels.', 'adventure', 'explore.jpg');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Graduate College Tower', '609-555-1002', 'Graduate College', 'Climb to the top for a great view.', 'historic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Rockefeller Tower', '609-555-1003', 'Rockefeller College', 'See campus from the Rocky tower.', 'historic', 'tower.jpg');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('PNI Monkey Lab', '609-555-1004', 'PNI', 'Tour the cognitive neuroscience facilities.', 'academic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Roma Theater Movie Night', '609-555-1005', 'Campus', 'Go to a movie night at the Roma.', 'social', 'movie.png');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Princeton Battlefield Tour', '609-555-1006', 'Princeton Battlefield', 'Visit the Revolutionary War site.', 'historic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Princeton Airport Flight Class', '609-555-1007', 'Princeton Airport', 'Take an introductory flying lesson.', 'adventure', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Danny DeVito Shrine', '609-555-1008', 'Mathey College', 'Visit the shrine of Danny DeVito.', 'quirky', 'danny.avif');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Grounds for Sculpture', '609-555-1010', 'Hamilton, NJ', 'Explore the outdoor sculpture museum.', 'artistic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Amish Farmers Market', '609-555-1011', 'Trenton Area', 'Eat and shop at the Amish market.', 'food', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Prospect 13', '609-555-1012', 'Prospect Ave', 'Discover what happens at Prospect 13.', 'social', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('PPPL', '609-555-1013', 'Plainsboro', 'Tour the Princeton Plasma Physics Lab.', 'academic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Poe field stargazing', '609-555-1014', 'Poe Field', 'Relax and stargaze under the open sky.', 'reflective', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Farminary', '609-555-1015', 'Route 206', 'Visit the farm run by the seminary.', 'sustainable', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Forbes Garden', '609-555-1016', 'Forbes College', 'Walk through the student-run garden.', 'nature', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Map room (Lewis basement)', '609-555-1017', 'Lewis Library', 'Explore rare maps in the basement.', 'academic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Forbes Brunch', '609-555-1018', 'Forbes College', 'Have a fancy brunch at Forbes.', 'food', 'XXX');
