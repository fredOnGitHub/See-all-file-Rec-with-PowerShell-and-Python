
# https://pypi.org/project/scandir/ il inclut stat du fichier (is_dir...)
# https://stackoverflow.com/questions/2212643/python-recursive-folder-read
# https://stackoverflow.com/a/70398926/7058377
import pprint
import os
import re
import time
import sys
from pathlib import Path
import locale
import re


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


def regex_trouvé(regex, s):
    # print("regex", dirname)
    r = re.search(regex, s, re.IGNORECASE)  # https://regex101.com/
    if r:
        # print("ok", s)
        return True
    return False


def nettoyer_patht(path):
    # print('path', path)
    path = re.sub(r'\\+', '/', path)  # tous les slash Windows en /
    path = re.sub(r'/+', '/', path)  # toutes les rép de / en 1 fois
    # vider les caractères espace ex : pour '/a/d/    ' deviendra '/a/d/'
    path = re.sub(r'\s+$', '', path)
    # enlever le dernier / (pour afficher un os.path.basename(path))
    path = re.sub(r'/$', '', path)
    # print('path', path)
    return path


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
    path = sys.argv[1]
    regex = sys.argv[2]
    # print("path=<%s>" % (path))
    path = nettoyer_patht(path)
    # print("path=<%s>" % (path))
    if not os.path.exists(path):
        print("does not exist", path)
        exit(0)
    # print('basename', os.path.basename(path))
    # print('dirname', os.path.dirname(path))
    dir_exclus = ["AppData"]
    # dir_exclus = ["AppData", 'documents_']
    dirs = []
    stack = []
    files = []
    it = None

    if os.path.isdir(path):
        nom = os.path.basename(path)
        if not est_inclus_dans(dir_exclus, nom):
            try:
                it = os.scandir(path)
                stack.append(it)
                if regex_trouvé(regex, nom):
                    dirs.append(path)
            except:
                print("except", it)
                print("An error undefined has occurred")
    elif os.path.isfile(path):
        nom = os.path.basename(path)
        if regex_trouvé(regex, nom):
            files.append(path)

    others = []
    n = 0
    while stack:
        it = stack.pop()
        for e in it:
            n += 1
            if e.is_dir():
                # print("e.name=<%s>" % (e.name))
                # print("e.path=<%s>" % (e.path))
                if not est_inclus_dans(dir_exclus, e.name):
                    try:
                        it_ = os.scandir(e.path)
                        stack.append(it_)
                        if regex_trouvé(regex, e.name):
                            dirs.append(e.path)
                    except FileNotFoundError:
                        # print("FileNotFoundError", e.path)
                        print(bcolors.FAIL + "FileNotFoundError" +
                              e.path + bcolors.ENDC)
                        print(bcolors.FAIL + "FileNotFoundError" +
                              path + bcolors.ENDC)
                        print(bcolors.WARNING +
                              "taille du chemin trop long >= 260" + bcolors.ENDC)
                        print(bcolors.WARNING + 'Administrator mode and see https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell' + bcolors.ENDC)
                        # exit(0)
                        pass
                    except PermissionError:
                        print(bcolors.WARNING + "PermissionError" +
                              "  " + e.path + bcolors.ENDC)
                        pass
                    except NotADirectoryError:
                        print("NotADirectoryError", e.path)
                        pass
                    except:
                        print("except", e.path)
                        print("An error undefined has occurred")
                else:
                    print(bcolors.OKCYAN + "Not added" +
                          "  " + e.path + bcolors.ENDC)
            elif e.is_file():
                if regex_trouvé(regex, e.name):
                    files.append(e.path)
            else:
                others.append(e.path)

    # print("stack", *stack, sep="\n")
    # print("files", *files, sep="\n")
    # print("dirs", *dirs, sep="\n")
    # print("others", *others, sep="\n")

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
