from pathlib import Path
import os
import re
import sys
import locale


def Clean():
    os.system('cls' if os.name == 'nt' else 'clear')
    # if os.name == 'nt':
    #     print("nt")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def erreur():
    print(bcolors.FAIL + "usage : trouve.py  <repIn>  <regex comme \"^\..*\" (les .DS_Store par exemple)>" + bcolors.ENDC)
    print(bcolors.FAIL +
          "usage : trouve.py  <repIn>  <regex comme \".*\" (tout)>" + bcolors.ENDC)
    print(bcolors.FAIL + "usage : trouve.py  <repIn>  <regex comme \".*\.ps1$\" (fichiers se terminant par .ps1)>" + bcolors.ENDC)
    print(bcolors.FAIL + "usage : trouve.py  <repIn>  <regex comme \".*\.py$\" (fichiers se terminant par .py)>" + bcolors.ENDC)
    print(bcolors.FAIL +
          "usage : trouve.py  <repIn>  <regex comme \"applica.*Data\">" + bcolors.ENDC)
    print(bcolors.FAIL + """
        ^ start
        $ end
        \. le point
        .* n'importe quel caractère
    """ + bcolors.ENDC)
    sys.exit(1)


def lireListe(s, l):
    if l != []:
        a = 10
        if len(l) > a:
            print(s, *l[0:a], sep="\n")
        else:
            print(s, *l, sep="\n")


def regex_trouvé(regex, s):
    # print("regex", dirname)
    r = re.search(regex, s, re.IGNORECASE)  # https://regex101.com/
    if r:
        # print("ok", s)
        return True
    return False


print('version', sys.version)
print('USERPROFILE', os.environ['USERPROFILE'])  # sur windows
print('getfilesystemencoding', sys.getfilesystemencoding())
print('locale.getpreferredencoding', locale.getpreferredencoding())
print('écrire chinois traditionel : 漢字')

if len(sys.argv) != 3:
    erreur()
else:
    nmPgm = sys.argv[0]
    dir = sys.argv[1]
    regex = sys.argv[2]

    print(bcolors.HEADER + "wait..." + bcolors.ENDC)

    # TEST
    # user = os.environ['USERPROFILE']  # on  windows
    # p = Path(user + "/Documents/")
    # p = Path(user + "/Documents/Mes vidéos")
    # p = Path(user + "/Documents/é é")
    # regex = ".*musi.*"
    dir_exclus = ["AppData"]
    p = Path(dir)
    stack = [p]
    execp = []
    dirs = []
    files = []
    others = []
    liens = []
    while stack:
        path = stack.pop()
        # isDir = path.is_dir()
        # if regex_trouvé(regex, path.name):
        # print("path", path)
        if path.is_dir():
            if path.name not in dir_exclus:
                try:
                    for e in path.iterdir():
                        stack.append(e)
                    if regex_trouvé(regex, path.name):
                        # print("dir", path)
                        # print("path.name", path.name)
                        # dir accessible (pas de PermissionError) + regex trouvé
                        dirs.append(path)
                except PermissionError:
                    execp.append(path)
                    # print("PermissionError", path)
                except NotADirectoryError:
                    ...
                    # print("NotADirectoryError", path)
            else:
                print("non", path)
        elif path.is_file():
            if regex_trouvé(regex, path.name):
                # print("file", path.name)
                files.append(path)
        elif path.is_symlink():
            liens.append(path)
        else:
            others.append(path)
    # print("execp", *execp, sep="\n")
    # print("dirs", *dirs, sep="\n")
    # print("files", *files, sep="\n")
    # print("liens", *liens, sep="\n")
    # print("others", *others, sep="\n")
    # print("end")
    i = 1
    for s in files:
        # s = s[ : 2]+"/"+s[2 : ]
        print(bcolors.OKGREEN + str(i) + "  " + str(s) + bcolors.ENDC)
        i += 1

    i = 1
    for s in dirs:
        print(bcolors.OKBLUE + str(i) + "  " + str(s) + bcolors.ENDC)
        i += 1

# In Windows 11, in `C:\Users\$env:username\Documents` there are special directories that you haven't access.
# You can list them with PowerShell command line:

#     Get-ChildItem -Path  C:\Users\$env:username\Documents -force
# Get-ChildItem -Path  C:\Users\$env:username\Documents -force
# ...
# l--hs          29/01/2023    15:32          My music -> C:\Users\****\Music
# l--hs          29/01/2023    15:32          My pictures -> C:\Users\****\Pictures
# l--hs          29/01/2023    15:32          My videos -> C:\Users\****\Videos


# pathlib  new in 3.4
# ... "pathlib" module providing object-oriented filesystem paths
# https://www.python.org/downloads/release/python-340

# intéressant : demander pardon avec try que de faire pleins de tests et qu'un autre thread (par ex) supprime la ressource testée
# https://stackoverflow.com/a/28015065
# https://stackoverflow.com/questions/58306849/python-having-trouble-opening-a-file-with-spaces
# https://docs.python.org/2/glossary.html#term-lbyl

# exemple
# cls;cls; python .\cherche_path.py.py C:\Users\***\ .*musi.*
# cls; cls; measure-Command { python .\cherche_path.py C:\Users\detro\ .*musi.* }
