import unittest
from . import board, buildings

class BoardTest(unittest.TestCase):

  def test_get_revenue(self):
    tableau = board.Tableau({buildings.AGRICULTURE: 3})
    self.assertEqual(tableau.getRevenue(board.Point.FOOD), 3)
