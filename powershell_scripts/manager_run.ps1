$host.UI.RawUI.WindowTitle = "Manager"

[console]::WindowWidth=250
[console]::WindowHeight=50
[console]::BufferWidth=[console]::WindowWidth

Set-PSDebug -Trace 1
docker run --rm --name manager --network spn_overlay --ip 10.0.1.10 -e CONFIG_FILE_LOCATION="./resources/config/config.ini" manager_build
Set-PSDebug -Trace 0
