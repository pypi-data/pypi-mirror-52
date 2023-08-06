
pandoc-xnos 2.0.0
=================

*pandoc-xnos* provides library code for the pandoc-[fignos]/[eqnos]/[tablenos] filters.

I am pleased to receive bug reports and feature requests on the project's [Issues tracker].

[pandocfilters]: https://github.com/jgm/pandocfilters
[fignos]: https://github.com/tomduck/pandoc-fignos
[eqnos]: https://github.com/tomduck/pandoc-eqnos
[tablenos]: https://github.com/tomduck/pandoc-tablenos
[Issues tracker]: https://github.com/tomduck/pandocfiltering/issues


Overview
--------

Below is a short summary of what is available.  More details are
given in the function docstrings.

#### Globals ####

  * `STRTYPES` - a list of string types for this python version
  * `STDIN`/`STDOUT`/`STDERR` - streams for use with pandoc

#### Utility functions ####

  * `init()` - Determines and returns the pandoc version
  * `check_bool()` - Used to check if a variable is boolean
  * `get_meta()` - Retrieves variables from a document's metadata

#### Element list functions ####

  * `quotify()` - Changes Quoted elements to quoted strings
  * `dollarfy()` - Changes Math elements to dollared strings
  * `extract_attrs()` - Extracts attribute strings

#### Actions and their factory functions ####

  * `join_strings()` - Joins adjacent strings in a pandoc document
  * `repair_refs()` - Repairs broken Cite elements in a document
  * `process_refs_factory()` - Makes functions that process
                               references
  * `replace_refs_factory()` - Makes functions that replace refs with
                               format-specific content
  * `attach_attrs_factory()` - Makes functions that attach attributes
                               to elements
  * `detach_attrs_factory()` - Makes functions that detach attributes
                               from elements
  * `insert_secnos_factory()` - Makes functions that insert section
                                numbers into attributes
  * `delete_secnos_factory()` - Makes functions that delete section
                                numbers from attributes
  * `insert_rawblocks_factory()` - Makes function to insert
                                   non-duplicate RawBlock elements.
