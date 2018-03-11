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

  def __init__(self, government, buildings, building_technologies, civil_actions=None):
    """Creates a new Tableau.

    Args:
      government: The current government.
      building: A map from Buildings to the number of that kind of building you have.
      building_technologies: A sequence of BuildingTechnology cards representing the
        buildings you know about.
      civil_actions: The number of civil actions you currently have available of
        this type. If left empty, this is set to the maximum number of civil actions
        you have.
    """
    self._government = government
    self._buildings = buildings
    self._building_technologies = frozenset(building_technologies)
    if civil_actions is None:
      self._civil_actions = self.max_civil_actions
    else:
      self._civil_actions = civil_actions

  @property
  def max_civil_actions(self):
    return self._government.civil_actions

  @property
  def known_buildings(self):
    """The buildings this player knows about.

    Buildings might still show up here even if you can't build them right now:
    say, because they're too expensive, or because you hit your urban building
    maximum for this building type.
    """
    return tuple(t.building for t in self._building_technologies)

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

class BuildingTechnology:
  """A type of civil card which grants access to a building."""

  def __init__(self, building):
    self._building = building

  @property
  def building(self):
    return self._building

  def __eq__(self, other):
    return (isinstance(other, BuildingTechnology) and
            self._building == other._building)

  def __hash__(self):
    return hash(self._building)
