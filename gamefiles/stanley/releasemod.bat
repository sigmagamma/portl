set token=%1
set tag=%2
echo %token% | gh auth login --with-token
::gh release create %tag% --title "The Stanley Parable Hebrew" --notes "See [Installation guide](https://docs.google.com/document/d/1lsCQosS-TDPFxHi6mnZCE653AfrbqW5MhDCbnV-U_Ds/edit?usp=sharing)."
cd gamefiles\stanley\dist
for /r %%i in (*) do gh release upload --clobber %tag% %%i
cd ..\..\..