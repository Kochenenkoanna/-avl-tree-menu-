class StackNode:
    __slots__ = ("data", "next")
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
    
    def push(self, item):
        new_node = StackNode(item)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        if self.top is None:
            return None
        item = self.top.data
        self.top = self.top.next
        self.size -= 1
        return item
    
    def is_empty(self):
        return self.top is None
    
    def peek(self):
        return self.top.data if self.top else None


class DishNode:
    __slots__ = ("name", "price", "left", "right", "height")
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.left = None
        self.right = None
        self.height = 1


def _height(node):
    return 0 if node is None else node.height


def _update_height(node):
    if node:
        node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node):
    if node is None:
        return 0
    return _height(node.left) - _height(node.right)


def _rotate_right(y):
    x = y.left
    if x is None:
        return y
    
    T2 = x.right
    x.right = y
    y.left = T2
    
    _update_height(y)
    _update_height(x)
    return x


def _rotate_left(x):
    y = x.right
    if y is None:
        return x
    
    T2 = y.left
    y.left = x
    x.right = T2
    
    _update_height(x)
    _update_height(y)
    return y


def _rebalance(node):
    if node is None:
        return None
    
    _update_height(node)
    balance = _balance_factor(node)
    
    if balance > 1:
        if _balance_factor(node.left) < 0:
            node.left = _rotate_left(node.left)
        return _rotate_right(node)
    
    if balance < -1:
        if _balance_factor(node.right) > 0:
            node.right = _rotate_right(node.right)
        return _rotate_left(node)
    
    return node


def avl_insert(root, name, price):
    if root is None:
        return DishNode(name, price)
    
    if name.lower() < root.name.lower():
        root.left = avl_insert(root.left, name, price)
    elif name.lower() > root.name.lower():
        root.right = avl_insert(root.right, name, price)
    else:
        root.price = price
        return root
    
    return _rebalance(root)


def avl_search(root, name):
    if root is None:
        return None
    
    if name.lower() < root.name.lower():
        return avl_search(root.left, name)
    elif name.lower() > root.name.lower():
        return avl_search(root.right, name)
    else:
        return root

def avl_delete(root, name):
    if root is None:
        return None
    if name.lower() < root.name.lower():
        root.left = avl_delete(root.left, name)
    elif name.lower() > root.name.lower():
        root.right = avl_delete(root.right, name)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        min_right = root.right
        while min_right.left:
            min_right = min_right.left
        
        min_right_original_name = min_right.name
        
        root.name = min_right.name
        root.price = min_right.price
        
        root.right = avl_delete(root.right, min_right_original_name)

    _update_height(root)
    return _rebalance(root)

def avl_size(root):
    if root is None:
        return 0
    return 1 + avl_size(root.left) + avl_size(root.right)


def avl_height(root):
    return _height(root)

class TreeIterator:
    def __init__(self, root):
        self.stack = Stack()  
        self._push_left(root)
    
    def _push_left(self, node):
        while node:
            self.stack.push(node)
            node = node.left
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.stack.is_empty():
            raise StopIteration
        
        node = self.stack.pop()
        
        if node.right:
            self._push_left(node.right)
        
        return (node.name, node.price)


class MenuManager:
    def __init__(self):
        self.root = None
    
    def add(self, name, price):
        if price <= 0:
            return False
        self.root = avl_insert(self.root, name, price)
        return True
    
    def remove(self, name):
        if self.root is None:
            return False
        old_root = self.root
        self.root = avl_delete(self.root, name)
        return self.root != old_root
    
    def get_price(self, name):
        node = avl_search(self.root, name)
        return node.price if node else None
    
    def __iter__(self):
        return TreeIterator(self.root)
    
    def print_menu(self):
        if self.root is None:
            print("Меню пусто")
            return
        
        print("\n" + "="*50)
        print("МЕНЮ СТОЛОВОЙ 'МАРИЯ'")
        print("="*50)
        
        for name, price in self:
            print(f"  {name:35} {price:5d} руб.")
        
        print("="*50)
        print(f"Всего блюд: {avl_size(self.root)}")
        print(f"Высота дерева: {avl_height(self.root)}")
    
    def count(self):
        return avl_size(self.root)
    
    def clear(self):
        self.root = None