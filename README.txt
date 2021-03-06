Automatic Fortran makefile maker. The script (gen_make.py) first scans all Fortran files for imports of other source files and creates a directed dependency graph, where each vertex represents the file and an arrow from A to B
correspond to the File A depending on B. It then condenses the graph, i.e. creates a new graph whose vertices are connected components (CC) of the original graph and arrows between 
vertices A' and B' are present iff any vertex of the CC  corresponding to A' points to any vertex of the CC  corresponding to B'. 
This is useful, because the connected components represent circularly dependent graphs, they have to be compiled together. If any file in a CC is changed,  all files in the same CC must be recompiled, as well as all files in CCs
that depend on the changed CC. However, the files in CCs that do not depend on the changed CC do not have to be compiled. See an example in orig_structure.png and condensed_structure.png. 
Finaly, it creates a makefile from this condenseded dependency structure. The initial part of the makefile is copied from mkfilegen/preamble.txt, please  make sure to create your own version of this file. At the very least, 
you need to fill the $NAME, $COMPILER and $FLAGS variables.
