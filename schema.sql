CREATE TABLE users (username TEXT, password TEXT, role TEXT);
CREATE TABLE courses (id SERIAL PRIMARY KEY, name TEXT, professor TEXT, prerequisites INTEGER[]);
CREATE TABLE courselists (username TEXT, courses TEXT[]);