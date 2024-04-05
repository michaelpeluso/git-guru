#!/bin/bash

# compile
javac -g BinarySearchTree.java BinaryTree.java BST_Tests.java

# DynComp - generate comparability info
java -cp .:$DAIKONDIR/daikon.jar daikon.DynComp BST_Tests

# generate invarients 
java -cp .:$DAIKONDIR/daikon.jar daikon.Chicory --daikon --comparability-file=BST_Tests.decls-DynComp BST_Tests

# view results
java -cp $DAIKONDIR/daikon.jar daikon.PrintInvariants BST_Tests.inv.gz
