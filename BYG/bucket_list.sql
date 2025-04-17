DROP TABLE IF EXISTS bucket_list CASCADE;
DROP TABLE IF EXISTS user_bucket CASCADE;

CREATE TABLE bucket_list (
    bucket_id SERIAL PRIMARY KEY,
    item TEXT,
    contact TEXT,
    area TEXT,
    lat DOUBLE PRECISION,
    long DOUBLE PRECISION,
    descrip TEXT, 
    category TEXT,
    cloudinary_id TEXT,
    priv BOOLEAN DEFAULT FALSE
);

-- We can improve this logic later so no duplicate user_netids are made
CREATE TABLE user_bucket (
    id SERIAL PRIMARY KEY,
    user_netid VARCHAR NOT NULL,
    bucket_id INTEGER REFERENCES bucket_list(bucket_id),
    completed BOOLEAN DEFAULT FALSE
);

-- We can improve this logic later so we can linearize the items
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Ceramics Studio', '903-328-1390', 'New College West', NULL, NULL, 'Make clay pots.', 'creative', 'ceramic.jpg');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Climbing Wall', '721-675-8932', 'Dillon Gym', NULL, NULL, 'Scale the rock wall and see how you fare.', 'athletic', 'climbing');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Maker Space', '888-888-8888', 'Lewis Library', NULL, NULL, '3D-print and create what you can imagine.', 'creative', '3dprinter');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Princeton Tunnels', '609-555-1001', 'Campus', NULL, NULL, 'Explore the mysterious underground tunnels.', 'adventure', 'explore.jpg');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Graduate College Tower', '609-555-1002', NULL, NULL, 'Graduate College', 'Climb to the top for a great view.', 'historic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Rockefeller Tower', '609-555-1003' NULL, NULL, 'Rockefeller College', 'See campus from the Rocky tower.', 'historic', 'tower.jpg');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('PNI Monkey Lab', '609-555-1004', 'PNI', NULL, NULL, 'Tour the cognitive neuroscience facilities.', 'academic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Roma Theater Movie Night', '609-555-1005', NULL, NULL, 'Campus', 'Go to a movie night at the Roma.', 'social', 'movie.png');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Princeton Battlefield Tour', '609-555-1006', NULL, NULL, 'Princeton Battlefield', 'Visit the Revolutionary War site.', 'historic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Princeton Airport Flight Class', '609-555-1007', NULL, NULL, 'Princeton Airport', 'Take an introductory flying lesson.', 'adventure', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Danny DeVito Shrine', '609-555-1008', 'Mathey College', NULL, NULL, 'Visit the shrine of Danny DeVito.', 'quirky', 'danny.avif');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Grounds for Sculpture', '609-555-1010', 'Hamilton, NJ', NULL, NULL, 'Explore the outdoor sculpture museum.', 'artistic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Amish Farmers Market', '609-555-1011', 'Trenton Area', NULL, NULL, 'Eat and shop at the Amish market.', 'food', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Prospect 13', '609-555-1012', 'Prospect Ave', NULL, NULL, 'Discover what happens at Prospect 13.', 'social', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('PPPL', '609-555-1013', 'Plainsboro', NULL, NULL, 'Tour the Princeton Plasma Physics Lab.', 'academic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Poe field stargazing', '609-555-1014', 'Poe Field', NULL, NULL, 'Relax and stargaze under the open sky.', 'reflective', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Farminary', '609-555-1015', 'Route 206', NULL, NULL, 'Visit the farm run by the seminary.', 'sustainable', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Forbes Garden', '609-555-1016', 'Forbes College', NULL, NULL, 'Walk through the student-run garden.', 'nature', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Map room (Lewis basement)', '609-555-1017', 'Lewis Library', NULL, NULL, 'Explore rare maps in the basement.', 'academic', 'XXX');
INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
    VALUES ('Forbes Brunch', '609-555-1018', 'Forbes College', 'Have a fancy brunch at Forbes.', 'food', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Prospect 12', NULL, '', NULL, NULL, 'Drink an alcoholic drink at every eating club in one night', 'Social', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Visit the mae machine shop', NULL, '', NULL, NULL, 'Cool place to be, get to cut up some plastic or metal, and learn tools. Additional note: Probably need a MAE student to get in / use the machines', 'Academic', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Learn the wheel at the pottery studio', NULL, '', NULL, NULL, 'Sign up for a class and learn to throw clay at the student pottery studio. It is literally so fun and free.', 'Creative', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Fox Shrine', NULL, '', NULL, NULL, 'Find the fox shrine in Frist! Hint: it''s built into the wall in one of the hallways.', 'Adventurous', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Chill on Poe', NULL, '', NULL, NULL, 'When it''s warm out, get studio 34 vibes and no‐tech deep talks on Poe Field while stargazing', 'Social', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Explore Prospect Gardens', NULL, '', NULL, NULL, 'Just walk around the Prospect Gardens, take some pictures, bring friends.', 'Adventurous', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Princeton Garden Project', 'Elizabeth.kunze@princeton.edu', '', NULL, NULL, 'Volunteer with the Princeton Garden Project—people who work there are always welcoming.', 'Volunteer', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Visit the Danny DeVito Shrine', NULL, '', NULL, NULL, 'Find the hidden away Danny DeVito Shrine in the Slums (Frist basement).', 'Princetonia', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Roof Climbing', NULL, '', NULL, NULL, 'Climb all the roofs on campus (Forbes, Campus Club, Blair, etc).', 'Adventurous', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('NCW Ceramics Studio', NULL, '', NULL, NULL, 'Make and take home your own ceramic piece at the NCW studio!', 'Creative', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('FreeFood ListServ Day', NULL, '', NULL, NULL, 'Eat at every free‐food email from the ListServ in one day.', 'Princetonia', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Attend Christian Union Nova Encounter', '504-232-7518', '', NULL, NULL, 'Attend CU Nova Encounter to worship and learn about Christ among others.', 'Spiritual', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Intramural Sports', NULL, '', NULL, NULL, 'Join an intramural sport—even if you don’t know how to play, it’s a great time!', 'Athletic', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Go to the Ceramic Studio', NULL, '', NULL, NULL, 'Visit the ceramic studio and make something!', 'Creative', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Attend a Whig-Clio Senate Debate', NULL, '', NULL, NULL, 'Sit in on a Whig-Clio Senate debate to hear student government in action.', 'Social', 'XXX');

INSERT INTO bucket_list (item, contact, area, descrip, category, cloudinary_id)
VALUES ('Halloweekend', NULL, '', NULL, NULL, 'Participate in Halloweekend on Prospect Avenue.', 'Princetonia', 'XXX');
