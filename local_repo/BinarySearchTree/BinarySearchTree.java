import java.util.Iterator;
import java.util.Vector;

public class BinarySearchTree<E extends Comparable<? super E>> extends BinaryTree<E> {

    private Node<E> privateInsert(Node<E> root, E data) {
        if (root == null) {
            return new Node<>(data);
        }
        else if (data.compareTo(root.data) > 0) {
            root.right = privateInsert(root.right, data);
        } 
        else if (data.compareTo(root.data) < 0) {
            root.left = privateInsert(root.left, data);
        }
        return root;
    }

    public void insert(E data) {
        root = privateInsert(root, data);
    }

    private Node<E> privateRemove(Node<E> root, E data) {
        if (root == null) {
            return null;
        }
        if (data.compareTo(root.data) < 0) {
            root.left = privateRemove(root.left, data);
        } 
        else if (data.compareTo(root.data) > 0) {
            root.right = privateRemove(root.right, data);
        } 
        else {
            if (root.left == null) {
                return root.right;
            } else if (root.right == null) {
                return root.left;
            }
            root.data = lowestValue(root.right);
            root.right = privateRemove(root.right, root.data);
        }
        return root;
    }

    private E lowestValue(Node<E> root) {
        E min = root.data;
        while (root.left != null) {
            min = root.left.data;
            root = root.left;
        }
        return min;
    }

    public boolean search(E data) {
        return privateSearch(root, data);
    }

    private boolean privateSearch(Node<E> root, E data) {
        if (root == null) {
            return false;
        }
        else if (data.equals(root.data)) {
            return true;
        } 
        else if (data.compareTo(root.data) > 0) {
            return privateSearch(root.right, data);
        } 
        else {
            return privateSearch(root.left, data);
        }
    }

    public Iterator<E> iterator() {
        Vector<E> vector = new Vector<>();
        traverse(root, vector);
        return vector.iterator();
    }

    private void traverse(Node<E> root, Vector<E> vector) {
        if (root != null) {
            traverse(root.left, vector);
            vector.add(root.data);
            traverse(root.right, vector);
        }
    }
    
    @Override
    public void remove(E data) {
        root = privateRemove(root, data);
    }
}

