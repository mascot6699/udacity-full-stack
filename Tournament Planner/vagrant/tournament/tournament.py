#!/usr/bin/env python
"""
tournament.py -- implementation of a Swiss-system tournament
"""

import psycopg2

DBNAME = "tournament"

def connect(dbname=DBNAME):
    """
    Connect to the PostgreSQL database.
    :returns: a database connection.
    """
    try:
        return psycopg2.connect("dbname=" + DBNAME)
    except:
        print("Connection failed")


def fetch_data(SQL, data=None):
    """
    :param SQL: The SQL query to fetch data
    :return:
    """
    db = connect()
    c = db.cursor()
    if data == None:
        c.execute(SQL)
    else:
        c.execute(SQL, data)
    result = c.fetchall()
    db.close()
    return result



def commit_data(SQL, data=None):
    """
    :param SQL: The SQL query to commit
    :return:
    """
    db = connect()
    c = db.cursor()
    if data == None:
        c.execute(SQL)
    else:
        c.execute(SQL, data)
    db.commit()
    db.close()


def deleteMatches():
    """
    Remove all the match records from the database.
    """
    commit_data("DELETE FROM matches;")


def deletePlayers():
    """
    Remove all the player records from the database.
    """
    commit_data("DELETE FROM players;")


def countPlayers():
    """
    Returns the number of players currently registered.
    """
    query = "SELECT COUNT(id) from players;"
    result = fetch_data(query)
    return int(result[0][0]) # as result is in the format [(0L,)]


def registerPlayer(name):
    """
    Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES (%s)"
    data = (name,)
    commit_data(query, data)


def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    winners_query = "select players.id, name, count(matches.id) as wins from players left join matches on " \
                    "players.id = winner_id group by players.id order by wins desc"

    losers_query = "select players.id, count(matches.id) as losses from players left join matches on " \
                   "players.id = loser_id group by players.id order by losses desc"

    join_query = "select winners.id, winners.name, wins, wins+losses as matches from ({winners_query}) as winners left " \
                 "join ({losers_query}) as losers on winners.id = losers.id;".format(
        winners_query=winners_query, losers_query=losers_query)

    # I attempted to solve the possible SQL inject here but since there is no input used from user SQL injection is
    # not possible. Please correct me if I am wrong.
    # join_query = "select winners.id, winners.name, wins, wins+losses as matches from (%s) as winners left join (%s) " \
    #              "as losers on winners.id = losers.id;"
    # data = (winners_query, losers_query)
    # db = connect()
    # c = db.cursor()
    # c.execute(join_query, data)
    # results = c.fetchall()
    # db.close()

    return fetch_data(join_query)


def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "insert into matches (winner_id, loser_id) values ((%s), (%s))"
    data = (winner,loser)
    commit_data(query, data)


def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
  
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

    Raise:
      Error when number of player is less than 2 or not multiple of 2

    Scope:
      Implement bye feature (might require database change)
    """
    results = []

    standings = [(record[0], record[1]) for record in playerStandings()]
    # since only ID and names are required

    if len(standings) < 2:
        raise KeyError("Not enough players.")
    if len(standings) % 2:
        raise KeyError("Current implementation requires even number of players.")

    # Run a for loop from index zero to number of players in ranking skipping one index each time
    for player_rank in range(0, len(standings), 2):
        # appending the player at index player_rank and the next one as pairs
        results.append(standings[player_rank] + standings[player_rank + 1])
    return results


