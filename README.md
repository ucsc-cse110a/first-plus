# Calculation of FIRST, FOLLOW, FIRST+ Sets
Implementation of First+
Instructor: Marcelo Siero

## About first_follow.py
About programs to construct FIRST, FOLLOW and FIRST+ sets.

This is based on material from this site: 
   https://www.cs.uaf.edu/~cs331/notes/FirstFollow.pdf  
   Thanks to student Lauren Willey from CSE110A for help with this program
See the included FirstFollow.pdf in this file.

first_follow.py can take a grammar without left recursion and 
create a First+ set to convert that grammar to LL(1) or to prepare
it to create a Recursive Descent Compiler.

Various grammars were provided as input to test the latter program.
g_expr.py includes a grammar from our slides, also see the other
test grammars: g*.py  These tests different aspects of the First+
algorithm. 

You are welcome to use these programs to help you better understand
the FIRST, FOLLOW and FIRST+ algorithm.

I suggest you start out by running:
   python first_follow.py -h 
to get help on the various flags that the program accepts.

The -a flag will display the Grammar, also First Set, First including 
terminals, Follow Set, and First+ Set.
Without -a the program will only display the First+ set.

The -t flag will show the same sets but will include a tabular form.

