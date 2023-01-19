$host.UI.RawUI.WindowTitle = "Control Shell"

[console]::WindowWidth=180
[console]::WindowHeight=50
[console]::BufferWidth=[console]::WindowWidth

Write-Host -ForegroundColor DarkYellow "Building manager"
& .\manager_build.ps1
Write-Host -ForegroundColor DarkYellow "Manager done."

Write-Host -ForegroundColor DarkYellow "Building member"
& .\member_build.ps1
Write-Host -ForegroundColor DarkYellow "Member done."
