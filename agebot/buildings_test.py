import unittest
from . import board, buildings

class BuildingsTest(unittest.TestCase):

  def test_building_equality(self):
    def makeIron():
      return buildings.Building(
        'Iron',
        'Mine',
        5,
        {board.Point.RESOURCES: 2},
        board.Age.ONE)

    self.assertEqual(makeIron(), makeIron())
    self.assertEqual(hash(makeIron()), hash(makeIron()))

  def test_no_duplicate_age_buildings(self):
    for b in buildings.BUILDINGS:
      duplicates = [o for o in buildings.BUILDINGS
                    if (b.age, b.category) == (o.age, o.category)]
      self.assertEqual(duplicates, [b])
