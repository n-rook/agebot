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

  def __init__(self, government, buildings, civil_actions=None):
    """Creates a new Tableau.

    Args:
      government: The current government.
      building: A map from Buildings to the number of that kind of building you have.
      civil_actions: The number of civil actions you currently have available of
        this type. If left empty, this is set to the maximum number of civil actions
        you have.
    """
    self._government = government
    self._buildings = buildings
    self._civil_actions = civil_actions

  @property
  def max_civil_actions(self):
    return self._government.civil_actions

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

class Government:
  """A player's current government."""

  def __init__(self, name, age, civil_actions, military_actions, urban_buildings,
               income=None, happiness=0, strength=0):
    """Define a new form of government."""
    self._name = name
    self._age = age
    self._civil_actions = civil_actions
    self._military_actions = military_actions
    self._urban_buildings = urban_buildings
    self._income = income or {}
    self._happiness = happiness
    self._strength = strength

  @property
  def civil_actions(self):
    return self._civil_actions

  def __eq__(self, other):
    return (isinstance(other, Government) and
            self._name == other._name)

  def __hash__(self):
    return hash(self._name)

DESPOTISM = Government('Despotism', Age.ANCIENT, 4, 2, 3)
