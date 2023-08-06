
.. py:currentmodule:: goma

First setup basic objects
=========================

For a simple example setup imports and generate a nested list of match details.

.. doctest::

    >>> from goma.exactmatch import ExactMatch
    >>> detail_list = [["Property1","Value1_2"],["Property2","Value2_2"],["Property3","Value3_2"]]

And define a mapping list as instruction for the mapping algorithm

.. doctest::

   >>> mapping_list = list()
   >>> mapping_list.append(["Property1","Property2","Property3","Target"])
   >>> mapping_list.append(["Value1_1","Value2_1","Value3_1","Target1"])
   >>> mapping_list.append(["Value1_2","Value2_2","Value3_2","Target2"])

Finally generate an |ExactMatch| instance and run the matching algorithm

.. doctest::

   >>> exact_match = ExactMatch()
   >>> exact_match.match(detail_list, mapping_list)
   'Target2'
