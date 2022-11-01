# ARG0 = IP_Computer; ARG1 =path to pupil capture (use a link); ARG2 = PID start_stream.ps1; ARG3 = IP Rasb

.\venv\Scripts\activate
Write-Output $Args[1]
$NUM = python .\Comm_rasp_server.py $Args[0]
$PROCRAS=$NUM.Split(" ")
Write-Output $NUM.Split(" ")
if ($PROCRAS.Count -eq 4){
    Write-Output "Stream of pupil has started"
    #Start-Process -FilePath "C:\Program Files (x86)\Pupil-Labs\Pupil v3.5.1\Pupil Capture v3.5.1\pupil_capture.exe"
    Start-Process -FilePath $Args[1]
    Start-Sleep -Seconds 7
    Write-Output "Capture is starting..."
    Write-Output $Args[2]
    $PROC=(Get-Process pupil_capture -ErrorAction SilentlyContinue)
    if($PROC){
        Write-Output "Capture has started"
        $EYE_0_ID=Start-Process .\venv\Scripts\python.exe '.\pupil_remote_v2\pupil-video-backend\eye0.py' -PassThru
        $EYE_1_ID=Start-Process .\venv\Scripts\python.exe '.\pupil_remote_v2\pupil-video-backend\eye1.py' -PassThru
        $WORLD_0_ID=Start-Process .\venv\Scripts\python.exe '.\pupil_remote_v2\pupil-video-backend\world.py' -PassThru
        $ALL_RUNNING=0
        while ($ALL_RUNNING -eq 0) {
            Start-Sleep -Seconds 1
            $EYE_0_PROCESS = Get-Process -Id $EYE_0_ID.Id -ErrorAction SilentlyContinue
            $EYE_1_PROCESS = Get-Process -Id $EYE_1_ID.Id -ErrorAction SilentlyContinue
            $WORLD_0_PROCESS = Get-Process -Id $WORLD_0_ID.Id -ErrorAction SilentlyContinue
            $ALL_RUNNING=1
            if (!$EYE_0_PROCESS){
                $EYE_0_ID=Start-Process .\venv\Scripts\python.exe '.\pupil_remote_v2\pupil-video-backend\eye0.py' -PassThru
                $ALL_RUNNING=0
            }
            if (!$EYE_1_PROCESS){
                $EYE_1_ID=Start-Process .\venv\Scripts\python.exe '.\pupil_remote_v2\pupil-video-backend\eye1.py' -PassThru
                $ALL_RUNNING=0
            }
            if (!$WORLD_0_PROCESS){
                $WORLD_0_ID=Start-Process .\venv\Scripts\python.exe '.\pupil_remote_v2\pupil-video-backend\world.py' -PassThru
                $ALL_RUNNING=0
            }
        }
        $COND=1
        while($COND -eq 1){
            $USERINPUT = Read-Host -Prompt "Write Q to close stream and Capture"
            if ($USERINPUT -eq "Q"){
                $COND=0
                Write-Output "Quitting..."
                $CAPTURE_ID=Get-Process pupil_capture | Select-Object -expand id
                $SSH_ID=Get-Process ssh | Select-Object -expand id
                Stop-Process -Id $CAPTURE_ID
                Stop-Process -Id $EYE_0_ID.Id
                Stop-Process -Id $EYE_1_ID.Id
                Stop-Process -Id $WORLD_0_ID.Id
                .\expect.exe .\kill_stream.lua $NUM $Args[3]
                # Stop-Process -Id $Args[2]
                Start-Sleep -Seconds 2
                Stop-Process -Id $SSH_ID
                Stop-Process -Id $PID

            }
        }
    }
    else{
        Write-Output "Capture could not be launched"
    }
}
else{
    Write-Output "An Error has occured in the pupil video stream"
}