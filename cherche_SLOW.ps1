Clear-Host

Write-Host "Hello"

if (-not($args.Length -eq 2)) {
	Write-Host "usage : <nom_pgm>  <répertoire>  <regex  *.txt>  (tout ce qui se termine par .txt)" -ForegroundColor Red
	Write-Host "exemple : ./cherche.ps1   $env:username/Music   *doors*" -ForegroundColor Blue
}
else {
	$rep = $args[0]
	$regex = $args[1]
	Write-Host "rep = $($rep)"
	Write-Host "regex = $($regex)"
	
	measure-Command {
		$files = Get-ChildItem -LiteralPath $rep  -recurse -Include $regex
		$nFich = 1
		$nRep = 1
		# $tFich = @()#The @ indicates an array. @() simply creates an empty array
		$tFich=[System.Collections.ArrayList]@()
		# $tFich.count
		# $tRep = @()
		$tRep=[System.Collections.ArrayList]@()
		# Write-Host $tRep.GetType()
		foreach ($file in $files) {
			Write-Host $file
			$s = $file.FullName.Substring(0, $file.FullName.Length - $file.name.Length)
			if (Test-Path -LiteralPath $file.FullName -PathType Leaf) {
				#a file
				$s = "$($nFich)    $($file.name)    ::    $($s)"# add in array
				# Write-Host $s -ForegroundColor Green
				$nFich++
				$tFich += $s
			}
			elseif (Test-Path -LiteralPath $file.FullName -PathType Container) {
				#a dir
				$s = "$($nRep)    $($file.name)    ::    $($s)"
				# Write-Host $s -ForegroundColor Blue
				$nRep++
				$tRep += $s
			}
			else {
				#not file & not dir
				$file.path
				$s = "$($file.name)    ::    $($s)"
				Write-Host $s -ForegroundColor Red
			}
		}
		foreach ( $a in $tFich ) {
			Write-Host $a -ForegroundColor Green
		}
		foreach ( $a in $tRep ) {
			Write-Host $a -ForegroundColor Blue
		}
	}
	# Get-ChildItem -Path $rep  -recurse -Include $regex
	# $r = Measure-Command -Expression {
	# 	Get-ChildItem -Path $rep  -recurse -Include $regex | ForEach-Object {    
	# 		# Write-Host(('"{0}","{1}","{2}"' -f $_.Name, $_.CreationTime, $_.Directory))
	# 	} }
	# Write-Host("ForEach-Object -Parallel : ", $r.TotalSeconds)

	# $r = Measure-Command -Expression {
	# 	foreach ( $a in Get-ChildItem -Path $rep  -recurse -Include $regex  ) {   
	# 		# Write-Host(('"{0}","{1}","{2}"' -f $_.Name, $_.CreationTime, $_.Directory))
	# 	} }
	# Write-Host("ForEach : ", $r.TotalSeconds)
}


#ForEach vs ForEach-Object
# PowerShell - Les boucles ForEach
# https://youtu.be/h4z610jQANM?t=495
# https://stackoverflow.com/questions/65281667/get-childitem-foreach-object-vs-foreach-issue

#-LiteralPath
# https://www.reddit.com/r/PowerShell/comments/f6zlbp/path_vs_literalpath/
# https://stackoverflow.com/questions/28611307/literalpath-option-for-cmdlet