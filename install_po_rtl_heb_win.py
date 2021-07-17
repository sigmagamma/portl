import file_tools as ft
answer = input("This is an alpha version. Press y to acknowledge you are responsible for running this.")
if answer == "y":
    ft.write_files(ft.steam_path_windows(), 'hebrew')
