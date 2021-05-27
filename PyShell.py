import os
import shutil
import subprocess
import pickle

# +-------------------------------------------+
# | DRIVER FUNCTIONS FOR IDENTIFYING COMMANDS |
# +-------------------------------------------+

curpath = os.getcwd()
saveTo = os.path.dirname(__file__)

def main():
    isPy = False
    while 1:
        if not isPy:
            curpath = os.getcwd()
            command = input(f'PYSH | {curpath} | $ ')
            command = command.strip()
            if command == 'exit':
                print(
                    '\n\nPYSH : Thank you for using this PyCommander. Good Bye :)\n\n')
                break
            elif command == 'help':
                run_help()

            elif command.lower() == 'py on':
                isPy = True
            
            else:
                run_cmd(command)

        else:
            command = input('PYIN >>> ')
            if command.lower() != 'py off':
                try:
                    val = eval(command)
                    if val or val == 0:
                        print(f'PYOUT << {val}')
                        isPy = True
                except:
                    try:
                        exec(command)
                    except Exception as e:
                        print(f'PYOUT << ERROR: {e}')
            else:
                isPy = False


def run_cmd(command):

    if not runManual(command):
        try:
            subprocess.run(command.split(' '))

        except Exception:
            print(f"PYSH : Command '{command}' not found")


def runManual(command):
    curpath = os.getcwd()
    if command == 'pwd' or command == 'showpath':
        return show_path()

    elif command == 'ls' or command == 'list':
        return show_list()

    elif command[:3] == 'cd ':
        return change_dir(command[3:])

    elif command[:6] == 'mkdir ':
        return make_dir(os.path.join(curpath, command[6:]))

    elif command[:7] == 'create ':
        return make_file(os.path.join(curpath, command[7:]))

    elif command[:5] == 'edit ':
        return edit_file(os.path.join(curpath, command[5:]))

    elif command[:5] == 'read ':
        return read_file(os.path.join(curpath, command[5:]), command[5:])

    elif command[:3] == 'rm ':
        return delete_item(os.path.join(curpath, command[3:]), command[3:])

    elif command[:7] == 'rename ':
        cmd = command.split(' ')
        return rename_item(os.path.join(curpath, cmd[1]), cmd[1], os.path.join(curpath, cmd[2]))

    elif command[:3] == 'cp ':
        cmd = command.split(' ')
        return copy_item(os.path.join(curpath, cmd[1]), cmd[1], os.path.join(curpath, cmd[2]))
    
    elif command[:3] == 'mv ':
        cmd = command.split(' ')
        return move_item(os.path.join(curpath, cmd[1]), cmd[1], os.path.join(curpath, cmd[2]))

    elif command[:5] == 'link ':
        cmd = command[5:].split(' ')
        return make_Link(os.path.join(curpath, cmd[0]), os.path.join(curpath, cmd[1]))

    elif command[:6] == 'merge ':
        cmd = command[6:].split(' ')
        # Merge all directories
        if cmd[0] == '-a':
            # Merge and delete
            if cmd[-1] == '-d':
                return merge_AllDirs(os.path.join(curpath, cmd[1]), True)
            # Merge and keep original
            else:
                return merge_AllDirs(os.path.join(curpath, cmd[1]), False)
        # Merge specific directories
        else:
            if cmd[-1] == '-d':
                return merge_GivenDirs(cmd[:-1], curpath, os.path.join(curpath, cmd[-2]), True)
            else:
                return merge_GivenDirs(cmd, curpath, os.path.join(curpath, cmd[-1]), False)

    elif command[:6] == 'speed ':
        return speed_Command(command[6:])

    return False

# +---------------------------------------+
# | INDIVIDUAL FUNCTIONS FOR ALL COMMANDS |
# +---------------------------------------+

def speed_Command(choice):
    
    speedlist = {}
    listLocation = os.path.join(saveTo, 'speed.pkl')
    try:
        speedFile = open(listLocation, "rb")
        speedlist = pickle.load(speedFile)
        speedFile.close()

    except:
        speedFile = open(listLocation, "wb")
        pickle.dump(speedlist, speedFile)
        speedFile.close()

        try:
            speedFile = open(listLocation, "rb")
            speedlist = pickle.load(speedFile)
            speedFile.close()
        
        except:
            print('PYSH : Cannot run speed command feature.')
    
    if choice == 'show':
        print('\n\tAlias\t\tCommand\n')
        for alias in speedlist:
            print(f"\t{alias}\t\t'{speedlist[alias]}'")
        print('\n')

    elif choice == 'add':
        alias = input('\n\tEnter command alias: ')

        if alias == 'show' or alias == 'add' or alias == 'rm' or alias in speedlist.keys():
            print(f'\nPYSH : You cannot set {alias} as an alias as it is in use.')

        else:
            command = input('\n\tEnter command to perform: ')

            speedlist[alias] = command
            speedFile = open(listLocation, "wb")
            pickle.dump(speedlist, speedFile)
            speedFile.close()

    elif choice[:4] == 'edit':
        alias = input('\n\tEnter command alias: ')

        if alias in speedlist.keys():
            newcmd = input('\n\tEnter the new command to perform: ')
            speedlist[alias] = newcmd
            speedFile = open(listLocation, "wb")
            pickle.dump(speedlist, speedFile)
            speedFile.close()
        
        else:
            add = input('PYSH : Alias does not exist. Would you like to add one now (Y/N)?')
            if add.strip().lower() == 'y':
                speed_Command('add')

    elif choice[:2] == 'rm':
        alias = input('Enter command alias which you would like to remove: ')
        
        del speedlist[alias]
        
        speedFile = open(listLocation, "wb")
        pickle.dump(speedlist, speedFile)
        speedFile.close()

    else:
        try:
            run_cmd(speedlist[choice])

        except Exception as ex:
            print(ex)
    
    print('\n')
    return True


def merge_GivenDirs(lst, currentPath, targetPath, deleteOriginal=False):
    try:
        for i in lst[:-1]:
            currentfilePath = os.path.join(currentPath, i)
            shutil.copytree(currentfilePath, os.path.join(targetPath, i))
            if deleteOriginal:
                toDelete = currentfilePath
                if os.path.isfile(toDelete):
                    os.remove(toDelete)
                elif os.path.isdir(toDelete):
                    try:
                        os.rmdir(toDelete)
                    except:
                        shutil.rmtree(toDelete)
    except Exception as exc:
        print(f'PYSH : {exc}')
    return True


def merge_AllDirs(targetPath, deleteOriginal = False):
    try:
        lst = os.listdir()
        target = os.path.basename(os.path.normpath(targetPath))
        for i in lst:
            if i != target:
                currentfilePath = os.path.join(os.getcwd(), i)
                shutil.copytree(currentfilePath, os.path.join(targetPath, i))
                if deleteOriginal:
                    toDelete = currentfilePath
                    if os.path.isfile(toDelete):
                        os.remove(toDelete)
                    elif os.path.isdir(toDelete):
                        try:
                            os.rmdir(toDelete)
                        except:
                            shutil.rmtree(toDelete)
    except Exception as exc:
        print(f'PYSH : {exc}')
    return True


def make_Link(srcfilePath, destfilePath):
    try:
        os.symlink(srcfilePath, destfilePath)
    except Exception as exc:
        print(f'PYSH : {exc}')
    return True


def move_item(currentfilePath, newfilePath):
    try:
        shutil.move(currentfilePath, newfilePath)
    except Exception as exc:
        print(f'PYSH : {exc}')
    return True


def copy_item(currentfilePath, currentfilename, newfilePath):
    try:
        shutil.copy(currentfilePath, newfilePath)
    except:
        try:
            shutil.copytree(currentfilePath, os.path.join(newfilePath, currentfilename))
        except Exception as exc:
            print(f'PYSH : {exc}')
    return True


def rename_item(oldfilePath, oldfilename, newfilePath):
    try:
        os.rename(oldfilePath, newfilePath)
    except:
        print(f"PYSH : File '{oldfilename}' not found")
    return True


def delete_item(filepath, filename):
    try:
        if os.path.isfile(filepath):
            os.remove(filepath)

        elif os.path.isdir(filepath):
            try:
                os.rmdir(filepath)
            except:
                yousure = input(
                    f"PYSH : {filename} is a non-empty directory. Do you want to remove it anyway? (Y/N):").lower().strip()
                if yousure == 'y':
                    try:
                        shutil.rmtree(filepath)
                    except Exception as exc:
                        print(f'PYSH : {exc}')

    except Exception as exc:
        print(f'PYSH : {exc}')

    return True


def edit_file(filename):
    print('\n')
    try:
        reader = open(filename, "r+")
        old = reader.read()
        print(old, end='')
        reader.close()

    except:
        reader = open(filename, "a+")
        old = reader.read()
        print(old, end='')
        reader.close()

    thisfile = open(filename, 'a+')
    thisline = ''

    while thisline[-4:] != '/**/':

        thisline = input('')

        if thisline == '/**/':
            thisfile.write('')

        elif thisline[-4:] == '/**/':
            thisfile.write(thisline[:-4]+'\n')

        else:
            thisfile.write(thisline + '\n')

    thisfile.close()
    print('\n\n')
    return True


def read_file(filepath, filename):

    try:
        reader = open(filepath, "r+")
        old = reader.read()
        broken = old.split('\n')
        maxl, dash = 0, 0
        for i in broken:
            if len(i) > maxl:
                maxl = len(i)

        print()
        while dash in range(maxl+2):
            print('-', end='')
            dash += 1
        print()
        print(old, end='')
        print()
        dash = 0
        while dash in range(maxl+2):
            print('-', end='')
            dash += 1
        print()

        reader.close()

    except:
        print(f"PYSH : File '{filename}' not found")

    return True


def make_file(filename):
    open(filename, 'a').close()
    return True


def make_dir(dirName):
    dirName = dirName.split(' ')
    mode = dirName[-1]
    os.mkdir(dirName[0])
    if mode == '-cd':
        change_dir(dirName[0])
    return True


def show_path():
    print(f'PYSH : {os.getcwd()}')
    return True


def show_list():
    print(f'PYSH : ')
    lst = os.listdir()
    for i in lst:
        print(f'\t> {i}')
    print()
    return True


def change_dir(path):
    path = path.strip()
    mode = path[-3:]
    try:
        if mode == '-ls':
            os.chdir(os.path.abspath(path[:-3]))
            show_list()

        else:
            os.chdir(os.path.abspath(path))

    except:
        print(f'PYSH | {curpath} | cd: No such file or directory: {path[0]}')
    return True


def run_help():

    manual = {
        'exit':
        '''
        Usage: $ exit
        Function: Exits (quits) pycommander.
        ''',

        'pwd':
        '''
        Usage: $ pwd OR $ showpath
        Function: Prints the current working directory (path to current directory).
        ''',

        'showpath':
        '''
        Usage: $ pwd OR $ showpath
        Function: Prints the current working directory (path to current directory).
        ''',

        'ls':
        '''
        Usage: $ ls OR $ list
        Function: Prints the contents of the current working directory.
        ''',

        'list':
        '''
        Usage: $ ls OR $ list
        Function: Prints the contents of the current working directory.
        ''',

        'cd':
        '''
        Usage: $ cd {name/path of directory}
        Function: Navigate to target directory from current directory.
        
        Mode: -ls
        Mode Usage: $ cd {name/path of directory} -ls
        Mode Function: Print contents of new directory after navigating.
        ''',

        'mkdir':
        '''
        Usage: $ mkdir {name/path of new directory}
        Function: Create a new directory with the required name, having the required path.

        Mode: -cd
        Mode Usage: $ mkdir {name/path of new directory} -cd
        Mode Function: Move to new directory after creating it.
        ''',

        'create':
        '''
        Usage: $ create {file name}.{file extension}
        Function: Used to create a blank file.
        ''',

        'edit':
        '''
        Usage: $ edit {file name}.{file extension} OR $ edit {file location}
        Function: Used to edit an existing file. Creates a blank file for editing if one doesn't exist.
        ''',

        'read':
        '''
        Usage: $ read {file name}.{file extension} OR $ read {file location}
        Function: Used to merely read an existing file. Does not work if the file doesn't exist.
        ''',

        'rename':
        '''
        Usage: $ rename {old file name} {new file name}
        Function: Changes the name of a file from the old one to the new one.
        ''',

        'cp':
        '''
        Usage: cp {file name} {location of target directory}
        Function: Simply copies the file or directory from the current location to the new location. Target location must be a directory.
        ''',

        'link':
        '''
        Usage: $ link {source location} {new location}
        Function: Creates a hard link of the given source in the new link location.
        ''',

        'rm':
        '''
        Usage: $ rm {name of file/directory to remove} OR $ rm {location of file/directory to remove}
        Function: Deletes a file or directory permanently. Asks confirmation for non-empty directories. Does not work if the file doesn't exist.
        ''',

        'mv':
        '''
        Usage: $ mv {old location} {new location}
        Function: Moves files and directories from the old location to the new location.
        ''',

        'merge':
        '''
        Usage: $ merge {dir location 1} {dir location 2} ... {dir location n} {target directory}
        Function: Merges all listed directories into the target directory.

        Mode: -a
        Mode Usage: $ merge -a {target directory}
        Mode Function: Merges all directories in the current location into the target directory.

        Mode: -d
        Mode Usage: $ merge {dir location 1} {dir location 2} ... {dir location n} {target directory} -d
        Mode Function: Delete the original directories upon merging.

        Mode: -a -d
        Mode Usage: $ merge -a {target directory} -d
        Mode Function: Merges all directories in the current location into the target directory and delete the original directories upon merging.
        ''',

        'speed':
        '''
        Usage: $ speed {alias}
        Function: Allows users to set their own aliases for any command.

        In-Built Aliases:
        
        Alias: show
        Alias Usage: $ speed show
        Alias Function: Prints all the user-defined aliases.

        Alias: add
        Alias Usage: $ speed add
        Alias Function: Adds a new user-defined alias and its corresponding function.

        Alias: edit
        Alias Usage: $ speed edit
        Alias Function: Changes the command given to the specified user-defined alias.

        Alias: rm
        Alias Usage: $ speed rm
        Alias Function: Removes the specified user-defined alias.
        ''',
    }

    command_list = list(manual.keys())

    cmd = 'print'
    while cmd != 'quit':
        if cmd == 'print':
            print('\n')
            for i in range(len(command_list)):
                print(f'\t- {command_list[i]}')
            cmd = ''

        print(
            "\n\nPYHE : Enter 'quit' to exit help page and 'print' to see the list of commands again")
        cmd = input('Enter the command of your choice: ')

        if cmd != 'quit' and cmd != 'print':
            try:
                print('PYHE :')
                print(manual[cmd])
            except:
                print('PYHE: Command not found. Please check and try again.')

    return True


main()
