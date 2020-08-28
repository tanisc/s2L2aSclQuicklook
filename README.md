# s2L2aSclQuicklook
Produces quicklooks of SCL bands in Sentinel-2 L2A SAFE folders (use after unzipping). Pass the directory where SAFE files are as sys.argv[1]. 
Writes results to same directory. 
Produces grayscale image for SCL and false color image for snow(red)-nosnow(green). Uses only the best resolution available inside the file.
