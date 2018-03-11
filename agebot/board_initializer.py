"""Initializes the board state."""

from . import board, buildings

def initialize_tableau():
  starting_buildings = {
    buildings.AGRICULTURE: 2,
    buildings.BRONZE: 2,
    buildings.PHILOSOPHY: 1
  }

  starting_technologies = [
    buildings.AGRICULTURE_CARD,
    buildings.BRONZE_CARD,
    buildings.PHILOSOPHY_CARD,
    buildings.RELIGION_CARD
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
