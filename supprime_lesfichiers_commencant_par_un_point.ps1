$path = ""

Function Format-FileSize() {
	Param ([int]$size)
	If ($size -gt 1TB) { [string]::Format("{0:0.00} TB", $size / 1TB) }
	ElseIf ($size -gt 1GB) { [string]::Format("{0:0.00} GB", $size / 1GB) }
	ElseIf ($size -gt 1MB) { [string]::Format("{0:0.00} MB", $size / 1MB) }
	ElseIf ($size -gt 1KB) { [string]::Format("{0:0.00} kB", $size / 1KB) }
	ElseIf ($size -gt 0) { [string]::Format("{0:0.00} B", $size) }
	Else { "" }
}

$varCheminRepertoireScript = [System.IO.Path]::GetDirectoryName($MyInvocation.MyCommand.Definition)
$currentScriptName = $MyInvocation.MyCommand.Name #Récupération du nom du script en cours

#On ne prend que le nom du script sans l'extention. Pour cela on chercher la position d'un point en partant de la droite et on prend tout ce qui est à sa gauche
$currentScriptName = $currentScriptName.substring(0, $($currentScriptName.lastindexofany(".")))

#Création du fichier vierge
$EmplacementFichier = "$varCheminRepertoireScript\$($currentScriptName)_Log.txt"


Function Write_File_to_delete() {
	Param ([string]$path)

	$MonFichier = New-Item -type file $EmplacementFichier -Force

	$m = 0#longueur max de path
	$i = 0#num de fichier
	$t = 0#somme taille des fichiers
	Get-ChildItem -Path $path -Recurse -Force -include ".*" | ForEach-Object {
		$l = $_.DirectoryName.Length + $_.name.Length
		if ($m -lt $l ) { $m = $l }
		$taille_tot = Format-FileSize($t)
		if ($i % 20 -eq 0) {
			$MyLine = "========================================================================================================================="
			Write-Host $MyLine
			add-content $MonFichier $MyLine
			$MyLine = "num`tlong max de nom de fichier`ttaille totale`tlong nom de fichier`tTaille du fichier`tnom du fichier"
			Write-Host $MyLine
			add-content $MonFichier $MyLine
		}
		$MyLine = "$($i)`t$($m)`t`t`t`t$($taille_tot)`t$($l)`t`t`t$($_.Length)`t`t`t$($_.name)"
		Write-Host $MyLine
		# Write-Host "$($i)`t$($m)`t$($size)`t$($l)`t$($_.name)`t$($_.Length)"
		$i++
		$t += $_.Length
		add-content $MonFichier $MyLine
	} 
}

Function Delete_Files() {
	Param ([string]$path)
	Get-ChildItem -Path $path -Recurse -Force -include ".*" -exclude ".git*" | ForEach-Object {
		Write-host $_.Name
		# Remove-Item -Confirm -LiteralPath $_ -Force -Recurse
		Remove-Item -LiteralPath $_ -Force -Recurse 
		# -Force, sinon même avec bypass (exécute tout) on peut avoir des échecs, 
		# -Recurse pour les dossier et ss dossiers d'un coup avec option T pour tous .*
		Write-host
	}
}

# Write_File_to_delete($path)
# Delete_Files($path)


"Hello" > "log.txt"
Get-ChildItem -Path "Y:\" -Recurse -Force  -include ".*"  | 
Where-Object { $_ -notlike "*.git*" -and $_ -notlike "*.imovielibrary*" -and $_ -notlike "*.skt*" } | 
ForEach-Object {
	$l = "$($_.DirectoryName)\$($_.name)"
	$l >> "log.txt"
	Write-host $l
	# Remove-Item -Confirm -LiteralPath $_ -Force -Recurse
	# Remove-Item -LiteralPath $_ -Force -Recurse
}


# Get-ChildItem -Path "C:\Users\detro\*DELETE FICHIERS*"  -Recurse  | ForEach-Object {
# 	$l = "$($_.DirectoryName)\$($_.name)"
# 	Write-host $l
# }


# Start-Sleep -Seconds 5

# encodage de ce fichier en utf16le!!
# https://docs.microsoft.com/fr-fr/powershell/scripting/dev-cross-plat/vscode/understanding-file-encoding?view=powershell-7.1
# https://blog.netwrix.fr/2018/12/05/gestion-des-fichiers-avec-powershell/
# https://www.tutos.eu/5453
# https://stackoverflow.com/questions/55665530/why-cant-i-use-in-write-host
# https://www.tutorialspoint.com/powershell/powershell_files_delete_folders.htm
# https://www.it-connect.fr/autoriser-lexecution-de-scripts-powershell/
# https://www.spguides.com/check-file-size-using-powershell/
# https://community.idera.com/database-tools/powershell/ask_the_experts/f/powershell_for_windows-12/5120/how-to-deal-with-special-characters-in-filenames
# https://stackoverflow.com/questions/19207991/how-to-exclude-list-of-items-from-get-childitem-result-in-powershell
# https://docs.microsoft.com/fr-fr/powershell/scripting/samples/removing-objects-from-the-pipeline--where-object-?view=powershell-7.1
# https://docs.microsoft.com/fr-fr/powershell/module/microsoft.powershell.core/about/about_comparison_operators?view=powershell-7.1
