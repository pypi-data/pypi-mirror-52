import os

# Sets a project's working directory.
# Looks for a file named .anchor in the current directory. If it can't
# find one, go up one level and look again. Keep looking until the file
# is found or the recursion limit is reached.
def set_anchor(starting_point = os.getcwd()):
    dirs = []

    path = starting_point

    while True:
        names = os.listdir(path)
        for name in names:
            if name == '.anchor':
                print('Found anchor file.')
                print(f'Setting working directory to {path}.')
                os.chdir(path)
                return 1
        else:
            path = os.path.realpath(os.path.join(path, '..'))
            if path == starting_point:
                print('Reached recursion limit without finding anchor file.')
                return 0
