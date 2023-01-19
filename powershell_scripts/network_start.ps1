$host.UI.RawUI.WindowTitle = "Control Shell"
[console]::WindowWidth=180
[console]::WindowHeight=50
[console]::BufferWidth=[console]::WindowWidth

start pwsh (".\manager_run.ps1")

Start-Sleep -Seconds 15

$AmountMembers= $args[0]

$ID=1
while($ID -lt ($AmountMembers + 1)) {
  start pwsh (".\member_run.ps1 $ID")
  $ID++
}






