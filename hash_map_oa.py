# Name: Frank Hodges
# OSU Email: hodgesf@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - hashmap open addressing
# Due Date: 12/7
# Description: hash map implementation using open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key/value pair is added. The table resizes to double its current
        capacity when this method is called and the current load factor of the table is
        greater than or equal to 0.5
        """
        # Check if resizing is needed due to high load factor
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)  # Resize table if load factor exceeds 0.5 to double current capacity

        # Calculate the hash key using the hash function
        hash_key = self._hash_function(key) % self._capacity

        # Initialize quadratic probing
        probe = 0
        while True:
            # Compute the next quadratic probing position
            quad_key = (hash_key + probe ** 2) % self._capacity
            entry = self._buckets.get_at_index(quad_key)

            # If the bucket is empty or contains a tombstone, insert the entry
            if entry is None or entry.is_tombstone:
                self._buckets.set_at_index(quad_key, HashEntry(key, value))
                self._size += 1
                return

            # If the key matches, update the value and handle tombstones
            if entry.key == key:
                if entry.is_tombstone:
                    self._size += 1
                    entry.is_tombstone = False
                entry.value = value
                return

            probe += 1  # Increment quadratic probing

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size / self._capacity  # Calculate and return the load factor

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        count_empty = 0
        for bucket in range(self._buckets.length()):
            if self._buckets.get_at_index(bucket) is None:
                count_empty += 1
        return count_empty  # Return the count of empty buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs remain in the new hash map and all hash table links are rehashed.
        new_capacity must be > current number of elements in the hash map. If not, the method does nothing.
        Checks if new_capacity is a prime number. If not, it rounds up to the nearest prime number.
        """
        # Check if new_capacity is less than or equal to the current number of elements
        if new_capacity <= self._size:
            return  # Do nothing if the new capacity is not sufficient

        # Check if the new_capacity is a prime number, and round up if not
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new hash map with the updated capacity
        new_table = HashMap(new_capacity, self._hash_function)

        # Rehash and insert all existing key/value pairs into the new hash map
        [new_table.put(item.key, item.value) for item in self if item]

        # Update the current hash map with the new values
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table.get_capacity()

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, then the method returns None.
        """
        # Calculate the hash key for the provided key
        hash_key = self._hash_function(key) % self._capacity

        probe = 0
        while True:
            # Apply quadratic probing to find the correct position or an empty slot
            quad_key = (hash_key + probe ** 2) % self._capacity
            entry = self._buckets.get_at_index(quad_key)

            if entry is None or entry.is_tombstone:
                # If the slot is empty or contains a tombstone, the key is not in the map
                return None

            if entry.key == key and not entry.is_tombstone:
                # Key found and it's not a tombstone; return the associated value
                return entry.value

            probe += 1  # Move to the next slot using quadratic probing

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False.
        An empty hash map does not contain any keys.
        """
        # Calculate the hash key for the provided key
        hash_key = self._hash_function(key) % self._capacity

        probe = 0
        while True:
            # Apply quadratic probing to find the correct position or an empty slot
            quad_key = (hash_key + probe ** 2) % self._capacity
            entry = self._buckets.get_at_index(quad_key)

            if entry is None or entry.is_tombstone:
                # If the slot is empty or contains a tombstone, the key is not in the map
                return False

            if entry.key == key and not entry.is_tombstone:
                # Key found and it's not a tombstone
                return True

            probe += 1  # Move to the next slot using quadratic probing

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing (no exceptions
        are raised).
        """
        # Calculate the hash key for the provided key
        hash_key = self._hash_function(key) % self._capacity

        probe = 0
        while True:
            # Apply quadratic probing to find the correct position or an empty slot
            quad_key = (hash_key + probe ** 2) % self._capacity
            entry = self._buckets.get_at_index(quad_key)

            if entry is None:
                # Key not found in the map
                return

            if entry.key == key and not entry.is_tombstone:
                # Key found and is not a tombstone, mark as tombstone and decrement the size
                entry.is_tombstone = True
                self._size -= 1
                return

            probe += 1  # Move to the next slot using quadratic probing

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        # Iterate through each bucket in the hash map
        for i in range(self._buckets.length()):
            # Set each bucket to None to clear its contents
            self._buckets.set_at_index(i, None)

        # Reset the size of the hash map to 0
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.
        """
        arr = DynamicArray()  # Create an empty dynamic array

        # Iterate through each bucket in the hash map
        for i in range(self._buckets.length()):
            current_entry = self._buckets.get_at_index(i)  # Get the current entry in the bucket

            # Check if the current entry is not None and not a tombstone
            if current_entry and not current_entry.is_tombstone:
                # Append a tuple containing key/value pair to the dynamic array
                arr.append((current_entry.key, current_entry.value))

        return arr  # Return the dynamic array containing key/value pairs

    def __iter__(self):
        """
        Enables the hash map to iterate across itself.
        A variable is initialized to track the iterator's progress
        through the hash map's contents.
        """
        self.index = 0
        return self

    def __next__(self):
        """
        This method returns the item in the hash map based on the current location of the iterator.
        """
        try:
            while self.index < self._capacity:
                value = self._buckets.get_at_index(self.index)  # Get the value at the current index
                self.index += 1  # Move to the next index

                # Check if the value is not None and not a tombstone
                if value and not value.is_tombstone:
                    return value  # Return the non-tombstone value

        except DynamicArrayException:
            pass  # Handle the end of the dynamic array

        raise StopIteration  # End of iteration, raise StopIteration to signify the end


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
