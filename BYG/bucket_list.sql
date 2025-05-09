DROP TABLE IF EXISTS bucket_list CASCADE;
DROP TABLE IF EXISTS user_bucket CASCADE;
DROP TABLE IF EXISTS subtasks CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS ratings CASCADE;

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
    priv BOOLEAN DEFAULT FALSE,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR NOT NULL
);

CREATE TABLE user_bucket (
    id SERIAL PRIMARY KEY,
    user_netid VARCHAR NOT NULL,
    bucket_id INTEGER REFERENCES bucket_list(bucket_id),
    completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE subtasks (
    id SERIAL PRIMARY KEY,
    user_bucket_id INTEGER NOT NULL REFERENCES user_bucket(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    bucket_id INTEGER NOT NULL REFERENCES bucket_list(bucket_id) ON DELETE CASCADE,
    user_netid VARCHAR NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    bucket_id INTEGER NOT NULL REFERENCES bucket_list(bucket_id) ON DELETE CASCADE,
    user_netid VARCHAR NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (bucket_id, user_netid)  -- Ensures one rating per user per bucket item
);


CREATE INDEX idx_subtasks_user_bucket_id ON subtasks(user_bucket_id);
CREATE INDEX idx_ratings_bucket_id ON ratings(bucket_id);

-- We can improve this logic later so we can linearize adding items
INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Ceramics Studio', NULL, 'New College West', 40.3422959650295, -74.65496351594201, 'Make clay pots.', 'Creative', 'ceramic.jpg', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Climbing Wall', NULL, 'Princeton Stadium', 40.34580906239536, -74.65000148021971, 'Scale the rock wall and see how you fare.', 'Sports', 'climbing', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Maker Space', NULL, 'Lewis Library', 40.34661008276812, -74.65258909200425, '3D-print and create what you can imagine.', 'Creative', '3dprinter', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Princeton Tunnels', NULL, 'Campus', 40.34886232734069, -74.6593445312841, 'Explore the mysterious underground tunnels.', 'Adventure', 'explore.jpg', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Graduate College Tower', NULL, 'Graduate College', 40.340862645767565, -74.66442614477758, 'Climb to the top for a great view.', 'Adventure', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Rockefeller Tower', NULL, 'Rockefeller College', 40.34860783791797, -74.66206518525743, 'See campus from the Rocky tower.', 'Other', 'tower.jpg', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('PNI Monkey Lab', NULL, 'PNI', 40.343480083733574, -74.65249748035964, 'Tour the cognitive neuroscience facilities.', 'Academic', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Roma Theater Movie Night', NULL, 'Rockefeller College', 40.3487999889968, -74.6621349226885, 'Go to a movie night at the Roma.', 'Event', 'movie.png', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Princeton Battlefield Tour', NULL, 'Princeton Battlefield', 40.33102075322586, -74.67671911779128, 'Visit the Revolutionary War site.', 'Adventure', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Princeton Airport Flight Class', NULL, 'Princeton Airport', 40.39757271507362, -74.66030562758498, 'Take an introductory flying lesson.', 'Adventure', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Danny DeVito Shrine', NULL, 'Frist Campus Center', 40.346796147653855, -74.65514601594192, 'Visit the shrine of Danny DeVito.', 'Other', 'danny.avif', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Grounds for Sculpture', NULL, 'Hamilton, NJ', 40.23695376032633, -74.71875739200733, 'Explore the outdoor sculpture museum.', 'Creative', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Amish Farmers Market', NULL, 'Trenton Area', 40.38777817707781, -74.60158420538576, 'Eat and shop at the Amish market.', 'Food', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('PPPL', '609-555-1013', NULL, 40.35074928704113, -74.6028651932533, 'Tour the Princeton Plasma Physics Lab.', 'Academic', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv, status, created_by) 
VALUES ('Poe field stargazing', NULL, 'Poe Field', 40.34364531909187, -74.6550066803598, 'Relax and stargaze under the open sky.', 'Other', 'XXX', FALSE, 'approved', 'admin');

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Farminary', NULL, 'Princeton Theological Seminary', 40.314165536365984, -74.69098698841175, 'Visit the farm run by the seminary.', 'Other', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Forbes Garden', NULL, 'Forbes College', 40.343982596131625, -74.66204687305132, 'Walk through the student-run garden.', 'Other', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Map room (Lewis basement)', NULL, 'Lewis Library', 40.346507900161235, -74.65268028465572, 'Explore rare maps in the basement.', 'Academic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Forbes Brunch', NULL, 'Forbes College', 40.34252120818171, -74.6605163042652, 'Have a fancy brunch at Forbes.', 'Food', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Prospect 12', NULL, 'Prospect Avenue', 40.34783912958914, -74.65494075205785, 'Have a drink at every eating club in one night', 'Event', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Visit the mae machine shop', NULL, 'MAE Machine Shop', 40.371482484022906, -74.64962559558104, 'Cool place to be, get to cut up some plastic or metal, and learn tools.', 'Academic', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Fox Shrine', NULL, 'Frist Campus Center', 40.34691882930069, -74.65515674232783, 'Find the fox shrine in Frist!', 'Adventure', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Explore Prospect Gardens', NULL, 'Prospect Gardens', 40.34740098859358, -74.65658412698363, 'Walk around the Prospect Gardens.', 'Adventure', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Roof Climbing', NULL, 'Forbes, Campus Club, Blair, etc.', 40.3476469329182, -74.66201667116395, 'Climb all the roofs on campus.', 'Adventure', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Rise Up Singing', NULL, 'Murray Dodge', 40.348311604728885, -74.65772145770458, 'Sing Folk Songs for a Memorable Evening', 'Music', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('FreeFood ListServ Day', NULL, 'Princeton University', 40.34782447967274, -74.6541785079345, 'Eat at every free‐food email from the ListServ in one day.', 'Food', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Intramural Sports', NULL, 'Dillon Gym', 40.346487599279996, -74.65923883442704, 'Join an intramural sport—even if you don’t know how.', 'Sports', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Attend a Whig-Clio Senate Debate', NULL, 'Whig Hall', 40.348240832900885, -74.65825880426206, 'Sit in on a Whig-Clio Senate debate.', 'Event', 'XXX', FALSE);

INSERT INTO bucket_list (item, contact, area, lat, lng, descrip, category, cloudinary_id, priv) 
VALUES ('Halloweekend', NULL, 'Prospect Avenue', 440.34783912958914, -74.65494075205785, 'Participate in Halloweekend on Prospect.', 'Event', 'XXX', FALSE);
