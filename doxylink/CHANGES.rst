0.4 (In Development)
====================

- Allow URLs as base paths for the HTML links.
- Don't append parentheses if the user has provided them already in their query.

0.3 (Aug 10, 2010)
====================

- Only parse the tag file once per run. This should increase the speed.
- Automatically add parentheses to functions if the add_function_parentheses config variable is set.

0.2 (Jul 31, 2010)
====================

- When a target cannot be found, make the node an `inline` node so there's no link created.
- No longer require a trailing slash on the `doxylink` config variable HTML link path.
- Allow doxylinks to work correctly when created from a documentation subdirectory.

0.1 (Jul 22, 2010)
==================

- Initial release
