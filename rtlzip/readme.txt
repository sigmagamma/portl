This is an alpha version. By following these instructions you acknowledge you are responsible for doing so.
Installation instructions:
Assuming C:\Program Files (x86)\Steam\steamapps\common\Portal\ is the game folder:

1. If you've installed a previous Hebrew into the game folder, remove it and restore any backups from the English version, specifically deleting closecaption_hebrew.dat (and if you overwrote portal_english.txt, that as well).
2. Go to the Portal\portal\resource folder and rename portal_english.txt .
3. Create a folder called Portal\portal\custom and place the contents of the zip under it.
4. It is assumed you're running Windows 10 with Hebrew support, meaning your default system Hebrew font is Tahoma.
5. *** The following changes the display font for your entire system. *** Run applyfonts.reg to change the default font to Miriam Fixed. Restart your PC.
6. When you start the game, set the game resolution to 1366 * 768 (higher resolutions might work as well, but the subtitles aren't as readable)


In order to uninstall:
1. Remove the custom\portl folder 
2. Rename the backup of resource\portal_english.txt back
3. Remember to run removefonts.reg file and restart Windows.
