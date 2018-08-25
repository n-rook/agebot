"""Defines the play space."""

import enum
from collections import namedtuple, Counter
from frozendict import frozendict
from immutable import frozenbag

# As a proof of concept, let's start with a board consisting of only one
# building: Bronze. No corruption or food yet.

class IllegalActionException(Exception):
  """Thrown if a player tries to play an illegal action."""

class Board:
  """Represents the entire board, including all players' tableaux and the market row."""

  def __init__(self, round_number, turn_order, acting_player, card_row, tableaux):
    """Initializes the board.

    Args:
      round: Which round number it is. A round consists of everyone taking
        a turn.
      turn_order: The order in which players take their turns.
      acting_player: Whose turn it is.
      card_row: The card row.
      tableaux: A map from each player to their tableau.
    """
    self._round_number = round_number
    self._turn_order = turn_order
    self._acting_player = acting_player
    self._card_row = card_row
    self._tableaux = frozendict(tableaux)

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

  def __repr__(self):
    return 'Board({}, {}, {}, {})'.format(
      self._round_number, self._turn_order, self._acting_player, self._tableaux)

  def __str__(self):
    return ('--------\nRound {}\nPlayer {}\nTableaux:\n' +
      '\n'.join(['{}\n{}\n'.format(p, t) for (p, t) in self._tableaux.items()]))

  def __hash__(self):
    return hash((self._round_number, self._turn_order, self._acting_player, self._card_row, self._tableaux))

  def __eq__(self, other):
    return (isinstance(other, Board) and
      self._round_number == other._round_number and
      self._turn_order == other._turn_order and
      self._acting_player == other._acting_player and
      self._tableaux == other._tableaux)

  def tableau(self, player):
    """Returns a player's tableau."""
    return self._tableaux[player]

  def update_tableau(self, player, tableau):
    """Give a player a new tableau.

    This should only be used by tests.
    """

    new_tableaux = dict(self._tableaux)
    new_tableaux[player] = tableau
    return Board(self._round_number, self._turn_order, self._acting_player, self._card_row, new_tableaux)

  def legal_actions(self):
    """Returns legal actions for the acting player."""
    return self._tableaux[self._acting_player].legal_actions()

  def play_action_phase(self, actions):
    """Plays and resolves the action phase and end of turn for a player.

    Args:
      actions: A list of Actions to take.
    Returns:
      A new Board.
    """
    theBoard = self
    for a in actions:
      theBoard = theBoard._play_action(a)

    return theBoard.resolve_end_of_turn_sequence()

  def _play_action(self, action):
    new_tableau = self._tableaux[self._acting_player].play_action(action)
    new_tableaux = dict(self._tableaux)
    new_tableaux[self._acting_player] = new_tableau

    return Board(
      self._round_number,
      self._turn_order,
      self._acting_player,
      self._card_row,
      new_tableaux)

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
      self._card_row,
      new_tableaux)

  def resolve_start_of_turn(self, options):
    """Resolves the beginning of a turn.

    Args:
      options: SimulatorOptions
    Returns:
      A Board representing the action phase of the next turn.
    """
    replenish_results = self._card_row.shift_left().replenish(options)

    # Resolve the end of an age.
    if replenish_results.new_age is not None:
      new_tableaux = {p: t.antiquate() for (p, t) in self._tableaux.items()}
    else:
      new_tableaux = dict(self._tableaux)

    # Resolve a war.
    # Make exclusive tactics available.

    return Board(
      self._round_number,
      self._turn_order,
      self._acting_player,
      replenish_results.card_row,
      new_tableaux
    )

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
    self._buildings = frozendict(buildings)
    self._building_technologies = frozenset(building_technologies)

    if points is None:
      points = {}
    self._points = _fill_out_points(points)

    if civil_actions is None:
      self._civil_actions = self.max_civil_actions
    else:
      self._civil_actions = civil_actions

  def __str__(self):
    return 'Tableau\n{}\n{}'.format(
      self._government.name,
      self._building_map_str()
    )

  def __eq__(self, other):
    return (isinstance(other, Tableau) and
      self._government == other._government and
      self._buildings == other._buildings and
      self._building_technologies == other._building_technologies)

  def _building_map_str(self):
    return 'Built:\n' + '\n'.join(['  ' + b.name for b in self._buildings]) + '\n'

  def _tech_str(self):
    return 'Discovered:\n' + '\n'.join(['  ' + t.name for t in self._building_technologies]) + '\n'

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

  def legal_actions(self):
    """Returns a set of all legal actions for this tableau."""

    # Soon, we will need the market row passed in here.
    return frozenset(self.legal_build_actions())

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
      if action.building.urban and self.num_buildings_in_category(action.building.category) >= self._government.urban_buildings:
        return False
    else:
      raise NotImplementedError('Unknown action type {}'.format(action))

    return True

  def play_action(self, action):
    """Plays an action and returns an updated tableau.

    Args:
      action: The action to play.
    Throws:
      IllegalActionException if we aren't allowed to play this action.
    """
    if (not self.is_action_legal(action)):
      raise IllegalActionException('Cannot play action: {}'.format(action))

    new_points = dict(self._points)
    for point in Point:
      new_points[point] -= action.get_price(point)

    if isinstance(action, BuildAction):
      new_buildings = dict(self._buildings)
      if (action.building in new_buildings):
        new_buildings[action.building] += 1
      else:
        new_buildings[action.building] = 1

      return Tableau(
        self._government,
        new_buildings,
        self._building_technologies,
        new_points)
    else:
      raise NotImplementedError(str(action))

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

  def antiquate(self, new_age):
    """Upon the dawn of a new age, discard old held cards."""
    # Not yet implemented
    return self

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

def _fill_out_points(pointDictionary):
  """Returns a dictionary with 0 of each absent type of point.

  Note that if the incoming dictionary is all filled out already, this returns
  the original point dictionary.
  """
  returnDictionary = pointDictionary
  for point in Point:
    if point not in returnDictionary:
      returnDictionary = dict(returnDictionary)
      returnDictionary[point] = 0

  for point in returnDictionary:
    if not isinstance(point, Point):
      raise TypeError('Huh? ', point)
  return returnDictionary

class Age(enum.Enum):
  """Through the Ages consists of four ages. These are they."""
  ANCIENT = 0
  ONE = 1
  TWO = 2
  THREE = 3
  FOUR = 4

  def next_age(self):
    if self == Age.FOUR:
      raise RuntimeError('No age after Age IV!')
    return {
      Age.ANCIENT: Age.ONE,
      Age.ONE: Age.TWO,
      Age.TWO: Age.THREE,
      Age.THREE: Age.FOUR
    }[self]

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
  def name(self):
    return self._name

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

CARD_ROW_PRICES = (5, 4, 4)
"""The number of cards at each price point in the card row.

The first CARD_ROW_PRICES[0] cards cost 1 civil actions to take, the next
CARD_ROW_PRICES[1] take 2, etc.
"""
TOTAL_CARDS_IN_CARD_ROW = sum(CARD_ROW_PRICES)
"""The total number of cards in the card row."""

EMPTY_CARD_SLOT = object()
"""This singleton object represents an empty card slot."""

class CardRow:
  """The card row containing all civil cards."""

  def __init__(self, card_row, civil_decks, player_count):
    """Initializes the CardRow.

    Args:
      card_row: A tuple containing the cards in the card row. This must have
        a length of precisely 14. If a slot has no card in it, it contains
        EMPTY_CARD_SLOT instead.
      civil_decks: A CivilDecks representing the remaining cards.
      player_count: The number of players. This determines how many cards are
        replaced at the beginning of each turn.
    """
    if len(card_row) != TOTAL_CARDS_IN_CARD_ROW:
      raise ValueError('Card row has {} cards'.format(len(card_row)))

    self._card_row = card_row
    self._civil_decks = civil_decks
    self._player_count = player_count

  @property
  def cards_discarded_per_turn(self):
    return {2: 4, 3: 3, 4: 2}[self._player_count]

  def get_price(self, card_index):
    price = 1
    for i in CARD_ROW_PRICES:
      if i > card_index:
        return price
      card_index -= i
    raise ValueError('Invalid price {}')

  def pick_card(self, card_index):
    """Take a card from the card row.

    Returns a CardRowPickResult containing both the card picked and the
    new card row after the card picked is gone.
    """
    card = self._card_row[card_index]
    if card == EMPTY_CARD_SLOT:
      raise ValueError('No card at index {}'.format(card_index))

    new_card_row = list(self._card_row)
    new_card_row[card_index] = EMPTY_CARD_SLOT
    return CardRowPickResult(
      card,
      CardRow(tuple(new_card_row), self._civil_decks, self._player_count))

  def shift_left(self):
    """Discard the leftmost cards, and shift all other cards to the left."""

    new_card_row = list(self._card_row)
    for i in range(self.cards_discarded_per_turn):
      new_card_row[i] = EMPTY_CARD_SLOT

    new_cards = []
    for card in self._card_row[self.cards_discarded_per_turn:]:
      new_cards.append(card)
    while len(new_cards) < TOTAL_CARDS_IN_CARD_ROW:
      new_cards.append(EMPTY_CARD_SLOT)
    return CardRow(tuple(new_cards), self._civil_decks, self._player_count)

  def replenish(self, options):
    """Restore all empty slot cards."""

    empty_card_slots = [i for (i, c) in self._card_row if c == EMPTY_CARD_SLOT]
    if len(empty_card_slots) == 0:
      return self

    draw_result = self._civil_decks.draw(len(empty_card_slots), options)
    new_card_row = list(self._card_row)
    for (i, new_card) in zip(empty_card_slots, draw_result.cards):
      new_card_row[i] = new_card
    return ReplenishResult(
      CardRow(
        tuple(new_card_row),
        draw_result.civil_decks,
        self._player_count),
      draw_result.new_age)

class ReplenishResult(namedtuple('ReplenishResult', ['card_row', 'new_age'])):
  """The results of replenishing the card row.

  Fields:
  card_row: The updated card row.
  new_age: If a new age has begun, that age.
  """

class CardRowPickResult(namedtuple('CardRowPickResult', ['card', 'row'])):
  """The result of picking a card."""

class CivilDecks:
  """A collection of civil decks.

  In real life, a deck of cards is in a certain order hidden to players.
  Here, it is represented as a bag of cards, from which one is picked at
  random.
  """

  def __init__(self, deck_dicts):
    """Construct a CivilDecks instance.

    Args:
      deck_dicts: A mapping from ages to a frozenbag of the cards remaining
        in the deck for that age.
    """
    self._deck_dicts = frozendict(deck_dicts)

  def draw(self, num_cards, options):
    """Draw a number of cards. Returns a DrawResult."""
    age_to_draw_from = self._earliest_age_with_cards()

    if age_to_draw_from is None:
      # No cards left! Do nothing.
      return DrawResult(tuple(), self, None)

    deck_to_draw_from = self._deck_dicts[age_to_draw_from]
    cards_drawn = options.rng.pick_cards(num_cards, deck_to_draw_from)

    if len(cards_drawn) < num_cards and age_to_draw_from != Age.FOUR:
      next_age = age_to_draw_from.next_age()
      next_age_deck = self._deck_dicts[next_age]

      next_age_cards = options.rng.pick_cards(
        num_cards - len(cards_drawn), next_age_deck)

      new_decks = dict(self._deck_dicts)
      new_decks[age_to_draw_from] = cards_drawn.deck
      new_decks[next_age] = next_age_cards.deck

      return DrawResult(
        cards_drawn.cards + next_age_cards.cards,
        CivilDecks(new_decks))
    else:
      new_decks = dict(self._deck_dicts)
      new_decks[age_to_draw_from] = cards_drawn.deck
      return DrawResult(cards_drawn, CivilDecks(new_decks))

  def _earliest_age_with_cards(self):
    for age in Age:
      if self._deck_dicts[age]:
        return age
    return None

class DrawResult(namedtuple('DrawResult', ['cards', 'civil_decks', 'new_age'])):
  """Represents the outcome of drawing cards.

  Fields:
    cards: A tuple of the cards drawn.
    civil_decks: The new state of the civil decks.
    new_age: If set, the cards returned have caused a new age to dawn
      upon your glorious civilization!
  """


class CivilCard:
  """A card."""

  def __init__(self, name, age):
    """Create a new type of civil card.

    Args:
      name: The card's name, as a string.
      age: The age in which the card arrives.
    """
    self._name = name
    self._age = age

  @property
  def name(self):
    return self._name

  @property
  def age(self):
    return self._age

  def __str__(self):
    return self._name

class Technology(CivilCard):
  """A type of card purchased with science."""

  def __init__(self, name, age, price):
    """Initializes a Technology.

    Args:
      name: The technology's name.
      age: Which Age the technology appears in.
      price: An int representing how much science the techonology costs.
    """
    super().__init__(name, age)
    self._price = price

class BuildingTechnology(Technology):
  """A type of civil card which grants access to a building."""

  def __init__(self, building, price):
    super().__init__(building.name, building.age, price)
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
    self._price = _fill_out_points(price)

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

class CardDistribution(namedtuple('CardDistribution', ['two', 'three', 'four'])):
  """How many of a given card there are in the deck."""

  def withPlayers(self, number):
    try:
      return {2: self.two, 3: self.three, 4: self.four}[number]
    except KeyError:
      raise ValueError('Invalid number {}'.format(number))
