$host.UI.RawUI.WindowTitle = "Stopping member $args"
$Container_name = "member$args"
Set-PSDebug -Trace 1
docker stop $Container_name
Set-PSDebug -Trace 0