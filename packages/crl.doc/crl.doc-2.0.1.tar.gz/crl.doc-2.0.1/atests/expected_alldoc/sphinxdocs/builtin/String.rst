
===============
library: String
===============

:scope: global
:generated: 20190903 12:33:58


A test library for string manipulation and verification.

``String`` is Robot Framework's standard library for manipulating
strings (e.g. `Replace String Using Regexp`, `Split To Lines`) and
verifying their contents (e.g. `Should Be String`).

Following keywords from ``BuiltIn`` library can also be used with strings:

- `Catenate`
- `Get Length`
- `Length Should Be`
- `Should (Not) Be Empty`
- `Should (Not) Be Equal (As Strings/Integers/Numbers)`
- `Should (Not) Match (Regexp)`
- `Should (Not) Contain`
- `Should (Not) Start With`
- `Should (Not) End With`
- `Convert To String`
- `Convert To Bytes`





Convert To Lowercase
====================
.. py:function:: convert_to_lowercase(string)

   
      
   Converts string to lowercase.
   
   Examples:
   
   
   ===============  ====================  ======
   ${str1} =        Convert To Lowercase  ABC   
   ${str2} =        Convert To Lowercase  1A2c3D
   Should Be Equal  ${str1}               abc   
   Should Be Equal  ${str2}               1a2c3d
   
   ===============  ====================  ======
   
   

   




Convert To Uppercase
====================
.. py:function:: convert_to_uppercase(string)

   
      
   Converts string to uppercase.
   
   Examples:
   
   
   ===============  ====================  ======
   ${str1} =        Convert To Uppercase  abc   
   ${str2} =        Convert To Uppercase  1a2C3d
   Should Be Equal  ${str1}               ABC   
   Should Be Equal  ${str2}               1A2C3D
   
   ===============  ====================  ======
   
   

   




Decode Bytes To String
======================
.. py:function:: decode_bytes_to_string(bytes, encoding, errors=strict)

   
      
   Decodes the given ``bytes`` to a Unicode string using the given ``encoding``.
   
   ``errors`` argument controls what to do if decoding some bytes fails.
   All values accepted by ``decode`` method in Python are valid, but in
   practice the following values are most useful:
   
   - ``strict``: fail if characters cannot be decoded (default)
   - ``ignore``: ignore characters that cannot be decoded
   - ``replace``: replace characters that cannot be decoded with
     a replacement character
   
   Examples:
   
   
   ===========  ======================  ========  =====  =============
   ${string} =  Decode Bytes To String  ${bytes}  UTF-8               
   ${string} =  Decode Bytes To String  ${bytes}  ASCII  errors=ignore
   
   ===========  ======================  ========  =====  =============
   
   
   
   Use `Encode String To Bytes` if you need to convert Unicode strings to
   byte strings, and `Convert To String` in ``BuiltIn`` if you need to
   convert arbitrary objects to Unicode strings.

   




Encode String To Bytes
======================
.. py:function:: encode_string_to_bytes(string, encoding, errors=strict)

   
      
   Encodes the given Unicode ``string`` to bytes using the given ``encoding``.
   
   ``errors`` argument controls what to do if encoding some characters fails.
   All values accepted by ``encode`` method in Python are valid, but in
   practice the following values are most useful:
   
   - ``strict``: fail if characters cannot be encoded (default)
   - ``ignore``: ignore characters that cannot be encoded
   - ``replace``: replace characters that cannot be encoded with
     a replacement character
   
   Examples:
   
   
   ==========  ======================  =========  =====  =============
   ${bytes} =  Encode String To Bytes  ${string}  UTF-8               
   ${bytes} =  Encode String To Bytes  ${string}  ASCII  errors=ignore
   
   ==========  ======================  =========  =====  =============
   
   
   
   Use `Convert To Bytes` in ``BuiltIn`` if you want to create bytes based
   on character or integer sequences. Use `Decode Bytes To String` if you
   need to convert byte strings to Unicode strings and `Convert To String`
   in ``BuiltIn`` if you need to convert arbitrary objects to Unicode.

   




Fetch From Left
===============
.. py:function:: fetch_from_left(string, marker)

   
      
   Returns contents of the ``string`` before the first occurrence of ``marker``.
   
   If the ``marker`` is not found, whole string is returned.
   
   See also `Fetch From Right`, `Split String` and `Split String
   From Right`.

   




Fetch From Right
================
.. py:function:: fetch_from_right(string, marker)

   
      
   Returns contents of the ``string`` after the last occurrence of ``marker``.
   
   If the ``marker`` is not found, whole string is returned.
   
   See also `Fetch From Left`, `Split String` and `Split String
   From Right`.

   




Format String
=============
.. py:function:: format_string(template, *positional, **named)

   
      
   Formats a ``template`` using the given ``positional`` and ``named`` arguments.
   
   The template can be either be a string or an absolute path to
   an existing file. In the latter case the file is read and its contents
   are used as the template. If the template file contains non-ASCII
   characters, it must be encoded using UTF-8.
   
   The template is formatted using Python's
   [https://docs.python.org/library/string.html#format-string-syntax|format
   string syntax]. Placeholders are marked using ``{}`` with possible
   field name and format specification inside. Literal curly braces
   can be inserted by doubling them like `{{` and `}}`.
   
   Examples:
   
   
   =======  =============  ==============================  ============  ==============  ========
   ${to} =  Format String  To: {} <{}>                     ${user}       ${email}                
   ${to} =  Format String  To: {name} <{email}>            name=${name}  email=${email}          
   ${to} =  Format String  To: {user.name} <{user.email}>  user=${user}                          
   ${xx} =  Format String  {:*^30}                         centered                              
   ${yy} =  Format String  {0:{width}{base}}               ${42}         base=X          width=10
   ${zz} =  Format String  ${CURDIR}/template.txt          positional    named=value             
   
   =======  =============  ==============================  ============  ==============  ========
   
   
   
   New in Robot Framework 3.1.

   




Generate Random String
======================
.. py:function:: generate_random_string(length=8, chars=[LETTERS][NUMBERS])

   
      
   Generates a string with a desired ``length`` from the given ``chars``.
   
   The population sequence ``chars`` contains the characters to use
   when generating the random string. It can contain any
   characters, and it is possible to use special markers
   explained in the table below:
   
   
   
   =============  ===============================================
   = Marker =     = Explanation =                                
   ``[LOWER]``    Lowercase ASCII characters from ``a`` to ``z``.
   ``[UPPER]``    Uppercase ASCII characters from ``A`` to ``Z``.
   ``[LETTERS]``  Lowercase and uppercase ASCII characters.      
   ``[NUMBERS]``  Numbers from 0 to 9.                           
   
   =============  ===============================================
   
   
   
   Examples:
   
   
   ========  ======================  ==  ===============
   ${ret} =  Generate Random String                     
   ${low} =  Generate Random String  12  [LOWER]        
   ${bin} =  Generate Random String  8   01             
   ${hex} =  Generate Random String  4   [NUMBERS]abcdef
   
   ========  ======================  ==  ===============
   
   

   




Get Line
========
.. py:function:: get_line(string, line_number)

   
      
   Returns the specified line from the given ``string``.
   
   Line numbering starts from 0 and it is possible to use
   negative indices to refer to lines from the end. The line is
   returned without the newline character.
   
   Examples:
   
   
   =============  ========  =========  ==
   ${first} =     Get Line  ${string}  0 
   ${2nd last} =  Get Line  ${string}  -2
   
   =============  ========  =========  ==
   
   
   
   Use `Split To Lines` if all lines are needed.

   




Get Line Count
==============
.. py:function:: get_line_count(string)

   
      
   Returns and logs the number of lines in the given string.

   




Get Lines Containing String
===========================
.. py:function:: get_lines_containing_string(string, pattern, case_insensitive=False)

   
      
   Returns lines of the given ``string`` that contain the ``pattern``.
   
   The ``pattern`` is always considered to be a normal string, not a glob
   or regexp pattern. A line matches if the ``pattern`` is found anywhere
   on it.
   
   The match is case-sensitive by default, but giving ``case_insensitive``
   a true value makes it case-insensitive. The value is considered true
   if it is a non-empty string that is not equal to ``false``, ``none`` or
   ``no``. If the value is not a string, its truth value is got directly
   in Python. Considering ``none`` false is new in RF 3.0.3.
   
   Lines are returned as one string catenated back together with
   newlines. Possible trailing newline is never returned. The
   number of matching lines is automatically logged.
   
   Examples:
   
   
   ==========  ===========================  =========  ==========  ================
   ${lines} =  Get Lines Containing String  ${result}  An example                  
   ${ret} =    Get Lines Containing String  ${ret}     FAIL        case-insensitive
   
   ==========  ===========================  =========  ==========  ================
   
   
   
   See `Get Lines Matching Pattern` and `Get Lines Matching Regexp`
   if you need more complex pattern matching.

   




Get Lines Matching Pattern
==========================
.. py:function:: get_lines_matching_pattern(string, pattern, case_insensitive=False)

   
      
   Returns lines of the given ``string`` that match the ``pattern``.
   
   The ``pattern`` is a _glob pattern_ where:
   
   
   ============  ==================================================================================================
   ``*``         matches everything                                                                                
   ``?``         matches any single character                                                                      
   ``[chars]``   matches any character inside square brackets (e.g. ``[abc]`` matches either ``a``, ``b`` or ``c``)
   ``[!chars]``  matches any character not inside square brackets                                                  
   
   ============  ==================================================================================================
   
   
   
   A line matches only if it matches the ``pattern`` fully.
   
   The match is case-sensitive by default, but giving ``case_insensitive``
   a true value makes it case-insensitive. The value is considered true
   if it is a non-empty string that is not equal to ``false``, ``none`` or
   ``no``. If the value is not a string, its truth value is got directly
   in Python. Considering ``none`` false is new in RF 3.0.3.
   
   Lines are returned as one string catenated back together with
   newlines. Possible trailing newline is never returned. The
   number of matching lines is automatically logged.
   
   Examples:
   
   
   ==========  ==========================  =========  ================  =====================
   ${lines} =  Get Lines Matching Pattern  ${result}  Wild???? example                       
   ${ret} =    Get Lines Matching Pattern  ${ret}     FAIL: *           case_insensitive=true
   
   ==========  ==========================  =========  ================  =====================
   
   
   
   See `Get Lines Matching Regexp` if you need more complex
   patterns and `Get Lines Containing String` if searching
   literal strings is enough.

   




Get Lines Matching Regexp
=========================
.. py:function:: get_lines_matching_regexp(string, pattern, partial_match=False)

   
      
   Returns lines of the given ``string`` that match the regexp ``pattern``.
   
   See `BuiltIn.Should Match Regexp` for more information about
   Python regular expression syntax in general and how to use it
   in Robot Framework test data in particular.
   
   By default lines match only if they match the pattern fully, but
   partial matching can be enabled by giving the ``partial_match``
   argument a true value. The value is considered true
   if it is a non-empty string that is not equal to ``false``, ``none`` or
   ``no``. If the value is not a string, its truth value is got directly
   in Python. Considering ``none`` false is new in RF 3.0.3.
   
   If the pattern is empty, it matches only empty lines by default.
   When partial matching is enabled, empty pattern matches all lines.
   
   Notice that to make the match case-insensitive, you need to prefix
   the pattern with case-insensitive flag ``(?i)``.
   
   Lines are returned as one string concatenated back together with
   newlines. Possible trailing newline is never returned. The
   number of matching lines is automatically logged.
   
   Examples:
   
   
   ==========  =========================  =========  =================  ==================
   ${lines} =  Get Lines Matching Regexp  ${result}  Reg\\w{3} example                    
   ${lines} =  Get Lines Matching Regexp  ${result}  Reg\\w{3} example  partial_match=true
   ${ret} =    Get Lines Matching Regexp  ${ret}     (?i)FAIL: .*                         
   
   ==========  =========================  =========  =================  ==================
   
   
   
   See `Get Lines Matching Pattern` and `Get Lines Containing
   String` if you do not need full regular expression powers (and
   complexity).
   
   ``partial_match`` argument is new in Robot Framework 2.9. In earlier
    versions exact match was always required.

   




Get Regexp Matches
==================
.. py:function:: get_regexp_matches(string, pattern, *groups)

   
      
   Returns a list of all non-overlapping matches in the given string.
   
   ``string`` is the string to find matches from and ``pattern`` is the
   regular expression. See `BuiltIn.Should Match Regexp` for more
   information about Python regular expression syntax in general and how
   to use it in Robot Framework test data in particular.
   
   If no groups are used, the returned list contains full matches. If one
   group is used, the list contains only contents of that group. If
   multiple groups are used, the list contains tuples that contain
   individual group contents. All groups can be given as indexes (starting
   from 1) and named groups also as names.
   
   Examples:
   
   
   ================  ==================  ==========  =============  ====  =
   ${no match} =     Get Regexp Matches  the string  xxx                   
   ${matches} =      Get Regexp Matches  the string  t..                   
   ${one group} =    Get Regexp Matches  the string  t(..)          1      
   ${named group} =  Get Regexp Matches  the string  t(?P<name>..)  name   
   ${two groups} =   Get Regexp Matches  the string  t(.)(.)        1     2
   
   ================  ==================  ==========  =============  ====  =
   
   
   =>
   
   ${no match} = []
   
   ${matches} = ['the', 'tri']
   
   ${one group} = ['he', 'ri']
   
   ${named group} = ['he', 'ri']
   
   ${two groups} = [('h', 'e'), ('r', 'i')]
   
   New in Robot Framework 2.9.

   




Get Substring
=============
.. py:function:: get_substring(string, start, end=None)

   
      
   Returns a substring from ``start`` index to ``end`` index.
   
   The ``start`` index is inclusive and ``end`` is exclusive.
   Indexing starts from 0, and it is possible to use
   negative indices to refer to characters from the end.
   
   Examples:
   
   
   =================  =============  =========  ==  ==
   ${ignore first} =  Get Substring  ${string}  1     
   ${ignore last} =   Get Substring  ${string}      -1
   ${5th to 10th} =   Get Substring  ${string}  4   10
   ${first two} =     Get Substring  ${string}      1 
   ${last two} =      Get Substring  ${string}  -2    
   
   =================  =============  =========  ==  ==
   
   

   




Remove String
=============
.. py:function:: remove_string(string, *removables)

   
      
   Removes all ``removables`` from the given ``string``.
   
   ``removables`` are used as literal strings. Each removable will be
   matched to a temporary string from which preceding removables have
   been already removed. See second example below.
   
   Use `Remove String Using Regexp` if more powerful pattern matching is
   needed. If only a certain number of matches should be removed,
   `Replace String` or `Replace String Using Regexp` can be used.
   
   A modified version of the string is returned and the original
   string is not altered.
   
   Examples:
   
   
   ===============  =============  ===============  ====  ==
   ${str} =         Remove String  Robot Framework  work    
   Should Be Equal  ${str}         Robot Frame              
   ${str} =         Remove String  Robot Framework  o     bt
   Should Be Equal  ${str}         R Framewrk               
   
   ===============  =============  ===============  ====  ==
   
   

   




Remove String Using Regexp
==========================
.. py:function:: remove_string_using_regexp(string, *patterns)

   
      
   Removes ``patterns`` from the given ``string``.
   
   This keyword is otherwise identical to `Remove String`, but
   the ``patterns`` to search for are considered to be a regular
   expression. See `Replace String Using Regexp` for more information
   about the regular expression syntax. That keyword can also be
   used if there is a need to remove only a certain number of
   occurrences.

   




Replace String
==============
.. py:function:: replace_string(string, search_for, replace_with, count=-1)

   
      
   Replaces ``search_for`` in the given ``string`` with ``replace_with``.
   
   ``search_for`` is used as a literal string. See `Replace String
   Using Regexp` if more powerful pattern matching is needed.
   If you need to just remove a string see `Remove String`.
   
   If the optional argument ``count`` is given, only that many
   occurrences from left are replaced. Negative ``count`` means
   that all occurrences are replaced (default behaviour) and zero
   means that nothing is done.
   
   A modified version of the string is returned and the original
   string is not altered.
   
   Examples:
   
   
   ===============  ==============  ==============  =====  ========  =======
   ${str} =         Replace String  Hello, world!   world  tellus           
   Should Be Equal  ${str}          Hello, tellus!                          
   ${str} =         Replace String  Hello, world!   l      ${EMPTY}  count=1
   Should Be Equal  ${str}          Helo, world!                            
   
   ===============  ==============  ==============  =====  ========  =======
   
   

   




Replace String Using Regexp
===========================
.. py:function:: replace_string_using_regexp(string, pattern, replace_with, count=-1)

   
      
   Replaces ``pattern`` in the given ``string`` with ``replace_with``.
   
   This keyword is otherwise identical to `Replace String`, but
   the ``pattern`` to search for is considered to be a regular
   expression.  See `BuiltIn.Should Match Regexp` for more
   information about Python regular expression syntax in general
   and how to use it in Robot Framework test data in particular.
   
   If you need to just remove a string see `Remove String Using Regexp`.
   
   Examples:
   
   
   ========  ===========================  ======  ======================  ========  =======
   ${str} =  Replace String Using Regexp  ${str}  20\\d\\d-\\d\\d-\\d\\d  <DATE>           
   ${str} =  Replace String Using Regexp  ${str}  (Hello|Hi)              ${EMPTY}  count=1
   
   ========  ===========================  ======  ======================  ========  =======
   
   

   




Should Be Byte String
=====================
.. py:function:: should_be_byte_string(item, msg=None)

   
      
   Fails if the given ``item`` is not a byte string.
   
   Use `Should Be Unicode String` if you want to verify the ``item`` is a
   Unicode string, or `Should Be String` if both Unicode and byte strings
   are fine. See `Should Be String` for more details about Unicode strings
   and byte strings.
   
   The default error message can be overridden with the optional
   ``msg`` argument.

   




Should Be Lowercase
===================
.. py:function:: should_be_lowercase(string, msg=None)

   
      
   Fails if the given ``string`` is not in lowercase.
   
   For example, ``'string'`` and ``'with specials!'`` would pass, and
   ``'String'``, ``''`` and ``' '`` would fail.
   
   The default error message can be overridden with the optional
   ``msg`` argument.
   
   See also `Should Be Uppercase` and `Should Be Titlecase`.

   




Should Be String
================
.. py:function:: should_be_string(item, msg=None)

   
      
   Fails if the given ``item`` is not a string.
   
   With Python 2, except with IronPython, this keyword passes regardless
   is the ``item`` a Unicode string or a byte string. Use `Should Be
   Unicode String` or `Should Be Byte String` if you want to restrict
   the string type. Notice that with Python 2, except with IronPython,
   ``'string'`` creates a byte string and ``u'unicode'`` must be used to
   create a Unicode string.
   
   With Python 3 and IronPython, this keyword passes if the string is
   a Unicode string but fails if it is bytes. Notice that with both
   Python 3 and IronPython, ``'string'`` creates a Unicode string, and
   ``b'bytes'`` must be used to create a byte string.
   
   The default error message can be overridden with the optional
   ``msg`` argument.

   




Should Be Titlecase
===================
.. py:function:: should_be_titlecase(string, msg=None)

   
      
   Fails if given ``string`` is not title.
   
   ``string`` is a titlecased string if there is at least one
   character in it, uppercase characters only follow uncased
   characters and lowercase characters only cased ones.
   
   For example, ``'This Is Title'`` would pass, and ``'Word In UPPER'``,
   ``'Word In lower'``, ``''`` and ``' '`` would fail.
   
   The default error message can be overridden with the optional
   ``msg`` argument.
   
   See also `Should Be Uppercase` and `Should Be Lowercase`.

   




Should Be Unicode String
========================
.. py:function:: should_be_unicode_string(item, msg=None)

   
      
   Fails if the given ``item`` is not a Unicode string.
   
   Use `Should Be Byte String` if you want to verify the ``item`` is a
   byte string, or `Should Be String` if both Unicode and byte strings
   are fine. See `Should Be String` for more details about Unicode
   strings and byte strings.
   
   The default error message can be overridden with the optional
   ``msg`` argument.

   




Should Be Uppercase
===================
.. py:function:: should_be_uppercase(string, msg=None)

   
      
   Fails if the given ``string`` is not in uppercase.
   
   For example, ``'STRING'`` and ``'WITH SPECIALS!'`` would pass, and
   ``'String'``, ``''`` and ``' '`` would fail.
   
   The default error message can be overridden with the optional
   ``msg`` argument.
   
   See also `Should Be Titlecase` and `Should Be Lowercase`.

   




Should Not Be String
====================
.. py:function:: should_not_be_string(item, msg=None)

   
      
   Fails if the given ``item`` is a string.
   
   See `Should Be String` for more details about Unicode strings and byte
   strings.
   
   The default error message can be overridden with the optional
   ``msg`` argument.

   




Split String
============
.. py:function:: split_string(string, separator=None, max_split=-1)

   
      
   Splits the ``string`` using ``separator`` as a delimiter string.
   
   If a ``separator`` is not given, any whitespace string is a
   separator. In that case also possible consecutive whitespace
   as well as leading and trailing whitespace is ignored.
   
   Split words are returned as a list. If the optional
   ``max_split`` is given, at most ``max_split`` splits are done, and
   the returned list will have maximum ``max_split + 1`` elements.
   
   Examples:
   
   
   ==========  ============  ============  =========  ==  =
   @{words} =  Split String  ${string}                     
   @{words} =  Split String  ${string}     ,${SPACE}       
   ${pre}      ${post} =     Split String  ${string}  ::  1
   
   ==========  ============  ============  =========  ==  =
   
   
   
   See `Split String From Right` if you want to start splitting
   from right, and `Fetch From Left` and `Fetch From Right` if
   you only want to get first/last part of the string.

   




Split String From Right
=======================
.. py:function:: split_string_from_right(string, separator=None, max_split=-1)

   
      
   Splits the ``string`` using ``separator`` starting from right.
   
   Same as `Split String`, but splitting is started from right. This has
   an effect only when ``max_split`` is given.
   
   Examples:
   
   
   ========  =========  =======================  =========  =  =
   ${first}  ${rest} =  Split String             ${string}  -  1
   ${rest}   ${last} =  Split String From Right  ${string}  -  1
   
   ========  =========  =======================  =========  =  =
   
   

   




Split String To Characters
==========================
.. py:function:: split_string_to_characters(string)

   
      
   Splits the given ``string`` to characters.
   
   Example:
   
   
   ===============  ==========================  =========
   @{characters} =  Split String To Characters  ${string}
   
   ===============  ==========================  =========
   
   

   




Split To Lines
==============
.. py:function:: split_to_lines(string, start=0, end=None)

   
      
   Splits the given string to lines.
   
   It is possible to get only a selection of lines from ``start``
   to ``end`` so that ``start`` index is inclusive and ``end`` is
   exclusive. Line numbering starts from 0, and it is possible to
   use negative indices to refer to lines from the end.
   
   Lines are returned without the newlines. The number of
   returned lines is automatically logged.
   
   Examples:
   
   
   =================  ==============  ============  ==  ==
   @{lines} =         Split To Lines  ${manylines}        
   @{ignore first} =  Split To Lines  ${manylines}  1     
   @{ignore last} =   Split To Lines  ${manylines}      -1
   @{5th to 10th} =   Split To Lines  ${manylines}  4   10
   @{first two} =     Split To Lines  ${manylines}      1 
   @{last two} =      Split To Lines  ${manylines}  -2    
   
   =================  ==============  ============  ==  ==
   
   
   
   Use `Get Line` if you only need to get a single line.

   




Strip String
============
.. py:function:: strip_string(string, mode=both, characters=None)

   
      
   Remove leading and/or trailing whitespaces from the given string.
   
   ``mode`` is either ``left`` to remove leading characters, ``right`` to
   remove trailing characters, ``both`` (default) to remove the
   characters from both sides of the string or ``none`` to return the
   unmodified string.
   
   If the optional ``characters`` is given, it must be a string and the
   characters in the string will be stripped in the string. Please note,
   that this is not a substring to be removed but a list of characters,
   see the example below.
   
   Examples:
   
   
   ===============  ============  =====================  ==============
   ${stripped}=     Strip String  ${SPACE}Hello${SPACE}                
   Should Be Equal  ${stripped}   Hello                                
   ${stripped}=     Strip String  ${SPACE}Hello${SPACE}  mode=left     
   Should Be Equal  ${stripped}   Hello${SPACE}                        
   ${stripped}=     Strip String  aabaHelloeee           characters=abe
   Should Be Equal  ${stripped}   Hello                                
   
   ===============  ============  =====================  ==============
   
   
   
   New in Robot Framework 3.0.

   



