--Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.


CREATE TABLE players  ( id serial primary key,
                        name varchar (25) not null,
                        created_at timestamp default current_timestamp );

CREATE TABLE matches  ( id serial primary key,
                        winner_id int,
                        loser_id int,
                        foreign key (winner_id) references players(id),
                        foreign key (loser_id) references players(id) );

-- lists the table creted
\d
-- quits the screen
\q