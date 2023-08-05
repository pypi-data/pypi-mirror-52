
========================
library: OperatingSystem
========================

:scope: global
:generated: 20190903 12:31:55


A test library providing keywords for OS related tasks.

``OperatingSystem`` is Robot Framework's standard library that
enables various operating system related tasks to be performed in
the system where Robot Framework is running. It can, among other
things, execute commands (e.g. `Run`), create and remove files and
directories (e.g. `Create File`, `Remove Directory`), check
whether files or directories exists or contain something
(e.g. `File Should Exist`, `Directory Should Be Empty`) and
manipulate environment variables (e.g. `Set Environment Variable`).

== Table of contents ==

- `Path separators`
- `Pattern matching`
- `Tilde expansion`
- `Boolean arguments`
- `Example`
- `Shortcuts`
- `Keywords`

= Path separators =

Because Robot Framework uses the backslash (``\``) as an escape character
in the test data, using a literal backslash requires duplicating it like
in ``c:\\path\\file.txt``. That can be inconvenient especially with
longer Windows paths, and thus all keywords expecting paths as arguments
convert forward slashes to backslashes automatically on Windows. This also
means that paths like ``${CURDIR}/path/file.txt`` are operating system
independent.

Notice that the automatic path separator conversion does not work if
the path is only a part of an argument like with `Run` and `Start Process`
keywords. In these cases the built-in variable ``${/}`` that contains
``\`` or ``/``, depending on the operating system, can be used instead.

= Pattern matching =

Some keywords allow their arguments to be specified as
[http://en.wikipedia.org/wiki/Glob_(programming)|glob patterns] where:



============  =======================================================
``*``         matches any string, even an empty string               
``?``         matches any single character                           
``[chars]``   matches one character in the bracket                   
``[!chars]``  matches one character not in the bracket               
``[a-z]``     matches one character from the range in the bracket    
``[!a-z]``    matches one character not from the range in the bracket

============  =======================================================



Unless otherwise noted, matching is case-insensitive on
case-insensitive operating systems such as Windows.

Starting from Robot Framework 2.9.1, globbing is not done if the given path
matches an existing file even if it would contain a glob pattern.

= Tilde expansion =

Paths beginning with ``~`` or ``~username`` are expanded to the current or
specified user's home directory, respectively. The resulting path is
operating system dependent, but typically e.g. ``~/robot`` is expanded to
``C:\Users\<user>\robot`` on Windows and ``/home/<user>/robot`` on
Unixes.

The ``~username`` form does not work on Jython.

= Boolean arguments =

Some keywords accept arguments that are handled as Boolean values true or
false. If such an argument is given as a string, it is considered false if
it is an empty string or equal to ``FALSE``, ``NONE``, ``NO``, ``OFF`` or
``0``, case-insensitively. Other strings are considered true regardless
their value, and other argument types are tested using the same
[http://docs.python.org/library/stdtypes.html#truth|rules as in Python].

True examples:


==================  =======  =================  ================================
`Remove Directory`  ${path}  recursive=True     # Strings are generally true.   
`Remove Directory`  ${path}  recursive=yes      # Same as the above.            
`Remove Directory`  ${path}  recursive=${TRUE}  # Python ``True`` is true.      
`Remove Directory`  ${path}  recursive=${42}    # Numbers other than 0 are true.

==================  =======  =================  ================================



False examples:


==================  =======  ==================  ==============================
`Remove Directory`  ${path}  recursive=False     # String ``false`` is false.  
`Remove Directory`  ${path}  recursive=no        # Also string ``no`` is false.
`Remove Directory`  ${path}  recursive=${EMPTY}  # Empty string is false.      
`Remove Directory`  ${path}  recursive=${FALSE}  # Python ``False`` is false.  

==================  =======  ==================  ==============================



Considering string ``NONE`` false is new in Robot Framework 3.0.3 and
considering also ``OFF`` and ``0`` false is new in Robot Framework 3.1.

= Example =



=========  ===============
=Setting=  =Value=        
Library    OperatingSystem

=========  ===============





==========  =====================
=Variable=  =Value=              
${PATH}     ${CURDIR}/example.txt

==========  =====================





===========  =================  ==========  ===========================
=Test Case=  =Action=           =Argument=  =Argument=                 
Example      Create File        ${PATH}     Some text                  
             File Should Exist  ${PATH}                                
             Copy File          ${PATH}     ~/file.txt                 
             ${output} =        Run         ${TEMPDIR}${/}script.py arg

===========  =================  ==========  ===========================







Append To Environment Variable
==============================
.. py:function:: append_to_environment_variable(name, *values, **config)

   
      
   Appends given ``values`` to environment variable ``name``.
   
   If the environment variable already exists, values are added after it,
   and otherwise a new environment variable is created.
   
   Values are, by default, joined together using the operating system
   path separator (``;`` on Windows, ``:`` elsewhere). This can be changed
   by giving a separator after the values like ``separator=value``. No
   other configuration parameters are accepted.
   
   Examples (assuming ``NAME`` and ``NAME2`` do not exist initially):
   
   
   ==============================  ========  ========================  ===========
   Append To Environment Variable  NAME      first                                
   Should Be Equal                 %{NAME}   first                                
   Append To Environment Variable  NAME      second                    third      
   Should Be Equal                 %{NAME}   first${:}second${:}third             
   Append To Environment Variable  NAME2     first                     separator=-
   Should Be Equal                 %{NAME2}  first                                
   Append To Environment Variable  NAME2     second                    separator=-
   Should Be Equal                 %{NAME2}  first-second                         
   
   ==============================  ========  ========================  ===========
   
   

   




Append To File
==============
.. py:function:: append_to_file(path, content, encoding=UTF-8)

   
      
   Appends the given content to the specified file.
   
   If the file exists, the given text is written to its end. If the file
   does not exist, it is created.
   
   Other than not overwriting possible existing files, this keyword works
   exactly like `Create File`. See its documentation for more details
   about the usage.
   
   Note that special encodings ``SYSTEM`` and ``CONSOLE`` only work
   with this keyword starting from Robot Framework 3.1.2.

   




Copy Directory
==============
.. py:function:: copy_directory(source, destination)

   
      
   Copies the source directory into the destination.
   
   If the destination exists, the source is copied under it. Otherwise
   the destination directory and the possible missing intermediate
   directories are created.

   




Copy File
=========
.. py:function:: copy_file(source, destination)

   
      
   Copies the source file into the destination.
   
   Source must be a path to an existing file or a glob pattern (see
   `Pattern matching`) that matches exactly one file. How the
   destination is interpreted is explained below.
   
   1) If the destination is an existing file, the source file is copied
   over it.
   
   2) If the destination is an existing directory, the source file is
   copied into it. A possible file with the same name as the source is
   overwritten.
   
   3) If the destination does not exist and it ends with a path
   separator (``/`` or ``\``), it is considered a directory. That
   directory is created and a source file copied into it.
   Possible missing intermediate directories are also created.
   
   4) If the destination does not exist and it does not end with a path
   separator, it is considered a file. If the path to the file does not
   exist, it is created.
   
   The resulting destination path is returned since Robot Framework 2.9.2.
   
   See also `Copy Files`, `Move File`, and `Move Files`.

   




Copy Files
==========
.. py:function:: copy_files(*sources_and_destination)

   
      
   Copies specified files to the target directory.
   
   Source files can be given as exact paths and as glob patterns (see
   `Pattern matching`). At least one source must be given, but it is
   not an error if it is a pattern that does not match anything.
   
   Last argument must be the destination directory. If the destination
   does not exist, it will be created.
   
   Examples:
   
   
   ==========  =================  ================  =======
   Copy Files  ${dir}/file1.txt   ${dir}/file2.txt  ${dir2}
   Copy Files  ${dir}/file-*.txt  ${dir2}                  
   
   ==========  =================  ================  =======
   
   
   
   See also `Copy File`, `Move File`, and `Move Files`.

   




Count Directories In Directory
==============================
.. py:function:: count_directories_in_directory(path, pattern=None)

   
      
   Wrapper for `Count Items In Directory` returning only directory count.

   




Count Files In Directory
========================
.. py:function:: count_files_in_directory(path, pattern=None)

   
      
   Wrapper for `Count Items In Directory` returning only file count.

   




Count Items In Directory
========================
.. py:function:: count_items_in_directory(path, pattern=None)

   
      
   Returns and logs the number of all items in the given directory.
   
   The argument ``pattern`` has the same semantics as with `List Directory`
   keyword. The count is returned as an integer, so it must be checked e.g.
   with the built-in keyword `Should Be Equal As Integers`.

   




Create Binary File
==================
.. py:function:: create_binary_file(path, content)

   
      
   Creates a binary file with the given content.
   
   If content is given as a Unicode string, it is first converted to bytes
   character by character. All characters with ordinal below 256 can be
   used and are converted to bytes with same values. Using characters
   with higher ordinal is an error.
   
   Byte strings, and possible other types, are written to the file as is.
   
   If the directory for the file does not exist, it is created, along
   with missing intermediate directories.
   
   Examples:
   
   
   ==================  ==================  ================
   Create Binary File  ${dir}/example.png  ${image content}
   Create Binary File  ${path}             \x01\x00\xe4\x00
   
   ==================  ==================  ================
   
   
   
   Use `Create File` if you want to create a text file using a certain
   encoding. `File Should Not Exist` can be used to avoid overwriting
   existing files.

   




Create Directory
================
.. py:function:: create_directory(path)

   
      
   Creates the specified directory.
   
   Also possible intermediate directories are created. Passes if the
   directory already exists, but fails if the path exists and is not
   a directory.

   




Create File
===========
.. py:function:: create_file(path, content=, encoding=UTF-8)

   
      
   Creates a file with the given content and encoding.
   
   If the directory where the file is created does not exist, it is
   automatically created along with possible missing intermediate
   directories. Possible existing file is overwritten.
   
   On Windows newline characters (``\n``) in content are automatically
   converted to Windows native newline sequence (``\r\n``).
   
   See `Get File` for more information about possible ``encoding`` values,
   including special values ``SYSTEM`` and ``CONSOLE``.
   
   Examples:
   
   
   ===========  ==================  =================  =======
   Create File  ${dir}/example.txt  Hello, world!             
   Create File  ${path}             Hyv\xe4 esimerkki  Latin-1
   Create File  /tmp/foo.txt        3\nlines\nhere\n   SYSTEM 
   
   ===========  ==================  =================  =======
   
   
   
   Use `Append To File` if you want to append to an existing file
   and `Create Binary File` if you need to write bytes without encoding.
   `File Should Not Exist` can be used to avoid overwriting existing
   files.
   
   The support for ``SYSTEM`` and ``CONSOLE`` encodings is new in Robot
   Framework 3.0. Automatically converting ``\n`` to ``\r\n`` on
   Windows is new in Robot Framework 3.1.

   




Directory Should Be Empty
=========================
.. py:function:: directory_should_be_empty(path, msg=None)

   
      
   Fails unless the specified directory is empty.
   
   The default error message can be overridden with the ``msg`` argument.

   




Directory Should Exist
======================
.. py:function:: directory_should_exist(path, msg=None)

   
      
   Fails unless the given path points to an existing directory.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   The default error message can be overridden with the ``msg`` argument.

   




Directory Should Not Be Empty
=============================
.. py:function:: directory_should_not_be_empty(path, msg=None)

   
      
   Fails if the specified directory is empty.
   
   The default error message can be overridden with the ``msg`` argument.

   




Directory Should Not Exist
==========================
.. py:function:: directory_should_not_exist(path, msg=None)

   
      
   Fails if the given path points to an existing file.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   The default error message can be overridden with the ``msg`` argument.

   




Empty Directory
===============
.. py:function:: empty_directory(path)

   
      
   Deletes all the content from the given directory.
   
   Deletes both files and sub-directories, but the specified directory
   itself if not removed. Use `Remove Directory` if you want to remove
   the whole directory.

   




Environment Variable Should Be Set
==================================
.. py:function:: environment_variable_should_be_set(name, msg=None)

   
      
   Fails if the specified environment variable is not set.
   
   The default error message can be overridden with the ``msg`` argument.

   




Environment Variable Should Not Be Set
======================================
.. py:function:: environment_variable_should_not_be_set(name, msg=None)

   
      
   Fails if the specified environment variable is set.
   
   The default error message can be overridden with the ``msg`` argument.

   




File Should Be Empty
====================
.. py:function:: file_should_be_empty(path, msg=None)

   
      
   Fails unless the specified file is empty.
   
   The default error message can be overridden with the ``msg`` argument.

   




File Should Exist
=================
.. py:function:: file_should_exist(path, msg=None)

   
      
   Fails unless the given ``path`` points to an existing file.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   The default error message can be overridden with the ``msg`` argument.

   




File Should Not Be Empty
========================
.. py:function:: file_should_not_be_empty(path, msg=None)

   
      
   Fails if the specified directory is empty.
   
   The default error message can be overridden with the ``msg`` argument.

   




File Should Not Exist
=====================
.. py:function:: file_should_not_exist(path, msg=None)

   
      
   Fails if the given path points to an existing file.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   The default error message can be overridden with the ``msg`` argument.

   




Get Binary File
===============
.. py:function:: get_binary_file(path)

   
      
   Returns the contents of a specified file.
   
   This keyword reads the specified file and returns the contents as is.
   See also `Get File`.

   




Get Environment Variable
========================
.. py:function:: get_environment_variable(name, default=None)

   
      
   Returns the value of an environment variable with the given name.
   
   If no such environment variable is set, returns the default value, if
   given. Otherwise fails the test case.
   
   Returned variables are automatically decoded to Unicode using
   the system encoding.
   
   Note that you can also access environment variables directly using
   the variable syntax ``%{ENV_VAR_NAME}``.

   




Get Environment Variables
=========================
.. py:function:: get_environment_variables()

   
      
   Returns currently available environment variables as a dictionary.
   
   Both keys and values are decoded to Unicode using the system encoding.
   Altering the returned dictionary has no effect on the actual environment
   variables.

   




Get File
========
.. py:function:: get_file(path, encoding=UTF-8, encoding_errors=strict)

   
      
   Returns the contents of a specified file.
   
   This keyword reads the specified file and returns the contents.
   Line breaks in content are converted to platform independent form.
   See also `Get Binary File`.
   
   ``encoding`` defines the encoding of the file. The default value is
   ``UTF-8``, which means that UTF-8 and ASCII encoded files are read
   correctly. In addition to the encodings supported by the underlying
   Python implementation, the following special encoding values can be
   used:
   
   - ``SYSTEM``: Use the default system encoding.
   - ``CONSOLE``: Use the console encoding. Outside Windows this is same
     as the system encoding.
   
   ``encoding_errors`` argument controls what to do if decoding some bytes
   fails. All values accepted by ``decode`` method in Python are valid, but
   in practice the following values are most useful:
   
   - ``strict``: Fail if characters cannot be decoded (default).
   - ``ignore``: Ignore characters that cannot be decoded.
   - ``replace``: Replace characters that cannot be decoded with
     a replacement character.
   
   Support for ``SYSTEM`` and ``CONSOLE`` encodings in Robot Framework 3.0.

   




Get File Size
=============
.. py:function:: get_file_size(path)

   
      
   Returns and logs file size as an integer in bytes.

   




Get Modified Time
=================
.. py:function:: get_modified_time(path, format=timestamp)

   
      
   Returns the last modification time of a file or directory.
   
   How time is returned is determined based on the given ``format``
   string as follows. Note that all checks are case-insensitive.
   Returned time is also automatically logged.
   
   1) If ``format`` contains the word ``epoch``, the time is returned
      in seconds after the UNIX epoch. The return value is always
      an integer.
   
   2) If ``format`` contains any of the words ``year``, ``month``,
      ``day``, ``hour``, ``min`` or ``sec``, only the selected parts are
      returned. The order of the returned parts is always the one
      in the previous sentence and the order of the words in
      ``format`` is not significant. The parts are returned as
      zero-padded strings (e.g. May -> ``05``).
   
   3) Otherwise, and by default, the time is returned as a
      timestamp string in the format ``2006-02-24 15:08:31``.
   
   Examples (when the modified time of ``${CURDIR}`` is
   2006-03-29 15:06:21):
   
   
   =========  =================  =================  ===========================  ========
   ${time} =  Get Modified Time  ${CURDIR}                                               
   ${secs} =  Get Modified Time  ${CURDIR}          epoch                                
   ${year} =  Get Modified Time  ${CURDIR}          return year                          
   ${y}       ${d} =             Get Modified Time  ${CURDIR}                    year,day
   @{time} =  Get Modified Time  ${CURDIR}          year,month,day,hour,min,sec          
   
   =========  =================  =================  ===========================  ========
   
   
   =>
   - ${time} = '2006-03-29 15:06:21'
   - ${secs} = 1143637581
   - ${year} = '2006'
   - ${y} = '2006' & ${d} = '29'
   - @{time} = ['2006', '03', '29', '15', '06', '21']

   




Grep File
=========
.. py:function:: grep_file(path, pattern, encoding=UTF-8, encoding_errors=strict)

   
      
   Returns the lines of the specified file that match the ``pattern``.
   
   This keyword reads a file from the file system using the defined
   ``path``, ``encoding`` and ``encoding_errors`` similarly as `Get File`.
   A difference is that only the lines that match the given ``pattern`` are
   returned. Lines are returned as a single string catenated back together
   with newlines and the number of matched lines is automatically logged.
   Possible trailing newline is never returned.
   
   A line matches if it contains the ``pattern`` anywhere in it and
   it *does not need to match the pattern fully*. The pattern
   matching syntax is explained in `introduction`, and in this
   case matching is case-sensitive.
   
   Examples:
   
   
   ===========  =========  ==================  ==================
   ${errors} =  Grep File  /var/log/myapp.log  ERROR             
   ${ret} =     Grep File  ${CURDIR}/file.txt  [Ww]ildc??d ex*ple
   
   ===========  =========  ==================  ==================
   
   
   
   If more complex pattern matching is needed, it is possible to use
   `Get File` in combination with String library keywords like `Get
   Lines Matching Regexp`.

   




Join Path
=========
.. py:function:: join_path(base, *parts)

   
      
   Joins the given path part(s) to the given base path.
   
   The path separator (``/`` or ``\``) is inserted when needed and
   the possible absolute paths handled as expected. The resulted
   path is also normalized.
   
   Examples:
   
   
   =========  =========  =========  =====  =====  ========
   ${path} =  Join Path  my         path                  
   ${p2} =    Join Path  my/        path/                 
   ${p3} =    Join Path  my         path   my     file.txt
   ${p4} =    Join Path  my         /path                 
   ${p5} =    Join Path  /my/path/  ..     path2          
   
   =========  =========  =========  =====  =====  ========
   
   
   =>
   - ${path} = 'my/path'
   - ${p2} = 'my/path'
   - ${p3} = 'my/path/my/file.txt'
   - ${p4} = '/path'
   - ${p5} = '/my/path2'

   




Join Paths
==========
.. py:function:: join_paths(base, *paths)

   
      
   Joins given paths with base and returns resulted paths.
   
   See `Join Path` for more information.
   
   Examples:
   
   
   =======  ==========  ========  =============  =====  ========
   @{p1} =  Join Paths  base      example        other          
   @{p2} =  Join Paths  /my/base  /example       other          
   @{p3} =  Join Paths  my/base   example/path/  other  one/more
   
   =======  ==========  ========  =============  =====  ========
   
   
   =>
   - @{p1} = ['base/example', 'base/other']
   - @{p2} = ['/example', '/my/base/other']
   - @{p3} = ['my/base/example/path', 'my/base/other', 'my/base/one/more']

   




List Directories In Directory
=============================
.. py:function:: list_directories_in_directory(path, pattern=None, absolute=False)

   
      
   Wrapper for `List Directory` that returns only directories.

   




List Directory
==============
.. py:function:: list_directory(path, pattern=None, absolute=False)

   
      
   Returns and logs items in a directory, optionally filtered with ``pattern``.
   
   File and directory names are returned in case-sensitive alphabetical
   order, e.g. ``['A Name', 'Second', 'a lower case name', 'one more']``.
   Implicit directories ``.`` and ``..`` are not returned. The returned
   items are automatically logged.
   
   File and directory names are returned relative to the given path
   (e.g. ``'file.txt'``) by default. If you want them be returned in
   absolute format (e.g. ``'/home/robot/file.txt'``), give the ``absolute``
   argument a true value (see `Boolean arguments`).
   
   If ``pattern`` is given, only items matching it are returned. The pattern
   matching syntax is explained in `introduction`, and in this case
   matching is case-sensitive.
   
   Examples (using also other `List Directory` variants):
   
   
   ==========  ========================  ==========  =====  ========
   @{items} =  List Directory            ${TEMPDIR}                 
   @{files} =  List Files In Directory   /tmp        *.txt  absolute
   ${count} =  Count Files In Directory  ${CURDIR}   ???            
   
   ==========  ========================  ==========  =====  ========
   
   

   




List Files In Directory
=======================
.. py:function:: list_files_in_directory(path, pattern=None, absolute=False)

   
      
   Wrapper for `List Directory` that returns only files.

   




Log Environment Variables
=========================
.. py:function:: log_environment_variables(level=INFO)

   
      
   Logs all environment variables using the given log level.
   
   Environment variables are also returned the same way as with
   `Get Environment Variables` keyword.

   




Log File
========
.. py:function:: log_file(path, encoding=UTF-8, encoding_errors=strict)

   
      
   Wrapper for `Get File` that also logs the returned file.
   
   The file is logged with the INFO level. If you want something else,
   just use `Get File` and the built-in keyword `Log` with the desired
   level.
   
   See `Get File` for more information about ``encoding`` and
   ``encoding_errors`` arguments.

   




Move Directory
==============
.. py:function:: move_directory(source, destination)

   
      
   Moves the source directory into a destination.
   
   Uses `Copy Directory` keyword internally, and ``source`` and
   ``destination`` arguments have exactly same semantics as with
   that keyword.

   




Move File
=========
.. py:function:: move_file(source, destination)

   
      
   Moves the source file into the destination.
   
   Arguments have exactly same semantics as with `Copy File` keyword.
   Destination file path is returned since Robot Framework 2.9.2.
   
   If the source and destination are on the same filesystem, rename
   operation is used. Otherwise file is copied to the destination
   filesystem and then removed from the original filesystem.
   
   See also `Move Files`, `Copy File`, and `Copy Files`.

   




Move Files
==========
.. py:function:: move_files(*sources_and_destination)

   
      
   Moves specified files to the target directory.
   
   Arguments have exactly same semantics as with `Copy Files` keyword.
   
   See also `Move File`, `Copy File`, and `Copy Files`.

   




Normalize Path
==============
.. py:function:: normalize_path(path, case_normalize=False)

   
      
   Normalizes the given path.
   
   - Collapses redundant separators and up-level references.
   - Converts ``/`` to ``\`` on Windows.
   - Replaces initial ``~`` or ``~user`` by that user's home directory.
     The latter is not supported on Jython.
   - If ``case_normalize`` is given a true value (see `Boolean arguments`)
     on Windows, converts the path to all lowercase. New in Robot
     Framework 3.1.
   
   Examples:
   
   
   ==========  ==============  ==============
   ${path1} =  Normalize Path  abc/          
   ${path2} =  Normalize Path  abc/../def    
   ${path3} =  Normalize Path  abc/./def//ghi
   ${path4} =  Normalize Path  ~robot/stuff  
   
   ==========  ==============  ==============
   
   
   =>
   - ${path1} = 'abc'
   - ${path2} = 'def'
   - ${path3} = 'abc/def/ghi'
   - ${path4} = '/home/robot/stuff'
   
   On Windows result would use ``\`` instead of ``/`` and home directory
   would be different.

   




Remove Directory
================
.. py:function:: remove_directory(path, recursive=False)

   
      
   Removes the directory pointed to by the given ``path``.
   
   If the second argument ``recursive`` is given a true value (see
   `Boolean arguments`), the directory is removed recursively. Otherwise
   removing fails if the directory is not empty.
   
   If the directory pointed to by the ``path`` does not exist, the keyword
   passes, but it fails, if the ``path`` points to a file.

   




Remove Environment Variable
===========================
.. py:function:: remove_environment_variable(*names)

   
      
   Deletes the specified environment variable.
   
   Does nothing if the environment variable is not set.
   
   It is possible to remove multiple variables by passing them to this
   keyword as separate arguments.

   




Remove File
===========
.. py:function:: remove_file(path)

   
      
   Removes a file with the given path.
   
   Passes if the file does not exist, but fails if the path does
   not point to a regular file (e.g. it points to a directory).
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   If the path is a pattern, all files matching it are removed.

   




Remove Files
============
.. py:function:: remove_files(*paths)

   
      
   Uses `Remove File` to remove multiple files one-by-one.
   
   Example:
   
   
   ============  =====================  =====================  =====================
   Remove Files  ${TEMPDIR}${/}foo.txt  ${TEMPDIR}${/}bar.txt  ${TEMPDIR}${/}zap.txt
   
   ============  =====================  =====================  =====================
   
   

   




Run
===
.. py:function:: run(command)

   
      
   Runs the given command in the system and returns the output.
   
   The execution status of the command *is not checked* by this
   keyword, and it must be done separately based on the returned
   output. If the execution return code is needed, either `Run
   And Return RC` or `Run And Return RC And Output` can be used.
   
   The standard error stream is automatically redirected to the standard
   output stream by adding ``2>&1`` after the executed command. This
   automatic redirection is done only when the executed command does not
   contain additional output redirections. You can thus freely forward
   the standard error somewhere else, for example, like
   ``my_command 2>stderr.txt``.
   
   The returned output contains everything written into the standard
   output or error streams by the command (unless either of them
   is redirected explicitly). Many commands add an extra newline
   (``\n``) after the output to make it easier to read in the
   console. To ease processing the returned output, this possible
   trailing newline is stripped by this keyword.
   
   Examples:
   
   
   ====================  ===============  ================================
   ${output} =           Run              ls -lhF /tmp                    
   Log                   ${output}                                        
   ${result} =           Run              ${CURDIR}${/}tester.py arg1 arg2
   Should Not Contain    ${result}        FAIL                            
   ${stdout} =           Run              /opt/script.sh 2>/tmp/stderr.txt
   Should Be Equal       ${stdout}        TEST PASSED                     
   File Should Be Empty  /tmp/stderr.txt                                  
   
   ====================  ===============  ================================
   
   
   
   *TIP:* `Run Process` keyword provided by the
   [http://robotframework.org/robotframework/latest/libraries/Process.html|
   Process library] supports better process configuration and is generally
   recommended as a replacement for this keyword.

   




Run And Return Rc
=================
.. py:function:: run_and_return_rc(command)

   
      
   Runs the given command in the system and returns the return code.
   
   The return code (RC) is returned as a positive integer in
   range from 0 to 255 as returned by the executed command. On
   some operating systems (notable Windows) original return codes
   can be something else, but this keyword always maps them to
   the 0-255 range. Since the RC is an integer, it must be
   checked e.g. with the keyword `Should Be Equal As Integers`
   instead of `Should Be Equal` (both are built-in keywords).
   
   Examples:
   
   
   ===========================  =================  =============================
   ${rc} =                      Run and Return RC  ${CURDIR}${/}script.py arg   
   Should Be Equal As Integers  ${rc}              0                            
   ${rc} =                      Run and Return RC  /path/to/example.rb arg1 arg2
   Should Be True               0 < ${rc} < 42                                  
   
   ===========================  =================  =============================
   
   
   
   See `Run` and `Run And Return RC And Output` if you need to get the
   output of the executed command.
   
   *TIP:* `Run Process` keyword provided by the
   [http://robotframework.org/robotframework/latest/libraries/Process.html|
   Process library] supports better process configuration and is generally
   recommended as a replacement for this keyword.

   




Run And Return Rc And Output
============================
.. py:function:: run_and_return_rc_and_output(command)

   
      
   Runs the given command in the system and returns the RC and output.
   
   The return code (RC) is returned similarly as with `Run And Return RC`
   and the output similarly as with `Run`.
   
   Examples:
   
   
   ===========================  ===============  ============================  ================================
   ${rc}                        ${output} =      Run and Return RC and Output  ${CURDIR}${/}mytool             
   Should Be Equal As Integers  ${rc}            0                                                             
   Should Not Contain           ${output}        FAIL                                                          
   ${rc}                        ${stdout} =      Run and Return RC and Output  /opt/script.sh 2>/tmp/stderr.txt
   Should Be True               ${rc} > 42                                                                     
   Should Be Equal              ${stdout}        TEST PASSED                                                   
   File Should Be Empty         /tmp/stderr.txt                                                                
   
   ===========================  ===============  ============================  ================================
   
   
   
   *TIP:* `Run Process` keyword provided by the
   [http://robotframework.org/robotframework/latest/libraries/Process.html|
   Process library] supports better process configuration and is generally
   recommended as a replacement for this keyword.

   




Set Environment Variable
========================
.. py:function:: set_environment_variable(name, value)

   
      
   Sets an environment variable to a specified value.
   
   Values are converted to strings automatically. Set variables are
   automatically encoded using the system encoding.

   




Set Modified Time
=================
.. py:function:: set_modified_time(path, mtime)

   
      
   Sets the file modification and access times.
   
   Changes the modification and access times of the given file to
   the value determined by ``mtime``. The time can be given in
   different formats described below. Note that all checks
   involving strings are case-insensitive. Modified time can only
   be set to regular files.
   
   1) If ``mtime`` is a number, or a string that can be converted
      to a number, it is interpreted as seconds since the UNIX
      epoch (1970-01-01 00:00:00 UTC). This documentation was
      originally written about 1177654467 seconds after the epoch.
   
   2) If ``mtime`` is a timestamp, that time will be used. Valid
      timestamp formats are ``YYYY-MM-DD hh:mm:ss`` and
      ``YYYYMMDD hhmmss``.
   
   3) If ``mtime`` is equal to ``NOW``, the current local time is used.
   
   4) If ``mtime`` is equal to ``UTC``, the current time in
      [http://en.wikipedia.org/wiki/Coordinated_Universal_Time|UTC]
      is used.
   
   5) If ``mtime`` is in the format like ``NOW - 1 day`` or ``UTC + 1
      hour 30 min``, the current local/UTC time plus/minus the time
      specified with the time string is used. The time string format
      is described in an appendix of Robot Framework User Guide.
   
   Examples:
   
   
   =================  ==========  ==================  ======================================
   Set Modified Time  /path/file  1177654467          # Time given as epoch seconds         
   Set Modified Time  /path/file  2007-04-27 9:14:27  # Time given as a timestamp           
   Set Modified Time  /path/file  NOW                 # The local time of execution         
   Set Modified Time  /path/file  NOW - 1 day         # 1 day subtracted from the local time
   Set Modified Time  /path/file  UTC + 1h 2min 3s    # 1h 2min 3s added to the UTC time    
   
   =================  ==========  ==================  ======================================
   
   

   




Should Exist
============
.. py:function:: should_exist(path, msg=None)

   
      
   Fails unless the given path (file or directory) exists.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   The default error message can be overridden with the ``msg`` argument.

   




Should Not Exist
================
.. py:function:: should_not_exist(path, msg=None)

   
      
   Fails if the given path (file or directory) exists.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   The default error message can be overridden with the ``msg`` argument.

   




Split Extension
===============
.. py:function:: split_extension(path)

   
      
   Splits the extension from the given path.
   
   The given path is first normalized (e.g. possible trailing
   path separators removed, special directories ``..`` and ``.``
   removed). The base path and extension are returned as separate
   components so that the dot used as an extension separator is
   removed. If the path contains no extension, an empty string is
   returned for it. Possible leading and trailing dots in the file
   name are never considered to be extension separators.
   
   Examples:
   
   
   =======  ========  ===============  =================
   ${path}  ${ext} =  Split Extension  file.extension   
   ${p2}    ${e2} =   Split Extension  path/file.ext    
   ${p3}    ${e3} =   Split Extension  path/file        
   ${p4}    ${e4} =   Split Extension  p1/../p2/file.ext
   ${p5}    ${e5} =   Split Extension  path/.file.ext   
   ${p6}    ${e6} =   Split Extension  path/.file       
   
   =======  ========  ===============  =================
   
   
   =>
   - ${path} = 'file' & ${ext} = 'extension'
   - ${p2} = 'path/file' & ${e2} = 'ext'
   - ${p3} = 'path/file' & ${e3} = ''
   - ${p4} = 'p2/file' & ${e4} = 'ext'
   - ${p5} = 'path/.file' & ${e5} = 'ext'
   - ${p6} = 'path/.file' & ${e6} = ''

   




Split Path
==========
.. py:function:: split_path(path)

   
      
   Splits the given path from the last path separator (``/`` or ``\``).
   
   The given path is first normalized (e.g. a possible trailing
   path separator is removed, special directories ``..`` and ``.``
   removed). The parts that are split are returned as separate
   components.
   
   Examples:
   
   
   ========  =========  ==========  ===============
   ${path1}  ${dir} =   Split Path  abc/def        
   ${path2}  ${file} =  Split Path  abc/def/ghi.txt
   ${path3}  ${d2}  =   Split Path  abc/../def/ghi/
   
   ========  =========  ==========  ===============
   
   
   =>
   - ${path1} = 'abc' & ${dir} = 'def'
   - ${path2} = 'abc/def' & ${file} = 'ghi.txt'
   - ${path3} = 'def' & ${d2} = 'ghi'

   




Touch
=====
.. py:function:: touch(path)

   
      
   Emulates the UNIX touch command.
   
   Creates a file, if it does not exist. Otherwise changes its access and
   modification times to the current time.
   
   Fails if used with the directories or the parent directory of the given
   file does not exist.

   




Wait Until Created
==================
.. py:function:: wait_until_created(path, timeout=1 minute)

   
      
   Waits until the given file or directory is created.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   If the path is a pattern, the keyword returns when an item matching
   it is created.
   
   The optional ``timeout`` can be used to control the maximum time of
   waiting. The timeout is given as a timeout string, e.g. in a format
   ``15 seconds``, ``1min 10s`` or just ``10``. The time string format is
   described in an appendix of Robot Framework User Guide.
   
   If the timeout is negative, the keyword is never timed-out. The keyword
   returns immediately, if the path already exists.

   




Wait Until Removed
==================
.. py:function:: wait_until_removed(path, timeout=1 minute)

   
      
   Waits until the given file or directory is removed.
   
   The path can be given as an exact path or as a glob pattern.
   The pattern matching syntax is explained in `introduction`.
   If the path is a pattern, the keyword waits until all matching
   items are removed.
   
   The optional ``timeout`` can be used to control the maximum time of
   waiting. The timeout is given as a timeout string, e.g. in a format
   ``15 seconds``, ``1min 10s`` or just ``10``. The time string format is
   described in an appendix of Robot Framework User Guide.
   
   If the timeout is negative, the keyword is never timed-out. The keyword
   returns immediately, if the path does not exist in the first place.

   



