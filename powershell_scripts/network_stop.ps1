$host.UI.RawUI.WindowTitle = "Control Shell"
[console]::WindowWidth=180
[console]::WindowHeight=50
[console]::BufferWidth=[console]::WindowWidth

start pwsh (".\manager_stop.ps1")

$AmountMembers=$args[0]

$ID=1
while($ID -lt ($AmountMembers + 1)) {
  start pwsh (".\member_stop.ps1 $ID")
  $ID++
}