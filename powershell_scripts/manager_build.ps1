Set-PSDebug -Trace 1
docker build -t manager_build -f dockerfile_manager .
Set-PSDebug -Trace 0