Clear-Host
$message = "Date: $(Get-Date)"

# if ('big' -match 'b[iou]g'){
# 	Write-Host "oui"
# }
# if ('_Cher_' -match ".*cher.*") {
# 	Write-Host "oui"
# }
# if ('_Cher_' -eq '_cher_') {
# 	Write-Host "oui"
# }
# $array = "Hello", 'Bonjour'
# $array -contains ("HELLO")# ! -contains est case insensitive mais pas $array.Contains("HELLO")
# exit

Write-Host $message
Write-Host "Hello"
if (-not($args.Length -eq 2)) {
	Write-Host "usage : <nom_pgm>  <répertoire>  <regex  *.txt>  (tout ce qui se termine par .txt)" -ForegroundColor Red
	Write-Host "exemple : ./cherche.ps1   $env:username/Music   *doors*" -ForegroundColor Blue
}
else {
	# powershell Get-ChildItem is slow vs python scandir
	# https://stackoverflow.com/questions/72193074/powershell-slowness-in-get-childitem-directory-recurse-when-there-are-lots
	# https://learn.microsoft.com/fr-fr/dotnet/api/system.collections.queue.dequeue?view=net-7.0
	
	$path = $args[0]
	$regex = $args[1]
	Write-Host "rep = $($path)"
	Write-Host "regex = $($regex)"
	# Set-Location $path
	$CurrentDirectory = Get-Location
	Write-Host "CurrentDirectory : $CurrentDirectory"#le mettre dans une var sinon affiche en bas
	$t = Measure-Command -Expression {
		if (Test-Path -Path $path -PathType Container) {
			$queue = [Collections.Generic.Queue[IO.DirectoryInfo]]::new()
			$queue.Enqueue("$path")
			$tFich = [System.Collections.ArrayList]@()
			$tRep = [System.Collections.ArrayList]@()
			$nbexception = 1
			$dir_exclus = "AppData_"
			if ($dir_exclus -contains ($dir.name)){
				exit
			}
			while ($queue.Count) {
				# Write-Host "count : $($queue.Count)"
				$dir = $queue.Dequeue()
				# https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-string-substitutions?view=powershell-7.3
				# Write-Host ('--> {0} ' -f $dir.name)
				# Write-Host "-->" $dir.name
				try {
					if ($dir.name -match $regex) {
						# Write-Host "oui  $dir.name"
						$tRep += $dir
					}
					# Test-Path -Path $fi -PathType Leaf  ou Container
					foreach ($fi in $dir.GetFiles()) {
						# Write-Host "file " $fi.name
						if ($fi.name -match $regex) {
							# Write-Host "oui  $fi.name"
							$tFich += $fi
						}
					}
					foreach ($fi in $dir.GetDirectories()) {
						if ($dir_exclus -contains ($fi.name)){
							Write-Host "Ne pas ajouter" $fi.FullName -ForegroundColor Blue
						}else{
							$queue.Enqueue("$fi")
						}
						# Write-Host "dir  " $fi.name
					}
					# Read-Host "continue"
				}
				catch [UnauthorizedAccessException] {
					Write-Warning "$nbexception $dir"
					$nbexception++
				}
				catch {
					# https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-exceptions?view=powershell-7.3
					Write-Error $_

					# https://stackoverflow.com/questions/54193643/powershell-catching-exception-type
					$exception = $_.Exception
					do {
						# Write-Host $exception.GetType().FullName  -ForegroundColor Yellow
						Write-Host $exception.GetType().Name -ForegroundColor Yellow
						$exception = $exception.InnerException
						# Write-Host $exception -ForegroundColor Yellow
					} while ($exception)
					Write-Host '---------------------' -ForegroundColor Yellow
					exit
				}
			}
			$i = 1
			foreach ( $a in $tFich ) {
				Write-Host $i $a -ForegroundColor Green
				$i++
			}$i = 1
			foreach ( $a in $tRep ) {
				Write-Host $i $a -ForegroundColor Blue
				$i++
			}
		} 
	}
	# Write-Host("", $t)
	Write-Host $t.TotalSeconds "sec"
}


#ForEach vs ForEach-Object
# PowerShell - Les boucles ForEach
# https://youtu.be/h4z610jQANM?t=495
# https://stackoverflow.com/questions/65281667/get-childitem-foreach-object-vs-foreach-issue

#-LiteralPath
# https://www.reddit.com/r/PowerShell/comments/f6zlbp/path_vs_literalpath/
# https://stackoverflow.com/questions/28611307/literalpath-option-for-cmdlet

# get-item  powershell  https://learn.microsoft.com/fr-fr/powershell/module/microsoft.powershell.management/get-item?view=powershell-7.3
# get-item  https://devblogs.microsoft.com/scripting/powertip-using-powershell-to-determine-if-path-is-to-file-or-folder/

# getfiles  dotnet  https://learn.microsoft.com/fr-fr/dotnet/api/system.io.directory.getfiles?view=net-7.0
# IO.DirectoryInfo  dotnet  https://learn.microsoft.com/fr-fr/dotnet/api/system.io.directoryinfo?view=net-7.0
# dequeue   dotnet   https://learn.microsoft.com/fr-fr/dotnet/api/system.collections.queue.dequeue?view=net-7.0

# regex exp régulière https://learn.microsoft.com/fr-fr/powershell/module/microsoft.powershell.core/about/about_regular_expressions?view=powershell-7.3
# powershell tell if is directory