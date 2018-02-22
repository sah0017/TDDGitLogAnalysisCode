set arg1=%1
FOR /F %%i IN (%arg1%.dirlist) DO TAAutoGrader %%i %arg1%
