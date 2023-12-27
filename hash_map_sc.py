# Name: Frank Hodges
# OSU Email: hodgesf@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - hashmap separate chaining
# Due Date: 12/7
# Description: hash map implementation using separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates the key/value pair in the hash map.
        If the given key exists, then associated value is replaced by new value.
        If given key is not in the hash map, a new key/value pair must be added.
        The table is resized to double its current capacity when current load factor is >= 1.0.
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hash_key = self._hash_function(key) % self._capacity
        chain_key = self._buckets.get_at_index(hash_key)

        # Iterate through the linked list and update value if the key exists
        for item in chain_key:
            if item.key == key:
                item.value = value
                return

        # If the key doesn't exist in the linked list, insert a new entry
        chain_key.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_bucket_count = 0  # O(1) - Initialize counter for empty buckets
        for bucket_index in range(self._capacity):  # O(n) - Iterate through all buckets
            # Access the linked list (chain) at the current bucket index and check its length
            if self._buckets.get_at_index(bucket_index).length() == 0:  # O(1) - Access length of the linked list
                empty_bucket_count += 1  # O(1) - Increment count if the linked list is empty

        return empty_bucket_count  # O(1) - Return the count of empty buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        Load factor is the average number of elements stored in the bucket.
        Load factor = total number of elements stored in the table / number of buckets.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        empty_bucket = LinkedList()  # Create an empty LinkedList instance

        # Resetting the hash map's contents
        self._buckets = DynamicArray()
        self._size = 0

        # Fill the buckets with empty linked lists
        for _ in range(self._capacity):
            self._buckets.append(empty_bucket)

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs must remain in the new hash map, and all hash table links are rehashed.
        It first checks that new_capacity is not less than 1. If it is, then it does nothing.
        If new_capacity >= 1, it makes sure that it is a prime number. If not, then it will round up to the
        next highest prime number.
        """

        # Ensure the new capacity is valid
        if new_capacity < 1:
            return  # Do nothing if the new capacity is invalid

        # Ensure new_capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)  # Find the next highest prime number

        # Create a new hash map with the new capacity
        new_table = HashMap(new_capacity, self._hash_function)

        # Special handling for new_capacity == 2
        if new_capacity == 2:
            new_table._capacity = 2

        # Copy elements from the old hash table to the new one
        for i in range(self._capacity):
            # Iterate through each bucket in the old table
            if self._buckets.get_at_index(i).length() > 0:
                # If the bucket is not empty
                for item in self._buckets.get_at_index(i):
                    # Iterate through each item in the bucket
                    new_table.put(item.key, item.value)  # Add item to the new hash table

        # Update internal references to the new hash table
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table._capacity

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not in the hash map, return None.
        """

        # Get the hash value for the given key
        hash_key = self._hash_function(key) % self._capacity

        # Get the linked list (chain) at the hashed index
        chain_key = self._buckets.get_at_index(hash_key)

        # If the linked list is empty, the key doesn't exist, return None
        if chain_key.length() == 0:
            return None
        else:
            # Iterate through the linked list
            for item in chain_key:
                # If the current item's key matches the provided key, return its value
                if item.key == key:
                    return item.value

        # If the key is not found in the linked list, return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False.
        An empty hash map does not contain any keys.
        """

        # Iterate through each index within the hash table capacity
        for i in range(self._capacity):

            # Retrieve the linked list (bucket) at the current index
            bucket = self._buckets.get_at_index(i)

            # Check if the current bucket is not empty
            if bucket.length() > 0:

                # Iterate through each item in the bucket
                for item in bucket:

                    # Check if the key of the current item matches the given key
                    if item.key == key:
                        return True  # Return True if the key is found in the hash map

        return False  # Return False if the key is not found in any bucket of the hash map

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map,
        the method does nothing (no exception needs to be raised).
        """

        # Iterate through each index within the hash table capacity
        for i in range(self._capacity):

            # Retrieve the linked list (bucket) at the current index
            bucket = self._buckets.get_at_index(i)

            # Check if the current bucket is not empty
            if bucket.length() > 0:

                # Iterate through each item in the bucket
                for item in bucket:

                    # Check if the key of the current item matches the given key
                    if item.key == key:
                        bucket.remove(key)  # Remove the key from the bucket
                        self._size -= 1  # Decrement the size of the hash map
                        return  # Exit after removing the key

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        The order of the keys in the dynamic array does not matter.
        """

        # Create an empty dynamic array to store key-value pairs
        da = DynamicArray()

        # Iterate through each index within the hash table capacity
        for i in range(self._capacity):

            # Retrieve the linked list (bucket) at the current index
            bucket = self._buckets.get_at_index(i)

            # Check if the current bucket is not empty
            if bucket.length() > 0:

                # Iterate through each item in the bucket
                for item in bucket:
                    # Append a tuple of key and value to the dynamic array
                    da.append((item.key, item.value))

        # Return the dynamic array containing all key-value pairs
        return da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    A standalone function outside of the HashMap class that receives a dynamic array (not guaranteed to be sorted).
    Returns a tuple containing, in this order, a dynamic array comprising the mode (most occurring) value/s of the
    array, and an integer that represents the highest frequency (how many times they appear).

    If more than one value has the highest frequency, all values at that frequency are included in the array
    being returned (order does not matter). If there is only one mode, the dynamic array will only contain that
    value.

    The input array must contain at least one element, and all values stored in the array will be strings.

    Implemented in O(N) time complexity. A separate chaining hash map is recommended.
    """

    # Initialize a HashMap instance
    map = HashMap()

    # Iterate through the input dynamic array
    for i in range(da.length()):
        # Count occurrences of each value in the dynamic array using a HashMap
        if not map.contains_key(da.get_at_index(i)):
            map.put(da.get_at_index(i), 1)
        else:
            map.put(da.get_at_index(i), map.get(da.get_at_index(i)) + 1)

    # Initialize variables to track frequency and mode
    frequency = 0
    arr = map.get_keys_and_values()
    mode_arr = DynamicArray()

    # Determine the highest frequency in the HashMap
    for i in range(arr.length()):
        if frequency < arr.get_at_index(i)[1]:
            frequency = arr.get_at_index(i)[1]

    # Retrieve all values that match the highest frequency
    for i in range(arr.length()):
        if arr.get_at_index(i)[1] == frequency:
            mode_arr.append(arr.get_at_index(i)[0])

    # Return a tuple containing a dynamic array of the most frequent values and the frequency
    return mode_arr, frequency

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
