
def assert_node_type(obj_type, prop, value):
    if not isinstance(value, obj_type):
        raise TypeError(f"Cannot set attribute `{prop}` to type {type(value)}")


class DLLNode:

    @property
    def prev(self):
        if hasattr(self, '_prev'):
            return self._prev
        return None

    @prev.setter
    def prev(self, value):
        assert_node_type(type(self), 'prev', value)
        self._prev = value


    @property
    def next(self):
        if hasattr(self, '_next'):
            return self._next
        return None

    @next.setter
    def next(self, value):
        assert_node_type(type(self), 'next', value)
        self._next = value

    @property
    def is_head(self):
        return self.next is None

    @property
    def is_root(self):
        return self.prev is None

    @property
    def is_detached(self):
        return self.is_head and self.is_root


class DLinkedList:

    def __init__(self, node_type):
        self._node_type = node_type
        self.root = None
        self.head = None

    def append_list(self, items):
        for item in items:
            self.append(item)

    def append(self, node):
        assert_node_type(self._node_type, 'append node', node)
        if self.head:
            self.head.next = node
            node.prev = self.head
        else:
            self.root = node

        self.head = node

    def append_list(self, nodes):
        for node in nodes:
            self.append(node)

    def get(self, func):
        for node in self:
            if func(node):
                return node

    def __getitem__(self, index):
        for node_index, node in enumerate(self):
            if node_index == index:
                return node
        raise IndexError('Index out of range')

    def __iter__(self):
        next = self.root
        while next:
            yield next
            next = next.next

    def __len__(self):
        cnt = 0
        next = self.root
        while next:
            cnt += 1
            next = next.next
        return cnt

    def last(self):
        last = None
        for node in self:
            last = node
        return last

    @property
    def is_empty(self):
        return not self.root

    @property
    def count(self):
        return len(self)
