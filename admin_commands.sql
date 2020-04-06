CREATE USER david WITH LOGIN PASSWORD "ng3po2si"; /* creating a new employee */
CREATE USER david WITH LOGIN PASSWORD "ng3po2si" VALID UNTIL '2020-08-30'; /* create an intern account */

CREATE ROLE admin WITH CREATEDB CREATEROLE;
GRANT admin TO andrew;
GRANT SELECT, UPDATE, INSERT ON employee TO GROUP admin;
