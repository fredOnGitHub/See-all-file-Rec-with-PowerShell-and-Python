# Créer l'exécutable

# Installer pyinstaller ?
# pip install pyinstaller
# Ajouter au Path C:\Users\*******\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts

# faire le rép \usr\bin\
# tout copier dedans si on refait une installation de Windows
# ajouter au Path C:\usr\bin\dist

# Aller dans \usr\bin\
# pyinstaller.exe --onefile .\cherche.py

# clear; cherche.exe d: .*txt.*

# https://www.youtube.com/watch?v=IvMajUjCpao #Créer un exécutable Windows à partir d'un script Python
# https://www.youtube.com/watch?v=Qb0fkeye-y0 #Comment convertir une application python (.py) en un exécutable (.exe)

# https://stackoverflow.com/questions/45951964/pyinstaller-is-not-recognized-as-internal-or-external-command

# https://stackoverflow.com/questions/53629115/colored-text-output-on-powershell
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

# Gestion des paths
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

# VERSION DE POWERSHELL : $PsVersionTable

import sys
import os
import re
import time
import locale
from pathlib import Path


def Clean():
    os.system('cls' if os.name == 'nt' else 'clear')


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


REP = []
FICH = []


def go(src, regex):
    m = 0
    nf = 0
    nd = 0
    n = 0
    # src = Path(src+"/")
    for root, dirs, files in os.walk(src):
        if len(dirs):
            n += len(dirs)
            nf += 1
            for i in dirs:
                r = re.search(regex, i, re.IGNORECASE)  # https://regex101.com/
                if r:
                    l = len(root)+len(i)
                    m = max(m, l)
                    nd += 1
                    # s = os.path.join(root, i)#belle jonction de path Unix ou Windows
                    s = "[D] %i  %s   ::   %s" % (nd, i, root)
                    REP.append(s)
        if len(files):
            n += len(files)
            for i in files:
                r = re.search(regex, i, re.IGNORECASE)  # https://regex101.com/
                if r:
                    l = len(root)+len(i)
                    m = max(m, l)
                    nf += 1
                    s = "[F] %i  %s   ::   %s" % (nf, i, root)
                    FICH.append(s)
    print(n, "éléments scannés")


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


Clean()

if len(sys.argv) != 3:
    erreur()
else:
    nmPgm = sys.argv[0]
    rin = sys.argv[1]
    regex = sys.argv[2]

    print('version', sys.version)
    if "HOME" in os.environ:
        print('user', os.environ['HOME'])  # sur Unix
    elif "USERPROFILE" in os.environ:
        print('USERPROFILE', os.environ['USERPROFILE'])  # sur windows
    print('getfilesystemencoding', sys.getfilesystemencoding())
    print('locale.getpreferredencoding', locale.getpreferredencoding())
    print('écrire chinois traditionel : 漢字')

    print(bcolors.HEADER + "wait..." + bcolors.ENDC)

    start = time.perf_counter()
    go(rin, regex)

    for s in FICH:
        # s = s[ : 2]+"/"+s[2 : ]
        print(bcolors.OKGREEN + s + bcolors.ENDC)

    for s in REP:
        print(bcolors.OKBLUE + s + bcolors.ENDC)

    end = time.perf_counter()
    ms = (end-start)  # * 10**6
    print(f"Elapsed {ms:.03f} secs.")
# Des rép bizarres :
# python ./cherche.py C:\Users\***\ .*musi.*
# voir les (jointure)


#  measure-Command { python ./cherche.py C:\Users\***\ .*musi.* }

# os.scandir new in 3.5
# The new os.scandir() function provides a better and significantly faster way of directory traversal.
# https://docs.python.org/3/whatsnew/3.5.html?highlight=scandir
# https://docs.python.org/3/whatsnew/3.5.html?highlight=scandir#whatsnew-pep-471

# https://docs.python.org/3/library/os.html#os.scandir
# Using scandir() instead of listdir() can significantly increase the performance of code that also needs
# file type or file attribute information, because os.DirEntry objects expose this information if the
#  operating system provides it when scanning a directory. All os.DirEntry methods may perform a system call,
# but is_dir() and is_file() usually only require a system call for symbolic links; os.DirEntry.stat()
# always requires a system call on Unix but only requires one for symbolic links on Windows.


# comparer les dossiers
# https://stackoverflow.com/questions/6776554/get-file-size-during-os-walk

# intéressant : demander pardon avec try que de faire pleins fde tests et qu'un autre thread (par ex) supprime la ressource testé
# https://stackoverflow.com/a/28015065
# https://stackoverflow.com/questions/58306849/python-having-trouble-opening-a-file-with-spaces
# https://docs.python.org/2/glossary.html#term-lbyl
