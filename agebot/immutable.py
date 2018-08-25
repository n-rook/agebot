"""Immutable collections."""

from collections import abc
from frozendict import frozendict

class frozenbag(abc.Mapping):
  """A frozen multiset (or "bag")."""

  def __init__(self, mapping):
    if (isinstance(mapping, frozenbag)):
      self._dict = mapping._dict
    else:
      self._dict = frozendict({k: c for (k, c) in mapping.items
                              if c > 0})


  def __eq__(self, other):
    return (
      isinstance(other, frozenbag) and
      self._dict == other._dict)

  def __hash__(self):
    return hash(self._dict)

  def __getitem__(self, key):
    if key not in self._dict:
      return 0
    return self._dict[key]

  def __iter__(self):
    """Iterates through a series of nonzero values."""
    return iter(self._dict)

  def __len__(self):
    return len(self._dict)
