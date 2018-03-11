"""Initializes the board state."""

from . import board, buildings

def initializeTableau():
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
