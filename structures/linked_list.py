class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    def append(self, data):

        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node

    def display(self):

        current = self.head

        while current:
            print(current.data)
            current = current.next

    def to_list(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

    def find_first(self, predicate):
        current = self.head
        while current:
            if predicate(current.data):
                return current.data
            current = current.next
        return None

    def remove_first(self, predicate):
        current = self.head
        prev = None

        while current:
            if predicate(current.data):
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next

        return False

    def clear(self):
        self.head = None
