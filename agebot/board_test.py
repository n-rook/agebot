import unittest
from . import board

class BoardTest(unittest.TestCase):

  def test_moses(self):
    someBoard = board.Board()
    self.assertEqual(someBoard._market_row, 'Moses')
