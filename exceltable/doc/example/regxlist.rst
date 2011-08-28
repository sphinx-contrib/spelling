
This is an example document that uses the ``regxlist`` directive. One of the 
most obvious use cases is the release notes and generating the list of bug
fixes.
 
**Release X**

Features:

  .. regxlist:: Added:\s*(.*)
     :siblings:
     :levelsup: 2
     :template: FEAT: ${0}

Bug fixes:

  .. regxlist:: Fixed (#\d+)(:\s*)(?P<desc>.*)
     :siblings:
     :levelsup: 2
     :template: BUG: ${desc} (${0})
   

All changes:

  - Fixed #2345: Crash while loading invalid document
  - Fixed #3454: Configuration parameter is missing
  - Added: Support for Vista
  - Changed default configuration parameter for ``show_version`` to ``False`` 

