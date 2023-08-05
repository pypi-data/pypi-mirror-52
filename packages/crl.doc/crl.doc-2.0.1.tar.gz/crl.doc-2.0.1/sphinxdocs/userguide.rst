.. copyright (C) 2019, Nokia

User Guide
==========

Generation of documentation with the tool
-----------------------------------------

The procedure for generating the documentation is the following

    - Create directory *sphinxdocs*.

    - Install packages you like to be documented

    - Run the command::

        # crl_doc_generate_rst (builtin, api and crl documentation)
        # crl_doc_generate_rst -d builtin -d crl (only builtin and crl documentation)



The documentation reStructuredText source is generated under *sphinxdocs*
directory in the following fashion:

   - *sphinxdocs/builtin*:  Robot Framework built-in reStructuredText source
     files

   - *sphinxdocs/crl*: Common Robot Libraries Robot Framework keyword
     documentation reStructuredText source files.

Generation of HTML documentation
--------------------------------

Please use the following procedure to generate HTML documentation:

   - create Sphinx configuration *conf.py* and *index.rst* so that it links to
     the sources described above.

   - Run *sphinx-build*.
