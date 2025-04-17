DROP TABLE IF EXISTS bucket_list CASCADE;
DROP TABLE IF EXISTS user_bucket CASCADE;

CREATE TABLE bucket_list (
    bucket_id SERIAL PRIMARY KEY,
    item TEXT,
    contact TEXT,
    area TEXT,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
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
INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Ceramics Studio', '903-328-1390', 'New College West', 40.3422959650295, -74.65496351594201, 'Make clay pots.', 'creative', 'ceramic.jpg', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Climbing Wall', '721-675-8932', 'Princeton Stadium', 40.34580906239536, -74.65000148021971, 'Scale the rock wall and see how you fare.', 'athletic', 'climbing', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Maker Space', '888-888-8888', 'Lewis Library', 40.34661008276812, -74.65258909200425, '3D-print and create what you can imagine.', 'creative', '3dprinter', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Princeton Tunnels', '609-555-1001', 'Campus', 40.34886232734069, -74.6593445312841, 'Explore the mysterious underground tunnels.', 'adventure', 'explore.jpg', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Graduate College Tower', '609-555-1002', 'Graduate College', 40.340862645767565, -74.66442614477758, 'Climb to the top for a great view.', 'historic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Rockefeller Tower', '609-555-1003', 'Rockefeller College', 40.34860783791797, -74.66206518525743, 'See campus from the Rocky tower.', 'historic', 'tower.jpg', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('PNI Monkey Lab', '609-555-1004', 'PNI', 40.343480083733574, -74.65249748035964, 'Tour the cognitive neuroscience facilities.', 'academic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Roma Theater Movie Night', '609-555-1005', 'Rockefeller College', 40.3487999889968, -74.6621349226885, 'Go to a movie night at the Roma.', 'social', 'movie.png', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Princeton Battlefield Tour', '609-555-1006', 'Princeton Battlefield', 40.33102075322586, -74.67671911779128, 'Visit the Revolutionary War site.', 'historic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Princeton Airport Flight Class', '609-555-1007', 'Princeton Airport', 40.39757271507362, -74.66030562758498, 'Take an introductory flying lesson.', 'adventure', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Danny DeVito Shrine', '609-555-1008', 'Frist Campus Center', 40.346796147653855, -74.65514601594192, 'Visit the shrine of Danny DeVito.', 'quirky', 'danny.avif', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Grounds for Sculpture', '609-555-1010', 'Hamilton, NJ', 40.23695376032633, -74.71875739200733, 'Explore the outdoor sculpture museum.', 'artistic', 'XXX', FALSE);
/*
INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Amish Farmers Market', '609-555-1011', 'Trenton Area', 40.2171, -74.7429, 'Eat and shop at the Amish market.', 'food', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Prospect 13', '609-555-1012', 'Prospect Ave', 40.3470, -74.6540, 'Discover what happens at Prospect 13.', 'social', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('PPPL', '609-555-1013', 'Plainsboro', 40.3506, -74.5987, 'Tour the Princeton Plasma Physics Lab.', 'academic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Poe field stargazing', '609-555-1014', 'Poe Field', 40.3424, -74.6565, 'Relax and stargaze under the open sky.', 'reflective', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Farminary', '609-555-1015', 'Route 206', 40.3253, -74.6835, 'Visit the farm run by the seminary.', 'sustainable', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Forbes Garden', '609-555-1016', 'Forbes College', 40.3441, -74.6602, 'Walk through the student-run garden.', 'nature', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Map room (Lewis basement)', '609-555-1017', 'Lewis Library', 40.3503, -74.6523, 'Explore rare maps in the basement.', 'academic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Forbes Brunch', '609-555-1018', 'Forbes College', 40.3441, -74.6602, 'Have a fancy brunch at Forbes.', 'food', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Prospect 12', NULL, 'Prospect Avenue', 40.3463, -74.6540, 'Drink an alcoholic drink at every eating club in one night', 'Social', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Visit the mae machine shop', NULL, 'MAE Machine Shop', NULL, NULL, 'Cool place to be, get to cut up some plastic or metal, and learn tools.', 'Academic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Learn the wheel at the pottery studio', NULL, 'New College West', 40.3444, -74.6577, 'Sign up for a class and learn to throw clay.', 'Creative', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Fox Shrine', NULL, 'Frist Campus Center', 40.3480, -74.6585, 'Find the fox shrine in Frist!', 'Adventurous', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Chill on Poe', NULL, 'Poe Field', 40.3424, -74.6565, 'Get studio 34 vibes and no‐tech deep talks.', 'Social', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Explore Prospect Gardens', NULL, 'Prospect Gardens', 40.3463, -74.6560, 'Walk around the Prospect Gardens.', 'Adventurous', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Princeton Garden Project', 'Elizabeth.kunze@princeton.edu', 'Princeton Garden', NULL, NULL, 'Volunteer with the Princeton Garden Project.', 'Volunteer', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Visit the Danny DeVito Shrine', NULL, 'Frist basement', 40.3480, -74.6585, 'Find the hidden away Danny DeVito Shrine.', 'Princetonia', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Roof Climbing', NULL, 'Forbes, Campus Club, Blair, etc.', NULL, NULL, 'Climb all the roofs on campus.', 'Adventurous', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('NCW Ceramics Studio', NULL, 'New College West', 40.3444, -74.6577, 'Make and take home your own ceramic piece!', 'Creative', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('FreeFood ListServ Day', NULL, 'Princeton University', 40.3431, -74.6551, 'Eat at every free‐food email from the ListServ in one day.', 'Princetonia', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Attend Christian Union Nova Encounter', '504-232-7518', 'Princeton University', 40.3431, -74.6551, 'Attend CU Nova Encounter to worship and learn.', 'Spiritual', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Intramural Sports', NULL, 'Dillon Gym', 40.3445, -74.6554, 'Join an intramural sport—even if you don’t know how.', 'Athletic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Go to the Ceramic Studio', NULL, 'New College West', 40.3444, -74.6577, 'Visit the ceramic studio and make something!', 'Creative', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Attend a Whig-Clio Senate Debate', NULL, 'Whig Hall', 40.3484, -74.6593, 'Sit in on a Whig-Clio Senate debate.', 'Social', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Halloweekend', NULL, 'Prospect Avenue', 40.3463, -74.6540, 'Participate in Halloweekend on Prospect.', 'Princetonia', 'XXX', FALSE);
*/