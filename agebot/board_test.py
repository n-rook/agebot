import unittest
from . import board

class BoardTest(unittest.TestCase):

  def test_get_revenue(self):
    tableau = board.Tableau({board.agriculture: 3})
    self.assertEqual(tableau.getRevenue(board.Point.FOOD), 3)

  def test_building_equality(self):
    def makeIron():
      return board.Building(
        'Iron',
        'Mine',
        5,
        {board.Point.RESOURCES, 2},
        0,
        0)

    self.assertEqual(makeIron(), makeIron())
    self.assertEqual(hash(makeIron()), hash(makeIron()))
