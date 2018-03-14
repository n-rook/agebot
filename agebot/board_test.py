import unittest
from .board import Player, Point, Tableau
from . import board, buildings, board_initializer, content

def give_free_stuff(board, points):
  return board.update_tableau(
    board.acting_player,
    board.tableau(board.acting_player).add_points(points))

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

  def test_build_actions_available(self):
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

  def test_conduct_build_actions(self):
    testing_board = give_free_stuff(
      board_initializer.initialize_board(),
      {Point.RESOURCES: 4})

    available_actions = testing_board.legal_actions()
    build_farm = next(
      a for a in available_actions
      if isinstance(a, board.BuildAction) and a.building == buildings.AGRICULTURE)

    new_board = testing_board.play_action_phase([build_farm, build_farm])
    self.assertEqual(new_board.acting_player, Player.TWO)
    new_tableau = new_board.tableau(Player.ONE)
    self.assertEqual(new_tableau.num_buildings(buildings.AGRICULTURE), 4)
    self.assertEqual(new_tableau.points(Point.FOOD), 4)
    self.assertEqual(new_tableau.points(Point.RESOURCES), 2)

  def test_eq_maintained_with_identical_outcomes(self):
    testing_board = give_free_stuff(
      board_initializer.initialize_board(),
      {Point.RESOURCES: 4})

    available_actions = testing_board.legal_actions()
    build_farm = next(
      a for a in available_actions
      if isinstance(a, board.BuildAction) and a.building == buildings.AGRICULTURE)
    build_mine = next(
      a for a in available_actions
      if isinstance(a, board.BuildAction) and a.building == buildings.BRONZE)
    board1 = testing_board.play_action_phase([build_farm, build_mine])
    board2 = testing_board.play_action_phase([build_mine, build_farm])
    self.assertEqual(board1, board2)

  def test_card_distributions(self):
    selectiveBreedingDistribution = (
      content.CIVIL_CARD_DISTRIBUTIONS[content.SELECTIVE_BREEDING_CARD])
    self.assertEqual(
      selectiveBreedingDistribution,
      board.CardDistribution(1, 2, 3))

    self.assertEqual(selectiveBreedingDistribution.two, 1)
    self.assertEqual(selectiveBreedingDistribution.three, 2)
    self.assertEqual(selectiveBreedingDistribution.four, 3)

    self.assertEqual(selectiveBreedingDistribution.withPlayers(2), 1)
    self.assertEqual(selectiveBreedingDistribution.withPlayers(3), 2)
    self.assertEqual(selectiveBreedingDistribution.withPlayers(4), 3)
