import os

current_script_path = os.path.abspath(__file__)
print("Путь к текущему скрипту:", current_script_path)

current_script_directory = os.path.dirname(os.path.abspath(__file__))
print("Директория текущего скрипта:", current_script_directory)