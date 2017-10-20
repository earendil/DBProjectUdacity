-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament

CREATE TABLE players(id serial primary key, name text not null);

CREATE TABLE matches(player1 serial references players(ID),
                     player2 serial references players(ID),
                     winner int
                     constraint single_match check (player1 != player2),
                     primary key(player1, player2));
