function wait(seconds)
    local start = os.time()
    repeat until os.time() > start + seconds
end


echo(true)
if spawn([[.\ssh.exe]],"-o UserKnownHostsFile=/dev/null","-o StrictHostKeyChecking=no","-L PORT:IP:PORT", "-L PORT:IP:PORT", "-L PORT:IP:PORT", "user@".. arg[3]) then
    expect("password:")
    echo(false)
    send("password\r")
    expect("~ $")
    send("nohup bash -c 'source script/stream_cam.script' &\r")
    send("\r")
    wait(2)
    send("\r")
    send("PROCESS=$(ps aux | grep mjpg | awk '{print $2}')")
    send("\r")
    send("PROCESS_COUNT=$(echo \"${PROCESS}\" | awk 'END {print NR}')")
    send("\r")
    send("echo $PROCESS_COUNT")
    send("\r")
    send("python3 ~/script/Comm_rasp_client.py  " .. arg[1] .. " " .. arg[2] .." $PROCESS")
    send("\r")
end