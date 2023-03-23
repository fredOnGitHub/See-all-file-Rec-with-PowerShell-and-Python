from pathlib import Path
import os
import re
import sys
import locale
import time


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


def est_inclus_dans(dir_exclus, nom):
    for i in dir_exclus:
        # print("i", i, nom)
        if regex_trouvé(i, nom):
            return True
    return False


Clean()
# Get the list of user's
# environment variables
env_var = os.environ
import pprint
# Print the list of user's
# environment variables
# print("User's Environment variable:")
# pprint.pprint(dict(env_var), width = 1)#https://www.geeksforgeeks.org/python-os-environ-object/

print('version', sys.version)
if "HOME" in os.environ:
    print('user', os.environ['HOME'])  # sur Unix
elif "USERPROFILE" in os.environ:
    print('USERPROFILE', os.environ['USERPROFILE'])  # sur windows
print('getfilesystemencoding', sys.getfilesystemencoding())
print('locale.getpreferredencoding', locale.getpreferredencoding())
print('écrire chinois traditionel : 漢字')


if len(sys.argv) != 3:
    erreur()
else:
    start = time.perf_counter()
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
    dir_exclus = ["AppData", "documents_"]
    # dir_exclus = []
    p = Path(dir)
    stack = []
    execp = []
    dirs = []
    files = []
    others = []
    liens = []
    n = 0
    if p.is_dir():
        # print("1")
        if not est_inclus_dans(dir_exclus, p.name):
            # print('NON dedans')
            stack = [p]
            if regex_trouvé(regex, p.name):
                dirs.append(p)
                # print("ok")
        # else:
        #     print('dedans')
    elif p.is_file():
        if regex_trouvé(regex, p.name):
            files.append(p)
    print('stack', stack)
    print('files', files)
    print('dirs', dirs)
    # exit(0)
    while stack:
        path = stack.pop()
        # print('path', path)
        # exit(0)
        n += 1
        try:
            for e in path.iterdir():
                if e.is_dir():
                    nom = e.name
                    if not est_inclus_dans(dir_exclus, nom):
                        stack.append(e)
                        if regex_trouvé(regex, nom):
                            dirs.append(e)
                elif e.is_file():
                    nom = e.name
                    if regex_trouvé(regex, nom):
                        files.append(e)
                elif e.is_symlink():
                    liens.append(e)
                else:
                    others.append(e)
        except PermissionError:
            print(bcolors.FAIL + "PermissionError" + "  " + str(path) + bcolors.ENDC)
        except NotADirectoryError:
            print(bcolors.FAIL + "NotADirectoryError" + "  " + str(path) + bcolors.ENDC)
            # ...
        except:
            print(bcolors.FAIL + "except" + "  " + str(path) + bcolors.ENDC)

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
    end = time.perf_counter()
    ms = (end-start)  # * 10**6
    print(f"Elapsed {ms:.03f} secs.")

    print(n, "élément scannés")
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
