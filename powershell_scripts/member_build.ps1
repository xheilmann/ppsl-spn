Set-PSDebug -Trace 1
docker build -t member_build  -f dockerfile_member .
Set-PSDebug -Trace 0