"""Defines the play space."""

import enum
from collections import namedtuple, Counter

# As a proof of concept, let's start with a board consisting of only one
# building: Bronze. No corruption or food yet.

def _hashDict(d):
  """Returns a hash value for a dictionary.

  Be aware that this hash value will change if the dictionary changes. In other
  words, if you use this function to calculate the hash of a mutable object,
  your life will become hard.
  """
  return hash(frozenset(d))

class Board:
  """Represents the entire board, including all players' tableaux and the market row."""

  def __init__(self):
    self._market_row = "Moses"

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

class Building:
  """Represents a type of building."""

  def __init__(self, name, category, price, income, happiness, strength):
    """Defines a new building type.

    Args:
      name: The name of the building.
      category: The category of the building. This defines which buildings can upgrade
        into which. For example, Agriculture and Irrigation are both 'Farm', so
        you can upgrade Agriculture buildings into Farm buildings.
      price: The resources required to buy this building.
      income: The points granted by this building each turn.
      happiness: How much happiness is gained from this building.
      strength: How much military strength is gained from this building.
    """
    self._name = name
    self._category = category
    self._price = price
    self._income = income
    self._happiness = happiness
    self._strength = strength
    self._hash = None

  def getIncome(self, point):
    if point in self._income:
      return self._income[point]
    else:
      return 0

  def __eq__(self, other):
    if not isinstance(other, Building):
      return False
    return (self._name == other._name
      and self._category == other._category
      and self._price == other._price
      and self._income == other._income
      and self._happiness == other._happiness
      and self._strength == other._strength)

  def __hash__(self):
    if self._hash:
      return self._hash
    return hash((
      self._name,
      self._category,
      self._price,
      _hashDict(self._income),
      self._happiness,
      self._strength
    ))

agriculture = Building(
  'Agriculture',
  'Farm',
  2,
  {Point.FOOD: 1},
  0,
  0
)
