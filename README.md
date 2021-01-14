# iMusic

Application made as a project for my Databses class. It uses an Oracle database to emulate an audio-streaming service.
Users can make accounts and add money funds to them, they can view a list of available music albums, sort them by artist or view the songs separately.
Each user has a personal album collection where he can add albums by buying them, with the option to refund any album later.

**Implementation details:**
 * the code is written in PEP 8 compliant `python 3` and uses type hints as much as possible
 * using `tkinter` for the grafical interface
 * using `pbkdf2`, a cryprographic key derivation function for secure hashing of user passwords
 * communication with an Oracle database using `cx_Oracle`
 * logging messages with `logging` and handling database errors
 * parsing customized command line argumets using `argparse`
 * using `threading` to run complex computational tasks like iterative hashing in a separate background thread
