"""Contains kinds of buildings."""

from .board import Point, Age, BuildingTechnology

class Building:
  """Represents a type of building."""

  def __init__(self, name, category, price, income, age, happiness=0, strength=0):
    """Defines a new building type.

    Args:
      name: The name of the building.
      category: The category of the building. This defines which buildings can upgrade
        into which. For example, Agriculture and Irrigation are both 'Farm', so
        you can upgrade Agriculture buildings into Farm buildings.
      price: The resources required to buy this building.
      income: The points granted by this building each turn.
      age: The Age of the building (A, I, II, III, or IV)
      happiness: How much happiness is gained from this building.
      strength: How much military strength is gained from this building.
    """
    self._name = name
    self._category = category
    self._price = price
    self._income = income
    self._happiness = happiness
    self._strength = strength
    self._age = age
    self._hash = None

  @property
  def category(self):
    return self._category

  @property
  def age(self):
    return self._age

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
      and self._strength == other._strength
      and self._age == other._age)

  def __hash__(self):
    if self._hash:
      return self._hash
    return hash((
      self._name,
      self._category,
      self._price,
      _hashDict(self._income),
      self._happiness,
      self._strength,
      self._age
    ))

def _hashDict(d):
  """Returns a hash value for a dictionary.

  Be aware that this hash value will change if the dictionary changes. In other
  words, if you use this function to calculate the hash of a mutable object,
  your life will become hard.
  """
  return hash(frozenset(d))

# Farms

AGRICULTURE = Building(
  'Agriculture',
  'Farm',
  2,
  {Point.FOOD: 1},
  Age.ANCIENT
)

IRRIGATION = Building(
  'Irrigation',
  'Farm',
  4,
  {Point.FOOD: 2},
  Age.ONE
)

SELECTIVE_BREEDING = Building(
  'Selective Breeding',
  'Farm',
  6,
  {Point.FOOD: 3},
  Age.TWO
)

MECHANIZED_AGRICULTURE = Building(
  'Mechanized Agriculture',
  'Farm',
  8,
  {Point.FOOD: 5},
  Age.THREE
)

BRONZE = Building(
  'Bronze',
  'Mine',
  2,
  {Point.RESOURCES: 1},
  Age.ANCIENT
)

IRON = Building(
  'Iron',
  'Mine',
  5,
  {Point.RESOURCES: 2},
  Age.ONE
)

COAL = Building(
  'Coal',
  'Mine',
  8,
  {Point.RESOURCES: 3},
  Age.TWO
)

OIL = Building(
  'Oil',
  'Mine',
  11,
  {Point.RESOURCES: 5},
  Age.THREE
)

PHILOSOPHY = Building(
  'Philosophy',
  'Lab',
  3,
  {Point.SCIENCE: 1},
  Age.ANCIENT
)

ALCHEMY = Building(
  'Alchemy',
  'Lab',
  6,
  {Point.SCIENCE: 2},
  Age.ONE
)

SCIENTIFIC_METHOD = Building(
  'Scientific Method',
  'Lab',
  8,
  {Point.SCIENCE: 3},
  Age.TWO
)

COMPUTERS = Building(
  'Computers',
  'Lab',
  11,
  {Point.SCIENCE: 5},
  Age.THREE
)

RELIGION = Building(
  'Religion',
  'Temple',
  3,
  {Point.CULTURE: 1},
  Age.ANCIENT,
  happiness=1
)

THEOLOGY = Building(
  'Theology',
  'Temple',
  5,
  {Point.CULTURE: 1},
  Age.ONE,
  happiness=2
)

ORGANIZED_RELIGION = Building(
  'Organized Religion',
  'Temple',
  3,
  {Point.CULTURE: 1},
  Age.TWO,
  happiness=1
)

BREAD_AND_CIRCUSES = Building(
  'Bread and Circuses',
  'Arena',
  3,
  {},
  Age.ONE,
  happiness=2,
  strength=1
)

TEAM_SPORTS = Building(
  'Team Sports',
  'Arena',
  5,
  {},
  Age.TWO,
  happiness=3,
  strength=2
)

PRO_SPORTS = Building(
  'Professional Sports',
  'Arena',
  8,
  {},
  Age.THREE,
  happiness=4,
  strength=3
)

PRINTING_PRESS = Building(
  'Printing Press',
  'Library',
  3,
  {Point.CULTURE: 1, Point.SCIENCE: 1},
  Age.ONE
)

JOURNALISM = Building(
  'Journalism',
  'Library',
  8,
  {Point.CULTURE: 2, Point.SCIENCE: 2},
  Age.TWO
)

MULTIMEDIA = Building(
  'Multimedia',
  'Library',
  11,
  {Point.CULTURE: 3, Point.SCIENCE: 3},
  Age.THREE
)

DRAMA = Building(
  'Drama',
  'Theater',
  4,
  {Point.CULTURE: 2},
  Age.ONE,
  happiness=1
)

OPERA = Building(
  'Opera',
  'Theater',
  8,
  {Point.CULTURE: 3},
  Age.TWO,
  happiness=1
)

MOVIES = Building(
  'Movies',
  'Theater',
  11,
  {Point.CULTURE: 4},
  Age.THREE,
  happiness=1
)

BUILDINGS = tuple(b for b in globals().values() if isinstance(b, Building))

AGRICULTURE_CARD = BuildingTechnology(AGRICULTURE)
BRONZE_CARD = BuildingTechnology(BRONZE)
PHILOSOPHY_CARD = BuildingTechnology(PHILOSOPHY)
RELIGION_CARD = BuildingTechnology(RELIGION)
