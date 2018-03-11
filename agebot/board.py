"""Defines the play space."""

import enum
from collections import namedtuple, Counter

# As a proof of concept, let's start with a board consisting of only one
# building: Bronze. No corruption or food yet.


class Board:
  """Represents the entire board, including all players' tableaux and the market row."""

  def __init__(self, acting_player):
    """Initializes the board."""
    self._market_row = "Moses"
    self._acting_player = acting_player

class Player(enum.Enum):
  """Represents a player."""
  ONE = 1
  TWO = 2

  def other(self):
    return {
      Player.TWO: Player.ONE,
      Player.ONE: Player.TWO
    }[self]

class Tableau:
  """An individual player's set of buildings and resources."""

  def __init__(self, buildings):
    # Building ID -> number of buildings
    self._buildings = buildings

  def getRevenue(self, point):
    return sum((c * b.getIncome(point) for (b, c) in self._buildings.items()))

class Point(enum.Enum):
  """Represents a type of resource gained each turn.

  Points are resources which can be gained or lost based on per-turn income.
  For example, FOOD is a Point, since your people eat food each turn (so
  you lose food), but they grow food too. SCIENCE is a Point, too, but
  military strength is not, because there aren't effects which give you more
  military strength each turn.
  """
  FOOD = 1
  RESOURCES = 2
  SCIENCE = 3
  CULTURE = 4

class Age(enum.Enum):
  """Through the Ages consists of four ages. These are they."""
  ANCIENT = 0
  ONE = 1
  TWO = 2
  THREE = 3
  FOUR = 4
