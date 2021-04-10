import os
import shutil
import subprocess

curpath = os.getcwd()

def main():
    isPy = False
    while 1:
        if not isPy:
            curpath = os.getcwd()
            command = input(f'PYSH | {curpath} | $ ')
            command = command.strip()
            if command == 'exit':
                print('\n\nPYSH : Thank you for using this Python Shell. Good Bye :)\n\n')
                break
            elif command == 'help':
                print('\nPYSH : This is a simple Python-based Shell.\n')
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

            if '|' in command:
                # save for restoring later on
                s_in, s_out = (0, 0)
                s_in = os.dup(0)
                s_out = os.dup(1)

                # first command takes commandut from stdin
                fdin = os.dup(s_in)

                # iterate over all the commands that are piped
                for cmd in command.split('|'):
                    # fdin will be stdin if it's the first iteration
                    # and the readable end of the pipe if not.
                    os.dup2(fdin, 0)
                    os.close(fdin)

                    # restore stdout if this is the last command
                    if cmd == command.split('|')[-1]:
                        fdout = os.dup(s_out)
                    else:
                        fdin, fdout = os.pipe()

                    # redirect stdout to pipe
                    os.dup2(fdout, 1)
                    os.close(fdout)

                    try:
                        subprocess.run(cmd.strip().split())
                    except Exception:
                        print(f"PYSH : Command '{cmd.strip()}' not found")

                # restore stdout and stdin
                os.dup2(s_in, 0)
                os.dup2(s_out, 1)
                os.close(s_in)
                os.close(s_out)
            
            else:
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

    return False

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
    os.mkdir(dirName)
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
    try:
        os.chdir(os.path.abspath(path))
    except:
        print(f'PYSH | {curpath} | cd: No such file or directory: {path}')
    return True


main()
