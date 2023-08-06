from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


NO_DEFAULT = object()


class Mapping(dict):
    """Base class for HTTP mappings.

    Mappings in HTTP differ from Python dictionaries in that they may have one
    or more values. This dictionary subclass maintains a list of values for
    each key. However, access semantics are asymmetric: subscript assignment
    clobbers to list, while subscript access returns the last item. Think
    about it.

    .. warning:: This isn't thread-safe.

    """

    def __getitem__(self, name):
        """Given a name, return the last value or call self.keyerror.
        """
        try:
            return dict.__getitem__(self, name)[-1]
        except KeyError:
            self.keyerror(name)

    def __setitem__(self, name, value):
        """Given a name and value, clobber any existing values.
        """
        dict.__setitem__(self, name, [value])

    def keyerror(self, key):
        """Called when a key is missing. Default implementation simply reraises.
        """
        raise

    def pop(self, name, default=NO_DEFAULT):
        """Given a name, return a value.

        This removes the last value from the list for name and returns it. If
        there was only one value in the list then the key is removed from the
        mapping. If name is not present and default is given, that is returned
        instead. Otherwise, self.keyerror is called.

        """
        try:
            values = dict.__getitem__(self, name)
        except KeyError:
            if default is not NO_DEFAULT:
                return default
            self.keyerror(name)
        value = values.pop()
        if not values:
            del self[name]
        return value

    popall = dict.pop

    def all(self, name):
        """Given a name, return a list of values, possibly empty.
        """
        return dict.get(self, name, [])

    def get(self, name, default=None):
        """Override to only return the last value.
        """
        return dict.get(self, name, [default])[-1]

    def add(self, name, value):
        """Given a name and value, clobber any existing values with the new one.
        """
        if name in self:
            self.all(name).append(value)
        else:
            dict.__setitem__(self, name, [value])

    def ones(self, *names):
        """Given one or more names of keys, return a list of their values.
        """
        lowered = []
        for name in names:
            n = name.lower()
            if n not in lowered:
                lowered.append(n)
        return [self[name] for name in lowered]
