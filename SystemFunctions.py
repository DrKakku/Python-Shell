import os
import shutil

from PyShell import saveTo , curpath

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



