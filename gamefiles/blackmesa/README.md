
## Development setup - Black Mesa Hebrew
The following part is relevant to developers who want to work on the game translation.
1. Get Black Mesa:
https://store.steampowered.com/app/362890/Black_Mesa/
2. Install Python 3.11 
3. Get an IDE for editing python such as [Pycharm](https://www.jetbrains.com/pycharm/). Notice to install the community edition.
4. git clone https://github.com/sigmagamma/portl.git . Don't use target folders that have spaces in them.
5. Open a project in the created folder, create a virtual environment, switch to branch feat-infraת and install the requirements from 
requirements.txt. 
6. You will need a separately distributed file named The `gamefiles/blackmesa/Black Mesa Hebrew RTL private.json` including the 
link to the translation sheet.
7. Make sure you have the correct dll files in place for Hebrew to show correctly.
8. `text_tools.py` contains the text transformation logic, while `file_tools.py` contains filesystem logistics. 
`src/blackmesa/install_unattended.py` has the various installation functions, `hebrew_rtl_install` is probably what you need. 
Make sure the working directory is above gamefiles. (the main project folder)
9. packmod_testers.bat produces the testers executable. 