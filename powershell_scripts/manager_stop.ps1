$host.UI.RawUI.WindowTitle = "Stopping manager"
$Container_name = "manager"
Set-PSDebug -Trace 1
docker stop $Container_name
Set-PSDebug -Trace 0