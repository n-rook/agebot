import unittest
from .board import Point
from . import board_initializer, buildings

class BoardInitializerTest(unittest.TestCase):

  def test_initialize_tableau(self):
    t = board_initializer.initializeTableau()
    self.assertEqual(t.getRevenue(Point.FOOD), 2)
    self.assertEqual(t.getRevenue(Point.RESOURCES), 2)
    self.assertEqual(t.getRevenue(Point.SCIENCE), 1)
    self.assertEqual(t.getRevenue(Point.CULTURE), 0)
    self.assertEqual(t.max_civil_actions, 4)
    self.assertCountEqual(t.known_buildings,
      [buildings.AGRICULTURE, buildings.BRONZE,
       buildings.PHILOSOPHY, buildings.RELIGION])
