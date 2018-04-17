set arg1=%1
set arg2=%2
FOR /F %%i IN (%arg1%.dirlist) DO CodeCoverage %%i %arg1% %arg2%