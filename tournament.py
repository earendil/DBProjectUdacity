#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    db = connect()
    dbc = db.cursor()
    dbc.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""

    db = connect()
    dbc = db.cursor()
    dbc.execute("DELETE FROM players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""

    db = connect()
    dbc = db.cursor()
    dbc.execute("SELECT COUNT(*) FROM players;")
    data = dbc.fetchall()
    db.close()
    return data[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    dbc = db.cursor()
    dbc.execute("INSERT INTO players (id, name) VALUES (DEFAULT, %s);", (name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    dbc = db.cursor()
    dbc.execute("""
        select id, name, count(matches.winner) as wins, matches1
        from (
            select players.id as id, players.name as name, count(matches.*) as matches1
            from players
            left outer join matches
            on players.id in (matches.player1, matches.player2)
            group by players.id
        ) as temp
        left join matches
        on temp.id = matches.winner
        group by id, name, matches1
        order by wins desc;
    """)
    data = dbc.fetchall()
    db.close()
    return data

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    dbc = db.cursor()
    dbc.execute("INSERT INTO matches (player1, player2, winner) VALUES (%s, %s, %s);", (winner, loser, winner))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    [(6, 'luca', 0L, 0L), (5, 'uca', 0L, 0L), (3, 'cas', 0L, 0L), (2, 'lu', 0L, 0L), (1, 'lucas', 0L, 0L), (4, 'ls', 0L, 0L)]

    current_status = playerStandings()

    nextRound = []

    for i, _ in enumerate(current_status):
        if i % 2 == 0:
            nextRound.append((current_status[i][0],current_status[i][1],
                              current_status[i + 1][0], current_status[i + 1][1]))

    return nextRound

if __name__ == "__main__":

    # registerPlayer("lucas")
    # registerPlayer("lu")
    # registerPlayer("cas")
    # registerPlayer("ls")
    # registerPlayer("uca")
    # registerPlayer("luca")
    print playerStandings()
    print swissPairings()
