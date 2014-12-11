class MultiDict:
    """
    Dictionary-like class that can have multiple values for each key.
    """

    def __init__(self, items=None):
        """
        items -- list of (key, value) pairs that specifies the MultiDict initial
                 values or None.
        """
        self._items = items[:] if items else []

    def __str__(self):
        """
        Returns a str representation of the MultiDict.
        """
        return str(self._items)

    def __repr__(self):
        """
        Returns a str representation of the MultiDict.
        """
        return str(self)

    def __eq__(self, other):
        """
        Returns True if other MultiDict is equal to this instance.

        other -- MultiDict instance to be compared with this instance.
        """
        other_items = other._items[:]
        for (k, v) in self._items:
            if (k, v) in other_items:
                other_items.remove((k, v))
            else:
                return False
        return len(other_items) == 0

    def __getitem__(self, key):
        """
        Returns a value associated with the specified key. If no value is
        associated with the specified key, raises a KeyError exception.

        key -- object that represents the key.
        """
        for (k, v) in self._items:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Adds a (key, value) pair.

        key -- object that represents the key.
        value -- object that represents the value.
        """
        self._items.append((key, value))

    def __delitem__(self, key):
        """
        Deletes the pairs identified by the key object. If no value is
        associated with the specified key, raises a KeyError exception.

        key -- object that represents the key.
        """
        found = False
        items = []
        for (k, v) in self._items:
            if k != key:
                items.append((k, v))
            else:
                found = True
        self._items = items
        if not found:
            raise KeyError(key)

    def __contains__(self, key):
        """
        Returns True if there is at least one pair identified by the key object.
        False, otherwise.

        key -- object that represents the key.
        """
        for (k, v) in self._items:
            if k == key:
                return True
        return False

    def __len__(self):
        """
        Returns the number of (key, value) pairs.
        """
        return len(self._items)

    def copy(self):
        """
        Returns a shallow copy of this instance.
        """
        return self.__class__(self._items)

    def clear(self):
        """
        Removes all (key, value) pairs from this instance.
        """
        self._items = []

    def get(self, key, default_value=None):
        """
        Returns a value associated with the specified key. If no value is
        associated with the specified key, returns the specified default_value.

        key -- object that represents the key.
        default_value -- object that is returned if no value is associated with
                         the specified key. None by default.
        """
        return self[key] if key in self else default_value

    def getall(self, key):
        """
        Returns a list of values associated with the specified key. If no value
        is associated with the specified key, returns an empty list.

        key -- object that represents the key.
        """
        values = []
        for (k, v) in self._items:
            if k == key:
                values.append(v)
        return values

    def keys(self):
        """
        Returns a list of the keys.
        """
        return list(set([k for (k, v) in self._items]))

    def items(self):
        """
        Returns a list of tuples of (key, value) pairs.
        """
        return self._items[:]

    def update(self, other):
        """
        Adds the (key, value) pairs of other MultiDict to this instance.

        other -- MultiDict instance that is merged with this instance.
        """
        self._items.extend(other._items)
