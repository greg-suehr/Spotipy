#!/bin/bash

# A quick hack
for i in `find . -type f | egrep -v '~|git|cache'`; do echo "$i"; echo "grep 'TODO' $i"; grep -n 'TODO' $i; echo;  done | less

# A full solution? 
# - - - - - - - - - - 
# for each directory under the current directory
#  print the current directory
#  for each non-binary file
#   print the filename
#   track the objectname
#   track the methodname
#   search for pattern "# TODO:"
#   collate additional text after "#" on consequetive lines
#   print the objectname, methodname, TODO_text

