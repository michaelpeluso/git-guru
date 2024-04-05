# Binary Search Tree Implementation in Java

This Java project provides an implementation of a Binary Search Tree (BST). The BST is a fundamental data structure that allows for efficient searching, insertion, and removal of elements, providing an average-case time complexity of O(log n) for these operations.

## Files

1. **BinaryTree.java**: This file contains an abstract class `BinaryTree` that defines the basic structure of a binary tree. It includes inner class `Node` representing a node in the tree, and abstract methods for insertion, removal, and searching within the tree.

2. **BinarySearchTree.java**: This file extends the `BinaryTree` class and implements the functionality specific to a binary search tree. It includes methods for insertion, removal, and searching, along with helper methods for tree traversal and manipulation.

3. **BST_Tests.java**: This file contains a series of test cases to validate the functionality of the `BinarySearchTree` class. The test suite covers various scenarios including inserting, removing, and searching elements in the tree, handling duplicates, different data types (integer, double, string, etc.), and edge cases like empty tree or single-node tree.

4. **Daikon_Testing**: This directory includes a .sh and a .txt file. `run_tests.sh` is a bash script that executes the necessary commands to generate `BST_Tests.txt` using [The Daikon Invariant Detector](https://plse.cs.washington.edu/daikon/download/doc/daikon.html). BST_Tests.txt contains an expressive list of generated invariants for this data structure.

## Usage

To use the `BinarySearchTree` class, follow these steps:

1. Import the `BinarySearchTree` class into your Java project.
2. Create an instance of `BinarySearchTree` for the desired data type.
3. Use the `insert`, `remove`, and `search` methods to manipulate the tree as needed.
4. Optionally, iterate through the elements of the tree using the provided iterator.

```java
BinarySearchTree<Integer> tree = new BinarySearchTree<>();
tree.insert(10);
tree.insert(5);
tree.insert(15);
System.out.println(tree.search(5)); // Output: true
tree.remove(5);
System.out.println(tree.search(5)); // Output: false
```

## Testing

The `BST_Tests.java` file contains a series of test cases to verify the correctness of the `BinarySearchTree` implementation. Each test case covers specific scenarios and edge cases to ensure the robustness of the implementation.

To run the tests, you can follow these steps:

```bash
javac BST_Tests.java
java BST_Tests
```

