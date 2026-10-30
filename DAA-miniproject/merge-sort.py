import time

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    merge_sort(left_half)
    merge_sort(right_half)

    i = j = k = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

if __name__ == "__main__":
    # Defined array with exactly 20 unsorted integer elements
    test_array = [45, 12, 89, 5, 67, 34, 91, 23, 76, 3, 54, 88, 19, 62, 7, 41, 99, 31, 15, 80]
    
    print(f"Original Array: {test_array}")
    
    # Track the precise execution window
    start_time = time.perf_counter()
    merge_sort(test_array)
    end_time = time.perf_counter()
    
    time_taken = end_time - start_time
    
    print(f"Sorted Array  : {test_array}")
    print(f"Time Taken    : {time_taken:.8f} seconds")
