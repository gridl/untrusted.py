import untrusted
import collections.abc


class iterator(collections.abc.Iterable):

    _valueType = untrusted.string

    def __init__(self, value, valueType=None):
        """value may be any iterable, e.g. a container, sequence, generator,
           or iterable."""

        if valueType is not None:
            assert isinstance(valueType, type)
            self._valueType = valueType

        self._value = value
   
    def __iter__(self):
        for x in self._value:
            yield self._valueType(x)

    def __repr__(self):
        return "<untrusted.iterator of type %s>" % repr(self._valueType)


def iteratorOf(valueType):
    """Dynamically creates a new untrusted.iterator subclass with a specific valueType"""

    assert isinstance(valueType, type)
    return type('iterableOf.'+valueType.__module__+'.'+valueType.__name__, (iterator,),{"_valueType": valueType})
    

