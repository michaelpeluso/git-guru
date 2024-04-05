import java.util.Iterator;
import java.util.Random;
import java.util.Vector;

public class BST_Tests {

    public static void main(String[] args) {
        
        test0();
        test1();
        test2();
        test3();
        test4();
        test5();
        test6();
        test7();
        test8();
        test9();
    }

    // cover most possibilites
    public static void test0() {
    
	BinaryTree<Integer> tree = new BinarySearchTree<Integer>();
	Random rand = new Random(1);
	int num = 1000;

	for (int i = 0; i < num; ++i) {
	    tree.insert(rand.nextInt(num));
	    tree.search(rand.nextInt(num));
	    tree.remove(rand.nextInt(num));
	}
    }
    
    // duplicates
    public static void test1() {
    
	    BinaryTree<Integer> tree = new BinarySearchTree<Integer>();
	    int num = 10;
	    
	    for (int i = 0; i < num; ++i) {
	    	tree.insert(5);
	    }
	    
	    for (int i = 0; i < num + 1; ++i) {
	    	tree.remove(5);
	    }

	    
    }
    
    // doubles
    public static void test2() {
    
    	    BinaryTree<Double> tree = new BinarySearchTree<Double>();
    	    tree.insert(2.5);
    	    tree.insert(2.4);
    	    tree.insert(2.3);
    	    tree.insert(2.2);
    	    tree.insert(2.1);
    	    tree.insert(2.0);
    	    tree.search(2.0);
    }
    
    // strings
    public static void test3() {
    
    	    BinaryTree<String> tree = new BinarySearchTree<String>();
    	    tree.insert("");
    	    tree.insert(" ");
    	    tree.insert("string");
    	    tree.search("string");
    	    tree.search("stringa");
    	    tree.insert("STRING");
    	    tree.insert("1");
    	    tree.insert("1.1");
    }
    
    // single root
    public static void test4() {
    
    	    BinaryTree<Integer> tree = new BinarySearchTree<Integer>();
    	    tree.insert(3);
    }
    
    // no root
    public static void test5() {
    
    	    BinaryTree<Integer> tree = new BinarySearchTree<Integer>();
    }
    
    // insert & remove root
    public static void test6() {
    
    	    BinaryTree<Integer> myTree = new BinarySearchTree<Integer>();
    	    myTree.remove(2);
    	    myTree.search(2);
    }
    
    // removing single root child
    public static void test7() {
    
    	    BinaryTree<Integer> tree = new BinarySearchTree<Integer>();
    	    tree.insert(3);
    	    tree.insert(2);
    	    tree.remove(3);
    }
    
    // negatives
    public static void test8() {
    
    	    BinaryTree<Integer> tree = new BinarySearchTree<Integer>();
    	    tree.insert(-3);
    	    tree.insert(3);
    	    tree.insert(-2);
    	    tree.insert(-4);
    }
    
    // single-child link
    public static void test9() {
    
    	    BinaryTree<Integer> tree = new BinarySearchTree<Integer>();
    	    
    	    // root.left.right
    	    tree.insert(10);
    	    tree.insert(5);
    	    tree.insert(7);
    	    
    	    // root.left.left
    	    tree.insert(10);
    	    tree.insert(5);
    	    tree.insert(2);
    	    
    	    // root.right.right
    	    tree.insert(10);
    	    tree.insert(7);
    	    tree.insert(8);
    	    
    	    // root.right.left
    	    tree.insert(10);
    	    tree.insert(7);
    	    tree.insert(5);
    }
}

