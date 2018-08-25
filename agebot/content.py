"""Contains definitions of buildings, cards, and so on."""

from .board import BuildingTechnology, CardDistribution
from .buildings import *
from . import buildings

AGRICULTURE_CARD = BuildingTechnology(AGRICULTURE, 0)
BRONZE_CARD = BuildingTechnology(BRONZE, 0)
PHILOSOPHY_CARD = BuildingTechnology(PHILOSOPHY, 0)
RELIGION_CARD = BuildingTechnology(RELIGION, 0)

IRRIGATION_CARD = BuildingTechnology(IRRIGATION, 3)
IRON_CARD = BuildingTechnology(IRON, 5)
ALCHEMY_CARD = BuildingTechnology(ALCHEMY, 4)
THEOLOGY_CARD = BuildingTechnology(THEOLOGY, 2)
BREAD_AND_CIRCUSES_CARD = BuildingTechnology(BREAD_AND_CIRCUSES, 3)
PRINTING_PRESS_CARD = BuildingTechnology(PRINTING_PRESS, 3)
DRAMA_CARD = BuildingTechnology(DRAMA, 3)

SELECTIVE_BREEDING_CARD = BuildingTechnology(SELECTIVE_BREEDING, 5)
COAL_CARD = BuildingTechnology(COAL, 7)
SCIENTIFIC_METHOD_CARD = BuildingTechnology(SCIENTIFIC_METHOD, 6)
ORGANIZED_RELIGION_CARD = BuildingTechnology(ORGANIZED_RELIGION, 4)
TEAM_SPORTS_CARD = BuildingTechnology(TEAM_SPORTS, 5)
JOURNALISM_CARD = BuildingTechnology(JOURNALISM, 6)
OPERA_CARD = BuildingTechnology(OPERA, 7)

MECHANIZED_AGRICULTURE_CARD = BuildingTechnology(MECHANIZED_AGRICULTURE, 7)
OIL_CARD = BuildingTechnology(OIL, 9)
COMPUTERS_CARD = BuildingTechnology(COMPUTERS, 8)
PRO_SPORTS_CARD = BuildingTechnology(PRO_SPORTS, 7)
MULTIMEDIA_CARD = BuildingTechnology(MULTIMEDIA, 9)
MOVIES_CARD = BuildingTechnology(MOVIES, 10)

BUILDING_CARDS = tuple(b for b in globals().values() if isinstance(b, BuildingTechnology))

CIVIL_CARD_DISTRIBUTIONS = {
  AGRICULTURE_CARD: CardDistribution(0, 0, 0),
  IRRIGATION_CARD: CardDistribution(2, 2, 2),
  SELECTIVE_BREEDING_CARD: CardDistribution(1, 2, 3),
  MECHANIZED_AGRICULTURE_CARD: CardDistribution(1, 2, 2),

  BRONZE_CARD: CardDistribution(0, 0, 0),
  IRON_CARD: CardDistribution(2, 2, 3),
  COAL_CARD: CardDistribution(1, 2, 2),
  OIL_CARD: CardDistribution(1, 2, 2),

  PHILOSOPHY_CARD: CardDistribution(0, 0, 0),
  ALCHEMY_CARD: CardDistribution(2, 2, 3),
  SCIENTIFIC_METHOD_CARD: CardDistribution(2, 2, 2),
  COMPUTERS_CARD: CardDistribution(2, 2, 2),

  RELIGION_CARD: CardDistribution(0, 0, 0),
  THEOLOGY_CARD: CardDistribution(1, 2, 2),
  ORGANIZED_RELIGION_CARD: CardDistribution(2, 2, 2),

  BREAD_AND_CIRCUSES_CARD: CardDistribution(1, 2, 2),
  TEAM_SPORTS_CARD: CardDistribution(1, 1, 1),
  PRO_SPORTS_CARD: CardDistribution(1, 1, 2),

  PRINTING_PRESS_CARD: CardDistribution(2, 2, 2),
  JOURNALISM_CARD: CardDistribution(1, 2, 2),
  MULTIMEDIA_CARD: CardDistribution(2, 2, 2),

  DRAMA_CARD: CardDistribution(1, 2, 2),
  OPERA_CARD: CardDistribution(2, 2, 2),
  MOVIES_CARD: CardDistribution(2, 2, 2),
}
