"""Initializes the board state."""

from . import board, buildings, content, immutable

def initial_civil_deck(age, player_count):
  """Given an age, returns the cards for that age."""

  return immutable.frozenbag({
    c: d.withPlayers(player_count) for (c, d) in content.CIVIL_CARD_DISTRIBUTIONS
    if c.age == age
  })

def initialize_tableau():
  starting_buildings = {
    buildings.AGRICULTURE: 2,
    buildings.BRONZE: 2,
    buildings.PHILOSOPHY: 1
  }

  starting_technologies = [
    content.AGRICULTURE_CARD,
    content.BRONZE_CARD,
    content.PHILOSOPHY_CARD,
    content.RELIGION_CARD
  ]

  return board.Tableau(
    board.DESPOTISM, starting_buildings, starting_technologies)

def initialize_board():
  """Initialize the board for a two-player game."""
  player_order = [board.Player.ONE, board.Player.TWO]
  tableaux = {p: initialize_tableau() for p in player_order}

  return board.Board(
    1,
    player_order,
    player_order[0],
    tableaux)
