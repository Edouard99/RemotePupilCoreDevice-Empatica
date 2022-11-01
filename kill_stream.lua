function wait(seconds)
    local start = os.time()
    repeat until os.time() > start + seconds
end
echo(true)
proc_list="kill -9 " .. arg[1]
string=proc_list.."\r"
echo(string)
if spawn([[.\ssh.exe]],"-o UserKnownHostsFile=/dev/null","-o StrictHostKeyChecking=no","user@"..arg[2],string) then
    expect("password:")
    echo(false)
    send("password\r")
end
