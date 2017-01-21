import heapq
from collections import Sequence
from itertools import count
from typing import List, Any, Dict, TypeVar, Generic, Union, Tuple, Generator

T = TypeVar("T")
Priority = Union[int, float]
EntryAttributeType = Union[Priority, Dict, T]


# TODO: Update Docs for Min Heap, because its original name was priority queue


class Entry(Sequence, Generic[T]):
    """ Helper class to handle a entry in the MinHeap/priority queue

        This class inherits from the Sequence container, so it behaves like a Sequence when getting its attributes
        This is purely a personal preference
    """

    def __init__(self, priority: Priority, access_counter: Dict, item: T) -> None:
        self.priority, self.access_counter, self.item = priority, access_counter, item

    # noinspection PyTypeChecker
    # Doesn't  handle a generator correctly yet
    def __iter__(self) -> Generator[EntryAttributeType, None, None]:
        yield self.priority
        yield self.access_counter
        yield self.item

    def __getitem__(self, key: int) -> EntryAttributeType:
        if key == 0:
            return self.priority
        if key == 1:
            return self.access_counter
        if key == 2:
            return self.item
        else:
            raise IndexError()

    def __len__(self) -> int:
        return 3

    def __lt__(self, other):
        return (self.priority, self.access_counter, self.item) < (other.priority, other.access_counter, other.item)


class MinHeap(Generic[T]):
    """ Implements a priority queue using heapq (min heap)

        Has the functionality to push, pop, heapify update and pop_all from heap
        To build a a new object from a queue use the ''@classmethod PriorityQueue.build()''
    """

    REMOVED = '<removed-task>'  # placeholder for a removed task
    PRIORITY_CONSTANT = 1  # Means that priorities are positive and that this is a min heap

    def __init__(self):
        self._access_counter = count()
        self._queue = list()  # type: List[T]
        self.entry_finder = dict()  # type: Dict[T]

    def __len__(self):
        return len(self.entry_finder)

    def push(self, item: Any, priority: Priority = 0) -> None:
        """ Pushes/updates an item into/in the priority queue

        :param item: What will be the added to the priority queue
        :param priority: the item's priority
        """

        # Create the entry and update entry_finder
        entry = self.entry_handler(item, priority)
        # Add to heap
        heapq.heappush(self._queue, entry)

    def entry_handler(self, item: Any, priority: Priority = 0) -> Entry:
        """ Creates the entry that will be stored on the heap
`
        This function handles all the challenges in a good implementation of priority queue
        1 - Sort stability: how do you get two tasks with equal priorities to be returned in the order
        they were originally added?
        2 - Tuple comparison breaks for (priority, task) pairs if the priorities are equal and the tasks do
        not have a default comparison order. If the priority of a task changes, how do you move it to a new position
        in the heap? Or if a pending task needs to be deleted, how do you find it and remove it from the queue?

        The solution for these two challenges is the addition of a counter

        3 - If the priority of a task changes, how do you move it to a new position in the heap?
        4 - Or if a pending task needs to be deleted, how do you find it and remove it from the queue?

        The solution for these challenges is to keep an entry_finder dictionary that points to the entry in the
        priority queue

        :param item: What will be the added to the priority queue
        :param priority: the item's priority
        :return: Returns the entry object: ``entry = [priority, count, item]``, type: ``List[int, Dict, Any ]``
        """
        # Remove item from entry finder if it is there and mark the entry with the ''REMOVED'' flag
        if item in self.entry_finder:
            self.remove_task(item)
        # Update access counter
        access_counter = next(self._access_counter)
        # Add item to entry_finder and heap

        entry_priority = self.PRIORITY_CONSTANT * priority  # Multiply by 1/-1 depending between min and max heap
        entry = Entry(entry_priority, access_counter, item)  # Minus because we want a min heap
        self.entry_finder[item] = entry
        return entry

    def heapify(self, input_elements: List[Tuple[T, Priority]]):
        """ Implements a heapify functionality for the priority queue

        The reason why ``heapq.heapify`` can't be performed directly in input_elements is that we need to create and
        handle a new entry for every element in the input list


        .. seealso:: ''PriorityQueue.entry_handler''
        .. TODO:: Add support for Any type items instead of just int (right now they have to be the indexes)

        :param input_elements: List of either int of float priorities.
        :return:
        """
        entry_list = list()
        for item in input_elements:
            i, priority = item
            entry_list.append(self.entry_handler(i, priority=priority))
        heapq.heapify(entry_list)
        self._queue = entry_list

    def remove_task(self, item: T) -> None:
        """ Mark an existing task as REMOVED.

        Raise KeyError if not found.

        :param item: Item to remove
        """
        entry = self.entry_finder.pop(item)
        entry.item = self.REMOVED

    def pop(self) -> T:
        """ Pops an item from the priority queue

        This method continually pops elements until it finds one that doesn't have the ''REMOVED'' flag set
        Raise KeyError if key becomes empty before a valid item can be returned

        :return:
        """
        while self._queue:
            priority, access_counter, item = heapq.heappop(self._queue)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    @classmethod
    def build(cls, input_elements: List[Tuple[T, Priority]]) -> 'MinHeap':
        """ Builds the priority queue from an input by calling heapify

        :param input_elements:
        :return: Returns the new PriorityQueue object
        """

        new_queue = cls()
        new_queue.heapify(input_elements)
        return new_queue

    def pop_all(self) -> List[T]:
        """ Pops all valid elements from queue

        :return: Returns a 'list()' object with all the elements
        """
        output = list()
        while self._queue:
            output.append(self.pop())
        return output

    def contains_item(self, item):
        return item in self.entry_finder


class PriorityQueue(MinHeap):
    """ Implements a priority queue using heapq (min heap)

        Has the functionality to push, pop, heapify update and pop_all from heap
        To build a a new object from a queue use the ''@classmethod PriorityQueue.build()''
    """
    PRIORITY_CONSTANT = -1


def test_build():
    l = [2, 1, 10, 4, 5]
    pq = PriorityQueue.build([(i, priority) for i, priority in enumerate(l)])
    assert pq.pop_all() == [1, 0, 3, 4, 2][::-1]
