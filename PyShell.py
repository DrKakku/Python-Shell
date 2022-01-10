import os
from Functions import *
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


if __name__ == '__main__':
    main()
