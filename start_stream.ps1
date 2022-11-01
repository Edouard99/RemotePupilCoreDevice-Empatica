# ARG0 = IP_Computer ; ARG1 = Port_comm_rasp ; ARG2 = IP Rasb; ARG3=path to pupil capture (use a link)

.\venv\Scripts\activate
Write-Output $Args[2]
$strconc="-noexit -command & {.\video_redirect.ps1 "+$Args[1]+" "+$Args[3]+" "+$PID+" "+ $Args[2]+"}" 
Start-Process powershell -ArgumentList $strconc
#Start-Process powershell.exe -ArgumentList "-noexit -file C:\Users\Edouard\Desktop\Research Project\Network\video_redirect.ps1" -Wait
Start-Sleep -Seconds 3
Write-Output($PID)
.\expect.exe .\connect_rasp.lua $Args[0] $Args[1] $Args[2]