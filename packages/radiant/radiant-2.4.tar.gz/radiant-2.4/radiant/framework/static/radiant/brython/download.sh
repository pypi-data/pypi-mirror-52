#!/usr/bin/bash

echo "Removing old files"
mkdir old
mv brython.js old/
mv brython_stdlib.js old/
mv brython_modules.js old/

echo "Downloading new files"
wget http://brython.info/src/brython.js
wget http://brython.info/src/brython_stdlib.js
echo "Done"
 
