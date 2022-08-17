from src.file_tools import FileTools
def install_stanley(filename,language,store):
    answer = input("This is an beta version. By proceeding you acknowledge you are responsible for running this. Press y to install, u to uninstall, any other key to quit")
    try:
        if answer in ['y','u']:
            print('Please select folder. This may appear in a separate window.')
        if answer == 'y':
            ft = FileTools(filename, language,'m',store)
            ft.write_patch_files()
        elif answer == 'u':
            ft = FileTools(filename,language,store)
            ft.remove_mod()
    except Exception as e:
        input("installer crashed with an error:\n"+str(e))
        exit()
    if answer in ['y','u']:
        input("Done, press any key to quit.")

