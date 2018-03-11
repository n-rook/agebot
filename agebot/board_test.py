import unittest
from .board import Player, Point, Tableau
from . import board, buildings, board_initializer

class BoardTest(unittest.TestCase):

  def test_revenue(self):
    tableau = Tableau(
      board.DESPOTISM, {buildings.AGRICULTURE: 3}, [])
    self.assertEqual(tableau.revenue(board.Point.FOOD), 3)

  def test_end_of_turn(self):
    testing_board = board_initializer.initialize_board()
    end_of_turn = testing_board.resolve_end_of_turn_sequence()

    self.assertEqual(end_of_turn.round, 1)
    self.assertEqual(end_of_turn.acting_player, Player.TWO)

    updated_tableau = end_of_turn.tableau(Player.ONE)
    self.assertEqual(updated_tableau.points(Point.FOOD), 2)
    self.assertEqual(updated_tableau.points(Point.RESOURCES), 2)
    self.assertEqual(updated_tableau.points(Point.SCIENCE), 1)
    self.assertEqual(updated_tableau.points(Point.CULTURE), 0)

  def test_build_actions(self):
    testing_board = board_initializer.initialize_board()
    testing_board = testing_board.update_tableau(
      Player.ONE,
      testing_board.tableau(Player.ONE).add_points({Point.RESOURCES: 2}))

    available_actions = testing_board.tableau(Player.ONE).legal_build_actions()
    self.assertCountEqual(
      available_actions,
      {
        board.BuildAction(buildings.AGRICULTURE),
        board.BuildAction(buildings.BRONZE)
      })
