import unittest
from . import board

class BoardTest(unittest.TestCase):

  def test_get_revenue(self):
    tableau = board.Tableau({board.agriculture: 3})
    self.assertEqual(tableau.getRevenue(board.Point.FOOD), 3)
