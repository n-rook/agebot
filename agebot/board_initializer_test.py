import unittest
from .board import Point
from . import board_initializer, buildings

class BoardInitializerTest(unittest.TestCase):

  def test_initialize_tableau(self):
    t = board_initializer.initialize_tableau()
    self.assertEqual(t.revenue(Point.FOOD), 2)
    self.assertEqual(t.revenue(Point.RESOURCES), 2)
    self.assertEqual(t.revenue(Point.SCIENCE), 1)
    self.assertEqual(t.revenue(Point.CULTURE), 0)
    self.assertEqual(t.max_civil_actions, 4)
    self.assertCountEqual(t.known_buildings,
      [buildings.AGRICULTURE, buildings.BRONZE,
       buildings.PHILOSOPHY, buildings.RELIGION])
