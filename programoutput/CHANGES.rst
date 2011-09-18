0.5 (in development)
====================

- :confval:`programoutput_prompt_template` is interpreted as format string now!
- Require Python 2.6 now
- Added ``returncode`` option to :rst:dir:`program-output` (thanks to Jan-Marek
  Glogowski)
- Support ``returncode`` formatting key in
  :confval:`programoutput_prompt_template`
- Warn on unexpected return codes instead of raising
  :exc:`~subprocess.CalledProcessError`


0.4.1 (Mar 11, 2011)
====================

- Some source code cleanups
- #10: Fixed installation instructions in documentation


0.4 (May 21, 2010)
==================

- Initial release
