"""Defines the play space."""

import enum
from collections import namedtuple, Counter

# As a proof of concept, let's start with a board consisting of only one
# building: Bronze. No corruption or food yet.


class Board:
  """Represents the entire board, including all players' tableaux and the market row."""

  def __init__(self, round_number, turn_order, acting_player, tableaux):
    """Initializes the board.

    Args:
      round: Which round number it is. A round consists of everyone taking
        a turn.
      turn_order: The order in which players take their turns.
      acting_player: Whose turn it is.
      tableaux: A map from each player to their tableau.
    """
    self._round_number = round_number
    self._turn_order = turn_order
    self._acting_player = acting_player
    self._tableaux = tableaux

  @property
  def round(self):
    return self._round_number

  @property
  def turn_order(self):
    return self._turn_order

  @property
  def acting_player(self):
    return self._acting_player

  @property
  def tableaux(self):
    return self._tableaux

  def tableau(self, player):
    return self._tableaux[player]

  def update_tableau(self, player, tableau):
    """Give a player a new tableau.

    This should only be used by tests.
    """

    new_tableaux = dict(self._tableaux)
    new_tableaux[player] = tableau
    return Board(self._round_number, self._turn_order, self._acting_player, new_tableaux)

  def resolve_end_of_turn_sequence(self):
    """Resolves the end of a turn and moves onto the next turn.

    Returns:
      A Board representing the beginning of the next turn.
    """
    updated_tableau = self._tableaux[self._acting_player]

    # Discard excess military cards

    # Check for an uprising

    # Score science and culture
    updated_tableau = updated_tableau.score_science_and_culture()

    # Check for corruption

    # Gain food
    updated_tableau = updated_tableau.gain_food()

    # Consume food

    # Gain resources
    updated_tableau = updated_tableau.gain_resources()

    # Draw new military cards

    # Reset your actions
    updated_tableau = updated_tableau.reset_actions()

    turn_index = self._turn_order.index(self._acting_player)
    if turn_index == len(self._turn_order) - 1:
      new_round = self._round_number + 1
      next_player = self._turn_order[0]
    else:
      new_round = self._round_number
      next_player = self._turn_order[turn_index + 1]

    new_tableaux = dict(self._tableaux)
    new_tableaux[self._acting_player] = updated_tableau

    return Board(
      new_round,
      self._turn_order,
      next_player,
      new_tableaux)


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

  def __init__(self, government, buildings, building_technologies, points=None, civil_actions=None):
    """Creates a new Tableau.

    Args:
      government: The current government.
      building: A map from Buildings to the number of that kind of building you have.
      building_technologies: A sequence of BuildingTechnology cards representing the
        buildings you know about.
      points: A map from Point types to the number of each type you have.
      civil_actions: The number of civil actions you currently have available of
        this type. If left empty, this is set to the maximum number of civil actions
        you have.
    """
    self._government = government
    self._buildings = buildings
    self._building_technologies = frozenset(building_technologies)

    if points is None:
      points = {}
    self._points = _fillOutPoints(points)

    if civil_actions is None:
      self._civil_actions = self.max_civil_actions
    else:
      self._civil_actions = civil_actions

  def points(self, point):
    return self._points[point]

  @property
  def civil_actions(self):
    return self._civil_actions

  @property
  def max_civil_actions(self):
    return self._government.civil_actions

  def num_buildings(self, building):
    if (building not in self._buildings):
      return 0
    return self._buildings[building]

  def num_buildings_in_category(self, category):
    """Returns the number of buildings we have in a given category."""

    return sum(c for (b, c) in self._buildings.items()
               if b.category == category)

  @property
  def known_buildings(self):
    """The buildings this player knows about.

    Buildings might still show up here even if you can't build them right now:
    say, because they're too expensive, or because you hit your urban building
    maximum for this building type.
    """
    return tuple(t.building for t in self._building_technologies)

  def legal_build_actions(self):
    """Returns a set of all legal build actions."""
    candidate_actions = [BuildAction(b) for b in self.known_buildings]
    return frozenset(filter(self.is_action_legal, candidate_actions))

  def is_action_legal(self, action):
    """Returns whether or not an action can legally be taken.

    This does NOT check if the action is totally made up. For instance, you
    could pass in a BuildAction that builds an expensive building, but with
    the wrong cost.
    """

    # Before doing per-action checks, check the basic prices.
    if (self._civil_actions < action.civil_cost):
      return False
    if any(action.get_price(p) > self.points(p) for p in Point):
      return False

    if isinstance(action, BuildAction):
      if action.building not in self.known_buildings:
        return False
      # Check urban building limit
      if self.num_buildings_in_category(action.building.category) >= self._government.urban_buildings:
        return False
    else:
      raise NotImplementedError('Unknown action type {}'.format(action))

    return True

  def revenue(self, point):
    return sum((c * b.getIncome(point) for (b, c) in self._buildings.items()))

  def add_points(self, points):
    """Add some number of points."""
    new_points = dict(self._points)
    for (point, number) in points.items():
      new_points[point] += number
    return Tableau(
      self._government,
      self._buildings,
      self._building_technologies,
      points=new_points,
      civil_actions=self._civil_actions)

  def score_science_and_culture(self):
    """Returns this tableau updated with more science and culture."""
    return self._gain_points([Point.SCIENCE, Point.CULTURE])

  def gain_food(self):
    """Returns this tableau with more food."""
    return self._gain_point(Point.FOOD)

  def gain_resources(self):
    """Returns this tableau having gained its resources revenue."""
    return self._gain_point(Point.RESOURCES)

  def _gain_point(self, point):
    return self._gain_points([point])

  def _gain_points(self, points):
    return self.add_points({p: self.revenue(p) for p in points})

  def reset_actions(self):
    """Resets the number of available civil and military actions."""
    return Tableau(
      self._government,
      self._buildings,
      self._building_technologies,
      points=self._points,
      civil_actions=self.max_civil_actions)

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

def _fillOutPoints(pointDictionary):
  """Returns a dictionary with 0 of each absent type of point.

  Note that if the incoming dictionary is all filled out already, this returns
  the original point dictionary.
  """
  returnDictionary = pointDictionary
  for point in Point:
    if point not in returnDictionary:
      returnDictionary = dict(returnDictionary)
      returnDictionary[point] = 0
  return returnDictionary

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

  @property
  def urban_buildings(self):
    """The maximum number of one category of urban buildings you can have."""
    return self._urban_buildings

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

class Action:
  """A type of action to be taken on a turn."""

  def __init__(self, civil_cost, military_cost, price):
    """Creates a new Action. Only call on subclasses.

    Args:
      civil_cost: The number of civil actions this takes.
      military_cost: The number of military actions this takes.
      price: A map from Point types to the price of the card.
    """
    self._civil_cost = civil_cost
    self._military_cost = military_cost
    self._price = _fillOutPoints(price)

  @property
  def civil_cost(self):
    return self._civil_cost

  @property
  def military_cost(self):
    return self._military_cost

  def get_price(self, point):
    return self._price[point]

class BuildAction(Action):
  """An action to build a brand-new building."""

  def __init__(self, building):
    super().__init__(1, 0, {Point.RESOURCES: building.price})
    self._building = building

  @property
  def building(self):
    return self._building

  def __eq__(self, other):
    return (isinstance(other, BuildAction) and
            self._building == other._building)

  def __hash__(self):
    return hash(self._building)
