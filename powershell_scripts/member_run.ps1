$ID=$args[0]
$host.UI.RawUI.WindowTitle = "Member $ID"
$Container_name = "member$ID"
Set-PSDebug -Trace 1
docker run --rm --name $Container_name --network spn_overlay --ip 10.0.1.1$ID -e CONFIG_FILE_LOCATION="./resources/config/config.ini" -e ID_OF_MEMBER="$ID" member_build
Set-PSDebug -Trace 0
