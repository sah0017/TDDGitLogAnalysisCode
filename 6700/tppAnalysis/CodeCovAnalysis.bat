set arg1=%1
FOR /F %%i IN (%arg1%.dirlist) DO CodeCoverage %%i %arg1%