import json
from typing import Any, Optional


class StringJoiner:
    """
    ``StringJoiner`` mimics the ``java.util.StringJoiner`` class. So, Make sure to also have a look at the ``Java``
    documentations available
    `here <https://docs.oracle.com/javase/8/docs/api/java/util/StringJoiner.html#merge-java.util.StringJoiner->`_

    It is supposed to be similar to the ``Java`` version but it would also have some ``Python`` feeling to it.

    As elements are added to the ``StringJoiner`` instance, they are not getting immediately joined. The joining happens
    only when the object is passed to ``str()`` or its ``.toString()`` method is called.

    Examples:
        * Creating a default ``StringJoiner``:

        >>> from pyjlib.util.stringjoiner import StringJoiner
        >>> sj = StringJoiner()
        >>> repr(sj)
        '{"separator": ",", "prefix": "", "suffix": "", "nelem": 0, "str_length": 0, "elements": []}'
        >>> str(sj)
        ''

        * Accessing readonly attributes:

        >>> sj = StringJoiner(prefix="(",suffix=")")
        >>> sj.separator
        ','
        >>> sj.prefix
        '('
        >>> sj.suffix
        ')'
        >>> sj.suffix = "["
        >>> sj.suffix
        ')'

        * adding few elements:

        >>> sj.add("e1")
        {"separator": ",", "prefix": "", "suffix": "", "nelem": 1, "str_length": 2, "elements": ["e1"]}
        >>> sj.add("e2")
        {"separator": ",", "prefix": "", "suffix": "", "nelem": 2, "str_length": 5, "elements": ["e1", "e2"]}

        * adding an element at a specific position:

        >>> sj.add("e1-2",1)
        {"separator": ",", "prefix": "", "suffix": "", "nelem": 3, "str_length": 10, "elements": ["e1", "e1-2", "e2"]}

        * you could check how big would be the resulting string by using ``len()`` or you could see how many elements
          are currently within the ``StringJoiner``:

        >>> sj = StringJoiner(prefix="(",suffix=")")
        >>> sj.add_multi("e1","e2","e3")
        {"separator": ",", "prefix": "(", "suffix": ")", "nelem": 3, "str_length": 10, "elements": ["e1", "e2", "e3"]}
        >>> s = str(sj)
        >>> print(s)
        (e1,e2,e3)
        >>> len(s)
        10
        >>> len(sj)
        10
        >>> sj.nelem
        3

        * you could check if something exists in the ``StringJoiner``:

        >>> sj = StringJoiner()
        >>> sj.add_multi("e1", "e2", "e3")
        {"separator": ",", "prefix": "", "suffix": "", "nelem": 3, "str_length": 8, "elements": ["e1", "e2", "e3"]}
        >>> "e2" in sj
        True
        >>> "non-existing" in sj
        False

        * You could access each element separately:

        >>> sj = StringJoiner(prefix="(",suffix=")")
        >>> sj.add_multi("e1","e2","e3")
        {"separator": ",", "prefix": "(", "suffix": ")", "nelem": 3, "str_length": 10, "elements": ["e1", "e2", "e3"]}
        >>> sj[0]
        'e1'
        >>> sj[1]
        'e2'
        >>> sj[2]
        'e3'
        >>> sj[3]
        Traceback (most recent call last):
        ...
        IndexError: index out of bound. Expected an integer between 0 and 2; got 3.

        * a merge example:

        >>> o_sj.add_multi("o1","o2")
        {"separator": ",", "prefix": "[", "suffix": "]", "nelem": 2, "str_length": 7, "elements": ["o1", "o2"]}
        >>> str(o_sj)
        '[o1,o2]'
        >>> str(sj)
        'e1,e1-2,e2'
        >>> o_sj.merge(sj,1)
        >>> str(o_sj)
        '[o1,e1,e1-2,e2,o2]'

        * adding two ``StringJoiner`` instances: note that the ``+`` operator is not cumulative, also, the addition
          would not change the original instances:

        >>> sj1 = StringJoiner()
        >>> repr(sj1)
        '{"separator": ",", "prefix": "", "suffix": "", "nelem": 0, "str_length": 0, "elements": []}'
        >>> sj2 = StringJoiner(prefix="(",suffix=")")
        >>> repr(sj2)
        '{"separator": ",", "prefix": "(", "suffix": ")", "nelem": 0, "str_length": 2, "elements": []}'
        >>> sj1.add_multi("sj1_e1","sj1_e2")
        {"separator": ",", "prefix": "", "suffix": "", "nelem": 2, "str_length": 13, "elements": ["sj1_e1", "sj1_e2"]}
        >>> sj2.add_multi("sj2_e1","sj2_e2")
        {"separator": ",", "prefix": "(", "suffix": ")", "nelem": 2, "str_length": 15, "elements": ["sj2_e1", "sj2_e2"]}
        >>> str(sj1)
        'sj1_e1,sj1_e2'
        >>> str(sj2)
        '(sj2_e1,sj2_e2)'
        >>> sj1_2 = sj1 + sj2 # the sum is not cumulative. You get a different results if you change the order.
        >>> str(sj1_2)
        'sj1_e1,sj1_e2,sj2_e1,sj2_e2'
        >>> sj2_1 = sj2 + sj1
        >>> str(sj2_1)
        '(sj2_e1,sj2_e2,sj1_e1,sj1_e2)'
        >>> str(sj1) # after addition, the original instances do not change.
        'sj1_e1,sj1_e2'
        >>> str(sj2)
        '(sj2_e1,sj2_e2)'

        * you could subtract two ``StringJoiner``:

        >>> sj1 = StringJoiner()
        >>> sj1.add_multi("e1", "e2", "e3")
        {"separator": ",", "prefix": "", "suffix": "", "nelem": 3, "str_length": 8, "elements": ["e1", "e2", "e3"]}
        >>>
        >>> sj2 = StringJoiner()
        >>> sj2.add_multi("e2", "e3", "e4")
        {"separator": ",", "prefix": "", "suffix": "", "nelem": 3, "str_length": 8, "elements": ["e2", "e3", "e4"]}
        >>> sj1_2 = sj1 - sj2
        >>> str(sj1_2)
        'e1'
        >>> sj2_1 = sj2 - sj1
        >>> str(sj2_1)
        'e4'

    """
    def __init__(self, separator=",", prefix="", suffix="") -> None:
        """
        Initializes a StringJoiner instance.
        :param separator: The separator to be used. Default value is comma
        :param prefix: The prefix to be used. Default value is empty
        :param suffix: The suffix to be used. Default value is empty

        :raise: TypeError: if any of the separator, prefix, or suffix is not of type str.
        """
        if isinstance(separator, str) and \
            isinstance(prefix, str) and \
            isinstance(suffix, str):

            self._separator = separator
            self._prefix = prefix
            self._suffix = suffix
            self._elements = []
            self._str_lenght = 0
        else:
            raise TypeError("Separator, prefix, and suffix must be of type str.")

    @property
    def separator(self):
        """
        provides access to separator. Readonly attribute.

        :return: the string used as separator
        """
        return self._separator

    @separator.setter
    def separator(self, value):
        pass

    @property
    def prefix(self):
        """
        provides access to the prefix. Readonly attribute.

        :return: the string used as prefix
        """
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        pass

    @property
    def suffix(self):
        """
        provides access to the suffix. Readonly attribue.

        :return: the string used as suffix
        """
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        pass

    @classmethod
    def _isReadOnly(cls, name: str) -> bool:
        return name in ("_separator", "_prefix", "_suffix", "_elements")

    @property
    def nelem(self):
        """
        number of elements that would be join together. Readonly attribute.

        :return: an integer showing number of elements that would be joined together.
        """
        return len(self._elements)

    @nelem.setter
    def nelem(self, value):
        pass

    def __len__(self):
        return self._str_lenght \
                + max(self.nelem - 1, 0) * len(self.separator) \
                + len(self.prefix) \
                + len(self.suffix)

    def __str__(self):
        return self.prefix + self.separator.join(self._elements) + self.suffix

    toString = __str__

    def __repr__(self):
        tmp_dic = dict(separator=self.separator, prefix=self.prefix, suffix=self.suffix, nelem=self.nelem,
                       str_length=len(self), elements=self._elements)
        return str(json.dumps(tmp_dic))

    def _setIdx(self, idx: int) -> int:
        if idx is None:
            idx = self.nelem
        elif not isinstance(idx, int):
            raise TypeError("Only integer values are accepted.")
        elif idx > self.nelem:
            raise IndexError("Trying to add an element way beyond the end of the list.")
        elif idx < -self.nelem:
            raise IndexError("index out of range.")

        return idx

    def add(self, value: Any, idx=None):
        """
        adds an element to the list that are going to be joined.

        :param value: the value that is going to be added to the list. Note that regardless of the type of the value
                      the list would always add str(value) to the list and not the value itself. So, always a string
                      representation of the value is added.
        :param idx: An optional integer suggesting where in the list this value should be added. If not provided, the
                    value is added at the end of the list.
        :return: the same instance of the ``StringJoiner``, so you could use it in a chain call.

        Example:
            Using Chain add:

            >>> sj = StringJoiner()
            >>> sj.add("first element").add("second element")

        """
        idx = self._setIdx(idx)

        value_str = str(value)
        self._elements.insert(idx, value_str)
        self._str_lenght += len(value_str)
        return self

    def add_multi(self, *values: Any, idx=None):
        """
        The same as ``sj.add``, however, you would be able to provide multiple entry at the same time.

        :param values: the values that are going to be added to the list
        :param idx: the index to start inserting the values.
        :return: the same instance of the ``StringJoiner``, so you could use it in a chain call.
        """
        idx = self._setIdx(idx)

        for e in values:
            self.add(e, idx)
            idx += 1

        return self

    def remove(self, value) -> None:
        """
        removes a value, if it is in the list.

        :param value: The value, whose string representation needs to be removed.

        :raise: ValueError: if the value is not found in the list.
        """
        value_str = str(value)
        self._elements.remove(value_str)
        self._str_lenght -= len(value_str)

    def remove_multi(self, *values):
        """
        The same as ``.remove``, this function tries to remove the value that are provided. Note that this function does
        not raises a ``ValueError`` if the value is not in the list.

        :param values: the values that are supposed to be removed.

        :return: a list of string, with those elements that were removed from the ``StringJoiner``
        """
        output = []
        for e in values:
            try:
                self.remove(e)
                output.append(e)
            except ValueError:
                pass

        return output

    def remove_by_index(self, *indices):
        """
        Could be used to remove multiple elements by their index. This does not produces an ``IndexError``. Also note
        that you could remove one element at a time as you do with regular lists.

        Example:
            * removing multiple elements:

            >>> sj.remove_by_index(1,3,4)

            * removing one element at a time:

            >>> del sj[1]
            >>> del sj[3]
            >>> del sj[4]

        :param indices: list of indices that are supposed to be removed.

        :return: list of indices that were successfully removed.

        :raise: TypeError: if any of the indices are not integer.
        """
        output = []
        if all(map(lambda e: isinstance(e, int), indices)):
            for i in indices:
                try:
                    del self[i]
                    output.append(i)
                except IndexError:
                    pass
        else:
            raise TypeError("only integer indices are accepted.")

    def __contains__(self, item):
        return str(item) in self._elements

    def __delitem__(self, idx: int) -> None:
        if isinstance(idx, int):
            if (idx >= self.nelem) or (idx < -self.nelem):
                raise IndexError(f"index out of bound. Expected an integer between {-self.nelem} and {self.nelem - 1};"
                                 f" got {idx}.")
            else:
                old_value_str = self[idx]
                del self._elements[idx]
                self._str_lenght -= len(old_value_str)
        else:
            raise TypeError("only integer indices are accepted.")

    def __getitem__(self, idx: int) -> str:
        if isinstance(idx, int):
            if (idx >= self.nelem) or (idx < -self.nelem):
                raise IndexError(f"index out of bound. Expected an integer between {-self.nelem} and {self.nelem - 1};"
                                 f" got {idx}.")
            else:
                return self._elements[idx]
        else:
            raise TypeError("only integer indices are accepted.")

    def __setitem__(self, idx: int, value: any) -> Optional[str]:
        if isinstance(idx, int):
            if idx < -self.nelem:
                raise IndexError("index out of range.")

            if idx >= self.nelem:
                self.add(value, idx)
                return None

            if idx < 0:
                idx = self.nelem + idx

            old_value_str = self[idx]
            self.add(value, idx)
            del self[idx+1]
            return old_value_str
        else:
            raise TypeError("only integer indices are accepted.")

    def __add__(self, other):
        out_sj = StringJoiner(
            separator=self.separator,
            prefix=self.prefix,
            suffix=self.suffix
        )

        out_sj.merge(self)
        out_sj.merge(other)
        return out_sj

    def __sub__(self, other):
        out_sj = StringJoiner(
            separator=self.separator,
            prefix=self.prefix,
            suffix=self.suffix
        )

        for e in self:
            if not (e in other):
                out_sj.add(e)

        return out_sj

    def __eq__(self, other):
        if (other is None) or (not isinstance(other, StringJoiner)):
            return False

        if (self.separator != other.separator) or \
                (self.prefix != other.prefix) or \
                (self.suffix != other.suffix) or \
                (self.nelem != other.nelem) or \
                (len(self) != len(other)):
            return False

        return all(map(lambda e: e[1] == e[2], zip(self, other)))

    def merge(self, o_iterable, idx=None) -> None:
        """
        merges the elements of another iterable object or another ``StringJoiner`` to this instance.

        :param o_iterable: The other iterable object that its elements are supposed to be merged with this one.

        :param idx: The starting index to merge. This could be used to merge another iterable in the middle of the
                    current one. If not provided, the merge happens at the end of the current elements.

        """
        idx = self._setIdx(idx)

        for e in o_iterable:
            self.add(e, idx)
            idx += 1
