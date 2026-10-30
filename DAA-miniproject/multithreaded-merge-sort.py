import time
from concurrent.futures import ThreadPoolExecutor

def merge(left, right):
    """Merges two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def parallel_merge_sort(arr, executor, depth=0, max_depth=2):
    """Recursively sorts an array using multi-threading up to a fixed depth."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    # Fork tasks to worker threads if we haven't hit max thread depth limit
    if depth < max_depth:
        future_left = executor.submit(parallel_merge_sort, arr[:mid], executor, depth + 1, max_depth)
        future_right = executor.submit(parallel_merge_sort, arr[mid:], executor, depth + 1, max_depth)
        
        # Await thread execution completions and merge
        return merge(future_left.result(), future_right.result())
    else:
        # Fall back to single-threaded sequential execution to avoid excessive thread creation overhead
        left_sorted = parallel_merge_sort(arr[:mid], executor, depth + 1, max_depth)
        right_sorted = parallel_merge_sort(arr[mid:], executor, depth + 1, max_depth)
        return merge(left_sorted, right_sorted)

if __name__ == "__main__":
    # Test array with 20 elements
    test_array = [45, 12, 89, 5, 67, 34, 91, 23, 76, 3, 54, 88, 19, 62, 7, 41, 99, 31, 15, 80]
    
    print(f"Original Array: {test_array}")
    
    # Initialize pool with 4 worker threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        start_time = time.perf_counter()
        sorted_array = parallel_merge_sort(test_array, executor)
        end_time = time.perf_counter()
        
    time_taken = end_time - start_time
    
    print(f"Sorted Array  : {sorted_array}")
    print(f"Time Taken    : {time_taken:.8f} seconds")
