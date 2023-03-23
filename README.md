# Note

**Note impotante :** débloquer la limitation de taille de chemin de fichier sur Windows 

https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell

https://docs.python.org/3/using/windows.html#removing-the-max-path-limitation

# PowerShell Windows

`.\cherche.ps1 C:\Users\$env:username .*mus.*` donne 2,9217598 sec

`.\cherche_SLOW.ps1 "C:\Users\$env:username" "*mus*"` donne 18,7601879 sec

# Python 

La version `cherche.py` est une version avec les path et montre aussi les dossiers de jointures dont on n'a pas accès et on a la possibilité d'inclure une liste de répertoire qu'on ne veut pas explorer.

La version `cherche_scandir_iterateur.py` n'affichera pas, dans ses résultats finaux, les répertoires dont on n'a pas accès. C'est une façon originale de le faire de cette manière. Le temps est pareil que `cherche_scandir_path.py`.

`python .\cherche_scandir_path.py C:\Users\$env:username .*mus.` donne 2.259 sec

**Le script python, transformé en exécutable, et mis dans C:\bin par exemple, peut être appelé même depuis une console WSL (Sous-système Linux Windows).**

On pourrait faire : **cherche.exe d: github**

### Créer un exécutable Python sur Windows :

    Installer pyinstaller ?
    pip install pyinstaller
    
    Ajouter au Path $HOME\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts

    # faire le rép C:\bin\
    # tout copier dedans si on refait une installation de Windows
    # ajouter au Path C:\bin\dist


***

Voir aussi https://regex101.com/ pour les tests regex

Voir aussi https://github.com/luong-komorebi/Markdown-Tutorial/blob/master/README_fr.md pour écrire un readme