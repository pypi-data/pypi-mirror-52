
====================
library: Collections
====================

:scope: global
:generated: 20190903 12:33:58


A test library providing keywords for handling lists and dictionaries.

``Collections`` is Robot Framework's standard library that provides a
set of keywords for handling Python lists and dictionaries. This
library has keywords, for example, for modifying and getting
values from lists and dictionaries (e.g. `Append To List`, `Get
From Dictionary`) and for verifying their contents (e.g. `Lists
Should Be Equal`, `Dictionary Should Contain Value`).

= Related keywords in BuiltIn =

Following keywords in the BuiltIn library can also be used with
lists and dictionaries:



============================  ===================  ================================
= Keyword Name =              = Applicable With =  = Comment =                     
`Create List`                 lists                                                
`Create Dictionary`           dicts                Was in Collections until RF 2.9.
`Get Length`                  both                                                 
`Length Should Be`            both                                                 
`Should Be Empty`             both                                                 
`Should Not Be Empty`         both                                                 
`Should Contain`              both                                                 
`Should Not Contain`          both                                                 
`Should Contain X Times`      lists                                                
`Should Not Contain X Times`  lists                                                
`Get Count`                   lists                                                

============================  ===================  ================================



= Using with list-like and dictionary-like objects =

List keywords that do not alter the given list can also be used
with tuples, and to some extend also with other iterables.
`Convert To List` can be used to convert tuples and other iterables
to Python ``list`` objects.

Similarly dictionary keywords can, for most parts, be used with other
mappings. `Convert To Dictionary` can be used if real Python ``dict``
objects are needed.

= Boolean arguments =

Some keywords accept arguments that are handled as Boolean values true or
false. If such an argument is given as a string, it is considered false if
it is an empty string or equal to ``FALSE``, ``NONE``, ``NO``, ``OFF`` or
``0``, case-insensitively. Keywords verifying something that allow dropping
actual and expected values from the possible error message also consider
string ``no values`` to be false. Other strings are considered true
regardless their value, and other argument types are tested using the same
[http://docs.python.org/library/stdtypes.html#truth|rules as in Python].

True examples:


======================  =======  ==========  ========================  ================================
`Should Contain Match`  ${list}  ${pattern}  case_insensitive=True     # Strings are generally true.   
`Should Contain Match`  ${list}  ${pattern}  case_insensitive=yes      # Same as the above.            
`Should Contain Match`  ${list}  ${pattern}  case_insensitive=${TRUE}  # Python ``True`` is true.      
`Should Contain Match`  ${list}  ${pattern}  case_insensitive=${42}    # Numbers other than 0 are true.

======================  =======  ==========  ========================  ================================



False examples:


=======================  =======  ==========  =========================  ==============================  ==============================================
`Should Contain Match`   ${list}  ${pattern}  case_insensitive=False     # String ``false`` is false.                                                  
`Should Contain Match`   ${list}  ${pattern}  case_insensitive=no        # Also string ``no`` is false.                                                
`Should Contain Match`   ${list}  ${pattern}  case_insensitive=${EMPTY}  # Empty string is false.                                                      
`Should Contain Match`   ${list}  ${pattern}  case_insensitive=${FALSE}  # Python ``False`` is false.                                                  
`Lists Should Be Equal`  ${x}     ${y}        Custom error               values=no values                # ``no values`` works with ``values`` argument

=======================  =======  ==========  =========================  ==============================  ==============================================



Considering string ``NONE`` false is new in Robot Framework 3.0.3 and
considering also ``OFF`` and ``0`` false is new in Robot Framework 3.1.

= Data in examples =

List related keywords use variables in format ``${Lx}`` in their examples.
They mean lists with as many alphabetic characters as specified by ``x``.
For example, ``${L1}`` means ``['a']`` and ``${L3}`` means
``['a', 'b', 'c']``.

Dictionary keywords use similar ``${Dx}`` variables. For example, ``${D1}``
means ``{'a': 1}`` and ``${D3}`` means ``{'a': 1, 'b': 2, 'c': 3}``.





Append To List
==============
.. py:function:: append_to_list(list_, *values)

   
      
   Adds ``values`` to the end of ``list``.
   
   Example:
   
   
   ==============  =====  ===  =  =
   Append To List  ${L1}  xxx      
   Append To List  ${L2}  x    y  z
   
   ==============  =====  ===  =  =
   
   
   =>
   
   ${L1} = ['a', 'xxx']
   
   ${L2} = ['a', 'b', 'x', 'y', 'z']

   




Combine Lists
=============
.. py:function:: combine_lists(*lists)

   
      
   Combines the given ``lists`` together and returns the result.
   
   The given lists are not altered by this keyword.
   
   Example:
   
   
   ======  ============  =====  =====  =====
   ${x} =  Combine List  ${L1}  ${L2}       
   ${y} =  Combine List  ${L1}  ${L2}  ${L1}
   
   ======  ============  =====  =====  =====
   
   
   =>
   
   ${x} = ['a', 'a', 'b']
   
   ${y} = ['a', 'a', 'b', 'a']
   
   ${L1} and ${L2} are not changed.

   




Convert To Dictionary
=====================
.. py:function:: convert_to_dictionary(item)

   
      
   Converts the given ``item`` to a Python ``dict`` type.
   
   Mainly useful for converting other mappings to normal dictionaries.
   This includes converting Robot Framework's own ``DotDict`` instances
   that it uses if variables are created using the ``&{var}`` syntax.
   
   Use `Create Dictionary` from the BuiltIn library for constructing new
   dictionaries.
   
   New in Robot Framework 2.9.

   




Convert To List
===============
.. py:function:: convert_to_list(item)

   
      
   Converts the given ``item`` to a Python ``list`` type.
   
   Mainly useful for converting tuples and other iterable to lists.
   Use `Create List` from the BuiltIn library for constructing new lists.

   




Copy Dictionary
===============
.. py:function:: copy_dictionary(dictionary, deepcopy=False)

   
      
   Returns a copy of the given dictionary.
   
   The ``deepcopy`` argument controls should the returned dictionary be
   a [https://docs.python.org/library/copy.html|shallow or deep copy].
   By default returns a shallow copy, but that can be changed by giving
   ``deepcopy`` a true value (see `Boolean arguments`). This is a new
   option in Robot Framework 3.1.2. Earlier versions always returned
   shallow copies.
   
   The given dictionary is never altered by this keyword.

   




Copy List
=========
.. py:function:: copy_list(list_, deepcopy=False)

   
      
   Returns a copy of the given list.
   
   If the optional ``deepcopy`` is given a true value, the returned
   list is a deep copy. New option in Robot Framework 3.1.2.
   
   The given list is never altered by this keyword.

   




Count Values In List
====================
.. py:function:: count_values_in_list(list_, value, start=0, end=None)

   
      
   Returns the number of occurrences of the given ``value`` in ``list``.
   
   The search can be narrowed to the selected sublist by the ``start`` and
   ``end`` indexes having the same semantics as with `Get Slice From List`
   keyword. The given list is never altered by this keyword.
   
   Example:
   
   
   ======  ====================  =====  =
   ${x} =  Count Values In List  ${L3}  b
   
   ======  ====================  =====  =
   
   
   =>
   
   ${x} = 1
   
   ${L3} is not changed

   




Dictionaries Should Be Equal
============================
.. py:function:: dictionaries_should_be_equal(dict1, dict2, msg=None, values=True)

   
      
   Fails if the given dictionaries are not equal.
   
   First the equality of dictionaries' keys is checked and after that all
   the key value pairs. If there are differences between the values, those
   are listed in the error message. The types of the dictionaries do not
   need to be same.
   
   See `Lists Should Be Equal` for more information about configuring
   the error message with ``msg`` and ``values`` arguments.

   




Dictionary Should Contain Item
==============================
.. py:function:: dictionary_should_contain_item(dictionary, key, value, msg=None)

   
      
   An item of ``key`` / ``value`` must be found in a ``dictionary``.
   
   Value is converted to unicode for comparison.
   
   Use the ``msg`` argument to override the default error message.

   




Dictionary Should Contain Key
=============================
.. py:function:: dictionary_should_contain_key(dictionary, key, msg=None)

   
      
   Fails if ``key`` is not found from ``dictionary``.
   
   Use the ``msg`` argument to override the default error message.

   




Dictionary Should Contain Sub Dictionary
========================================
.. py:function:: dictionary_should_contain_sub_dictionary(dict1, dict2, msg=None, values=True)

   
      
   Fails unless all items in ``dict2`` are found from ``dict1``.
   
   See `Lists Should Be Equal` for more information about configuring
   the error message with ``msg`` and ``values`` arguments.

   




Dictionary Should Contain Value
===============================
.. py:function:: dictionary_should_contain_value(dictionary, value, msg=None)

   
      
   Fails if ``value`` is not found from ``dictionary``.
   
   Use the ``msg`` argument to override the default error message.

   




Dictionary Should Not Contain Key
=================================
.. py:function:: dictionary_should_not_contain_key(dictionary, key, msg=None)

   
      
   Fails if ``key`` is found from ``dictionary``.
   
   Use the ``msg`` argument to override the default error message.

   




Dictionary Should Not Contain Value
===================================
.. py:function:: dictionary_should_not_contain_value(dictionary, value, msg=None)

   
      
   Fails if ``value`` is found from ``dictionary``.
   
   Use the ``msg`` argument to override the default error message.

   




Get Dictionary Items
====================
.. py:function:: get_dictionary_items(dictionary, sort_keys=True)

   
      
   Returns items of the given ``dictionary`` as a list.
   
   Uses `Get Dictionary Keys` to get keys and then returns corresponding
   items. By default keys are sorted and items returned in that order,
   but this can be changed by giving ``sort_keys`` a false value (see
   `Boolean arguments`). Notice that with Python 3.5 and earlier
   dictionary order is undefined unless using ordered dictionaries.
   
   Items are returned as a flat list so that first item is a key,
   second item is a corresponding value, third item is the second key,
   and so on.
   
   The given ``dictionary`` is never altered by this keyword.
   
   Example:
   
   
   =============  ====================  =====  ===============
   ${sorted} =    Get Dictionary Items  ${D3}                 
   ${unsorted} =  Get Dictionary Items  ${D3}  sort_keys=False
   
   =============  ====================  =====  ===============
   
   
   =>
   
   ${sorted} = ['a', 1, 'b', 2, 'c', 3]
   
   ${unsorted} = ['b', 2, 'a', 1, 'c', 3]    # Order depends on Python version.
   
   ``sort_keys`` is a new option in Robot Framework 3.1.2. Earlier items
   were always sorted based on keys.

   




Get Dictionary Keys
===================
.. py:function:: get_dictionary_keys(dictionary, sort_keys=True)

   
      
   Returns keys of the given ``dictionary`` as a list.
   
   By default keys are returned in sorted order (assuming they are
   sortable), but they can be returned in the original order by giving
   ``sort_keys``  a false value (see `Boolean arguments`). Notice that
   with Python 3.5 and earlier dictionary order is undefined unless using
   ordered dictionaries.
   
   The given ``dictionary`` is never altered by this keyword.
   
   Example:
   
   
   =============  ===================  =====  ===============
   ${sorted} =    Get Dictionary Keys  ${D3}                 
   ${unsorted} =  Get Dictionary Keys  ${D3}  sort_keys=False
   
   =============  ===================  =====  ===============
   
   
   =>
   
   ${sorted} = ['a', 'b', 'c']
   
   ${unsorted} = ['b', 'a', 'c']   # Order depends on Python version.
   
   ``sort_keys`` is a new option in Robot Framework 3.1.2. Earlier keys
   were always sorted.

   




Get Dictionary Values
=====================
.. py:function:: get_dictionary_values(dictionary, sort_keys=True)

   
      
   Returns values of the given ``dictionary`` as a list.
   
   Uses `Get Dictionary Keys` to get keys and then returns corresponding
   values. By default keys are sorted and values returned in that order,
   but this can be changed by giving ``sort_keys`` a false value (see
   `Boolean arguments`). Notice that with Python 3.5 and earlier
   dictionary order is undefined unless using ordered dictionaries.
   
   The given ``dictionary`` is never altered by this keyword.
   
   Example:
   
   
   =============  =====================  =====  ===============
   ${sorted} =    Get Dictionary Values  ${D3}                 
   ${unsorted} =  Get Dictionary Values  ${D3}  sort_keys=False
   
   =============  =====================  =====  ===============
   
   
   =>
   
   ${sorted} = [1, 2, 3]
   
   ${unsorted} = [2, 1, 3]    # Order depends on Python version.
   
   ``sort_keys`` is a new option in Robot Framework 3.1.2. Earlier values
   were always sorted based on keys.

   




Get From Dictionary
===================
.. py:function:: get_from_dictionary(dictionary, key)

   
      
   Returns a value from the given ``dictionary`` based on the given ``key``.
   
   If the given ``key`` cannot be found from the ``dictionary``, this
   keyword fails.
   
   The given dictionary is never altered by this keyword.
   
   Example:
   
   
   ==========  ===================  =====  =
   ${value} =  Get From Dictionary  ${D3}  b
   
   ==========  ===================  =====  =
   
   
   =>
   
   ${value} = 2

   




Get From List
=============
.. py:function:: get_from_list(list_, index)

   
      
   Returns the value specified with an ``index`` from ``list``.
   
   The given list is never altered by this keyword.
   
   Index ``0`` means the first position, ``1`` the second, and so on.
   Similarly, ``-1`` is the last position, ``-2`` the second last, and so on.
   Using an index that does not exist on the list causes an error.
   The index can be either an integer or a string that can be converted
   to an integer.
   
   Examples (including Python equivalents in comments):
   
   
   ======  =============  =====  ==  ========
   ${x} =  Get From List  ${L5}  0   # L5[0] 
   ${y} =  Get From List  ${L5}  -2  # L5[-2]
   
   ======  =============  =====  ==  ========
   
   
   =>
   
   ${x} = 'a'
   
   ${y} = 'd'
   
   ${L5} is not changed

   




Get Index From List
===================
.. py:function:: get_index_from_list(list_, value, start=0, end=None)

   
      
   Returns the index of the first occurrence of the ``value`` on the list.
   
   The search can be narrowed to the selected sublist by the ``start`` and
   ``end`` indexes having the same semantics as with `Get Slice From List`
   keyword. In case the value is not found, -1 is returned. The given list
   is never altered by this keyword.
   
   Example:
   
   
   ======  ===================  =====  =
   ${x} =  Get Index From List  ${L5}  d
   
   ======  ===================  =====  =
   
   
   =>
   
   ${x} = 3
   
   ${L5} is not changed

   




Get Match Count
===============
.. py:function:: get_match_count(list, pattern, case_insensitive=False, whitespace_insensitive=False)

   
      
   Returns the count of matches to ``pattern`` in ``list``.
   
   For more information on ``pattern``, ``case_insensitive``, and
   ``whitespace_insensitive``, see `Should Contain Match`.
   
   Examples:
   
   
   =========  ===============  =======  ==========  =============================================================================  ===================================================================
   ${count}=  Get Match Count  ${list}  a*          # ${count} will be the count of strings beginning with 'a'                                                                                        
   ${count}=  Get Match Count  ${list}  regexp=a.*  # ${matches} will be the count of strings beginning with 'a' (regexp version)                                                                     
   ${count}=  Get Match Count  ${list}  a*          case_insensitive=${True}                                                       # ${matches} will be the count of strings beginning with 'a' or 'A'
   
   =========  ===============  =======  ==========  =============================================================================  ===================================================================
   
   

   




Get Matches
===========
.. py:function:: get_matches(list, pattern, case_insensitive=False, whitespace_insensitive=False)

   
      
   Returns a list of matches to ``pattern`` in ``list``.
   
   For more information on ``pattern``, ``case_insensitive``, and
   ``whitespace_insensitive``, see `Should Contain Match`.
   
   Examples:
   
   
   ===========  ===========  =======  ==========  ========================================================================  ==============================================================
   ${matches}=  Get Matches  ${list}  a*          # ${matches} will contain any string beginning with 'a'                                                                                 
   ${matches}=  Get Matches  ${list}  regexp=a.*  # ${matches} will contain any string beginning with 'a' (regexp version)                                                                
   ${matches}=  Get Matches  ${list}  a*          case_insensitive=${True}                                                  # ${matches} will contain any string beginning with 'a' or 'A'
   
   ===========  ===========  =======  ==========  ========================================================================  ==============================================================
   
   

   




Get Slice From List
===================
.. py:function:: get_slice_from_list(list_, start=0, end=None)

   
      
   Returns a slice of the given list between ``start`` and ``end`` indexes.
   
   The given list is never altered by this keyword.
   
   If both ``start`` and ``end`` are given, a sublist containing values
   from ``start`` to ``end`` is returned. This is the same as
   ``list[start:end]`` in Python. To get all items from the beginning,
   use 0 as the start value, and to get all items until and including
   the end, use ``None`` (default) as the end value.
   
   Using ``start`` or ``end`` not found on the list is the same as using
   the largest (or smallest) available index.
   
   Examples (incl. Python equivalents in comments):
   
   
   ======  ===================  =====  =  ==  ============
   ${x} =  Get Slice From List  ${L5}  2  4   # L5[2:4]   
   ${y} =  Get Slice From List  ${L5}  1      # L5[1:None]
   ${z} =  Get Slice From List  ${L5}     -2  # L5[0:-2]  
   
   ======  ===================  =====  =  ==  ============
   
   
   =>
   
   ${x} = ['c', 'd']
   
   ${y} = ['b', 'c', 'd', 'e']
   
   ${z} = ['a', 'b', 'c']
   
   ${L5} is not changed

   




Insert Into List
================
.. py:function:: insert_into_list(list_, index, value)

   
      
   Inserts ``value`` into ``list`` to the position specified with ``index``.
   
   Index ``0`` adds the value into the first position, ``1`` to the second,
   and so on. Inserting from right works with negative indices so that
   ``-1`` is the second last position, ``-2`` third last, and so on. Use
   `Append To List` to add items to the end of the list.
   
   If the absolute value of the index is greater than
   the length of the list, the value is added at the end
   (positive index) or the beginning (negative index). An index
   can be given either as an integer or a string that can be
   converted to an integer.
   
   Example:
   
   
   ================  =====  =====  ===
   Insert Into List  ${L1}  0      xxx
   Insert Into List  ${L2}  ${-1}  xxx
   
   ================  =====  =====  ===
   
   
   =>
   
   ${L1} = ['xxx', 'a']
   
   ${L2} = ['a', 'xxx', 'b']

   




Keep In Dictionary
==================
.. py:function:: keep_in_dictionary(dictionary, *keys)

   
      
   Keeps the given ``keys`` in the ``dictionary`` and removes all other.
   
   If the given ``key`` cannot be found from the ``dictionary``, it
   is ignored.
   
   Example:
   
   
   ==================  =====  =  =  =
   Keep In Dictionary  ${D5}  b  x  d
   
   ==================  =====  =  =  =
   
   
   =>
   
   ${D5} = {'b': 2, 'd': 4}

   




List Should Contain Sub List
============================
.. py:function:: list_should_contain_sub_list(list1, list2, msg=None, values=True)

   
      
   Fails if not all of the elements in ``list2`` are found in ``list1``.
   
   The order of values and the number of values are not taken into
   account.
   
   See `Lists Should Be Equal` for more information about configuring
   the error message with ``msg`` and ``values`` arguments.

   




List Should Contain Value
=========================
.. py:function:: list_should_contain_value(list_, value, msg=None)

   
      
   Fails if the ``value`` is not found from ``list``.
   
   Use the ``msg`` argument to override the default error message.

   




List Should Not Contain Duplicates
==================================
.. py:function:: list_should_not_contain_duplicates(list_, msg=None)

   
      
   Fails if any element in the ``list`` is found from it more than once.
   
   The default error message lists all the elements that were found
   from the ``list`` multiple times, but it can be overridden by giving
   a custom ``msg``. All multiple times found items and their counts are
   also logged.
   
   This keyword works with all iterables that can be converted to a list.
   The original iterable is never altered.

   




List Should Not Contain Value
=============================
.. py:function:: list_should_not_contain_value(list_, value, msg=None)

   
      
   Fails if the ``value`` is found from ``list``.
   
   Use the ``msg`` argument to override the default error message.

   




Lists Should Be Equal
=====================
.. py:function:: lists_should_be_equal(list1, list2, msg=None, values=True, names=None)

   
      
   Fails if given lists are unequal.
   
   The keyword first verifies that the lists have equal lengths, and then
   it checks are all their values equal. Possible differences between the
   values are listed in the default error message like ``Index 4: ABC !=
   Abc``. The types of the lists do not need to be the same. For example,
   Python tuple and list with same content are considered equal.
   
   The error message can be configured using ``msg`` and ``values``
   arguments:
   - If ``msg`` is not given, the default error message is used.
   - If ``msg`` is given and ``values`` gets a value considered true
     (see `Boolean arguments`), the error message starts with the given
     ``msg`` followed by a newline and the default message.
   - If ``msg`` is given and ``values``  is not given a true value,
     the error message is just the given ``msg``.
   
   Optional ``names`` argument can be used for naming the indices shown in
   the default error message. It can either be a list of names matching
   the indices in the lists or a dictionary where keys are indices that
   need to be named. It is not necessary to name all of the indices.  When
   using a dictionary, keys can be either integers or strings that can be
   converted to integers.
   
   Examples:
   
   
   =====================  =================  ============  ==============  =====
   ${names} =             Create List        First Name    Family Name     Email
   Lists Should Be Equal  ${people1}         ${people2}    names=${names}       
   ${names} =             Create Dictionary  0=First Name  2=Email              
   Lists Should Be Equal  ${people1}         ${people2}    names=${names}       
   
   =====================  =================  ============  ==============  =====
   
   
   
   If the items in index 2 would differ in the above examples, the error
   message would contain a row like ``Index 2 (email): name@foo.com !=
   name@bar.com``.

   




Log Dictionary
==============
.. py:function:: log_dictionary(dictionary, level=INFO)

   
      
   Logs the size and contents of the ``dictionary`` using given ``level``.
   
   Valid levels are TRACE, DEBUG, INFO (default), and WARN.
   
   If you only want to log the size, use keyword `Get Length` from
   the BuiltIn library.

   




Log List
========
.. py:function:: log_list(list_, level=INFO)

   
      
   Logs the length and contents of the ``list`` using given ``level``.
   
   Valid levels are TRACE, DEBUG, INFO (default), and WARN.
   
   If you only want to the length, use keyword `Get Length` from
   the BuiltIn library.

   




Pop From Dictionary
===================
.. py:function:: pop_from_dictionary(dictionary, key, default=)

   
      
   Pops the given ``key`` from the ``dictionary`` and returns its value.
   
   By default the keyword fails if the given ``key`` cannot be found from
   the ``dictionary``. If optional ``default`` value is given, it will be
   returned instead of failing.
   
   Example:
   
   
   =======  ===================  =====  =
   ${val}=  Pop From Dictionary  ${D3}  b
   
   =======  ===================  =====  =
   
   
   =>
   
   ${val} = 2
   
   ${D3} = {'a': 1, 'c': 3}
   
   New in Robot Framework 2.9.2.

   




Remove Duplicates
=================
.. py:function:: remove_duplicates(list_)

   
      
   Returns a list without duplicates based on the given ``list``.
   
   Creates and returns a new list that contains all items in the given
   list so that one item can appear only once. Order of the items in
   the new list is the same as in the original except for missing
   duplicates. Number of the removed duplicates is logged.

   




Remove From Dictionary
======================
.. py:function:: remove_from_dictionary(dictionary, *keys)

   
      
   Removes the given ``keys`` from the ``dictionary``.
   
   If the given ``key`` cannot be found from the ``dictionary``, it
   is ignored.
   
   Example:
   
   
   ======================  =====  =  =  =
   Remove From Dictionary  ${D3}  b  x  y
   
   ======================  =====  =  =  =
   
   
   =>
   
   ${D3} = {'a': 1, 'c': 3}

   




Remove From List
================
.. py:function:: remove_from_list(list_, index)

   
      
   Removes and returns the value specified with an ``index`` from ``list``.
   
   Index ``0`` means the first position, ``1`` the second and so on.
   Similarly, ``-1`` is the last position, ``-2`` the second last, and so on.
   Using an index that does not exist on the list causes an error.
   The index can be either an integer or a string that can be converted
   to an integer.
   
   Example:
   
   
   ======  ================  =====  =
   ${x} =  Remove From List  ${L2}  0
   
   ======  ================  =====  =
   
   
   =>
   
   ${x} = 'a'
   
   ${L2} = ['b']

   




Remove Values From List
=======================
.. py:function:: remove_values_from_list(list_, *values)

   
      
   Removes all occurrences of given ``values`` from ``list``.
   
   It is not an error if a value does not exist in the list at all.
   
   Example:
   
   
   =======================  =====  =  =  =  =
   Remove Values From List  ${L4}  a  c  e  f
   
   =======================  =====  =  =  =  =
   
   
   =>
   
   ${L4} = ['b', 'd']

   




Reverse List
============
.. py:function:: reverse_list(list_)

   
      
   Reverses the given list in place.
   
   Note that the given list is changed and nothing is returned. Use
   `Copy List` first, if you need to keep also the original order.
   
   
   
   ============  =====
   Reverse List  ${L3}
   
   ============  =====
   
   
   =>
   
   ${L3} = ['c', 'b', 'a']

   




Set List Value
==============
.. py:function:: set_list_value(list_, index, value)

   
      
   Sets the value of ``list`` specified by ``index`` to the given ``value``.
   
   Index ``0`` means the first position, ``1`` the second and so on.
   Similarly, ``-1`` is the last position, ``-2`` second last, and so on.
   Using an index that does not exist on the list causes an error.
   The index can be either an integer or a string that can be converted to
   an integer.
   
   Example:
   
   
   ==============  =====  ==  ===
   Set List Value  ${L3}  1   xxx
   Set List Value  ${L3}  -1  yyy
   
   ==============  =====  ==  ===
   
   
   =>
   
   ${L3} = ['a', 'xxx', 'yyy']

   




Set To Dictionary
=================
.. py:function:: set_to_dictionary(dictionary, *key_value_pairs, **items)

   
      
   Adds the given ``key_value_pairs`` and ``items`` to the ``dictionary``.
   
   Giving items as ``key_value_pairs`` means giving keys and values
   as separate arguments:
   
   
   
   =================  =====  ===  =====  ======  ====
   Set To Dictionary  ${D1}  key  value  second  ${2}
   
   =================  =====  ===  =====  ======  ====
   
   
   =>
   
   ${D1} = {'a': 1, 'key': 'value', 'second': 2}
   
   
   
   =================  =====  =========  ===========
   Set To Dictionary  ${D1}  key=value  second=${2}
   
   =================  =====  =========  ===========
   
   
   
   The latter syntax is typically more convenient to use, but it has
   a limitation that keys must be strings.
   
   If given keys already exist in the dictionary, their values are updated.

   




Should Contain Match
====================
.. py:function:: should_contain_match(list, pattern, msg=None, case_insensitive=False, whitespace_insensitive=False)

   
      
   Fails if ``pattern`` is not found in ``list``.
   
   By default, pattern matching is similar to matching files in a shell
   and is case-sensitive and whitespace-sensitive. In the pattern syntax,
   ``*`` matches to anything and ``?`` matches to any single character. You
   can also prepend ``glob=`` to your pattern to explicitly use this pattern
   matching behavior.
   
   If you prepend ``regexp=`` to your pattern, your pattern will be used
   according to the Python
   [http://docs.python.org/library/re.html|re module] regular expression
   syntax. Important note: Backslashes are an escape character, and must
   be escaped with another backslash (e.g. ``regexp=\\d{6}`` to search for
   ``\d{6}``). See `BuiltIn.Should Match Regexp` for more details.
   
   If ``case_insensitive`` is given a true value (see `Boolean arguments`),
   the pattern matching will ignore case.
   
   If ``whitespace_insensitive`` is given a true value (see `Boolean
   arguments`), the pattern matching will ignore whitespace.
   
   Non-string values in lists are ignored when matching patterns.
   
   Use the ``msg`` argument to override the default error message.
   
   See also ``Should Not Contain Match``.
   
   Examples:
   
   
   ====================  =======  =============  ===========================  =====================  =====================================================================
   Should Contain Match  ${list}  a*                                                                 # Match strings beginning with 'a'.                                  
   Should Contain Match  ${list}  regexp=a.*                                                         # Same as the above but with regexp.                                 
   Should Contain Match  ${list}  regexp=\\d{6}                                                      # Match strings containing six digits.                               
   Should Contain Match  ${list}  a*             case_insensitive=True                               # Match strings beginning with 'a' or 'A'.                           
   Should Contain Match  ${list}  ab*            whitespace_insensitive=yes                          # Match strings beginning with 'ab' with possible whitespace ignored.
   Should Contain Match  ${list}  ab*            whitespace_insensitive=true  case_insensitive=true  # Same as the above but also ignore case.                            
   
   ====================  =======  =============  ===========================  =====================  =====================================================================
   
   

   




Should Not Contain Match
========================
.. py:function:: should_not_contain_match(list, pattern, msg=None, case_insensitive=False, whitespace_insensitive=False)

   
      
   Fails if ``pattern`` is found in ``list``.
   
   Exact opposite of `Should Contain Match` keyword. See that keyword
   for information about arguments and usage in general.

   




Sort List
=========
.. py:function:: sort_list(list_)

   
      
   Sorts the given list in place.
   
   Sorting fails if items in the list are not comparable with each others.
   On Python 2 most objects are comparable, but on Python 3 comparing,
   for example, strings with numbers is not possible.
   
   Note that the given list is changed and nothing is returned. Use
   `Copy List` first, if you need to keep also the original order.

   



