"""Contains classes which make it easy to modify resolution options."""

from .immutable import frozenbag
from collections import namedtuple
from typing import NamedTuple


class PickCardsResult(namedtuple('PickCardsResult', ['cards', 'deck'])):
  """The result of calling pickCards."""

class ConsoleLogger:
  """Logs to the console."""

  def replenish_civil_cards(self, cards):
    print('Drew {} from the civil deck.'.format(', '.join(card.name for card in cards)))

class ActualRng:
  """Actually resolves outcomes using pseudorandom numbers."""

  def __init__(self, random):
    self._random = random

  def pick_cards(self, count, mapping) -> PickCardsResult:
    """Draws cards from a set.

    If count is greater than the number of cards in mapping, this just returns all
    the cards in mapping (in a random order).

    Args:
      count: The number of cards to take.
      mapping: A mapping from cards to the number of that card type in the deck.
        No zeroes allowed.
    Returns:
      The cards picked, and a frozenbag containing the remaining cards in the deck.
    """
    cards = []
    remainder = dict(mapping)
    for _ in range(count):
      if not mapping:
        return PickCardsResult(cards, frozenbag(remainder))
      cards.append(self._pick_card(remainder))

    return PickCardsResult(cards, frozenbag(remainder))


  def _pick_card(self, mapping):
    """Pick a card. Edit mapping in place. Return card picked."""
    if not mapping:
      raise RuntimeError('bug')
    card = self._random.choices(mapping, mapping)
    mapping[card] -= 1
    if (mapping[card] == 0):
      del mapping[card]
    return card

class SimulatorOptions(NamedTuple):
  """Represents options which modify how parts of the game are resolved."""
  logger: ConsoleLogger
  rng: ActualRng
