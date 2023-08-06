"""Base class for all bounds."""
from abc import abstractmethod

from taurus.entity.dict_serializable import DictSerializable
from taurus.entity.value.base_value import BaseValue


class BaseBounds(DictSerializable):
    """Base class for bounds, including RealBounds and CategoricalBounds."""

    @abstractmethod
    def validate(self, value):
        """
        Check if a value is a member of this bounds.

        Parameters
        ----------
        value: BaseValue
            Value to validate

        Returns
        -------
        bool
            True if the value is a member of the bounds, and False otherwise

        """
        if value is None:
            return False
        if isinstance(value, BaseValue):
            return True
        raise TypeError('{} is not a Value object'.format(value))

    @abstractmethod
    def contains(self, bounds):
        """
        Check if another bounds is contained within this bounds.

        Parameters
        ----------
        bounds: BaseBounds
            Other bounds object to check.

        Returns
        -------
        bool
            True if any value that validates true for bounds also validates true for this

        """
        if bounds is None:
            return False
        if isinstance(bounds, BaseBounds):
            return True
        raise TypeError('{} is not a Bounds object'.format(bounds))
