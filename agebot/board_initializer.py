"""Initializes the board state."""

from . import board, buildings

def initializeTableau():
  starting_buildings = {
    buildings.AGRICULTURE: 2,
    buildings.BRONZE: 2,
    buildings.PHILOSOPHY: 1
  }

  return board.Tableau(
    board.DESPOTISM, starting_buildings)
