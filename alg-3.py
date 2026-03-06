
def find_closest(arr, target):
    left, right = 0, len(arr) - 1
    closest = arr[0]
    min_diff = abs(arr[0] - target)
    
    while left <= right:
        mid = (left + right) // 2
        diff = abs(arr[mid] - target)
        
        if diff < min_diff or (diff == min_diff and arr[mid] < closest):
            min_diff = diff
            closest = arr[mid]
        
        if arr[mid] < target:
            left = mid + 1
        elif arr[mid] > target:
            right = mid - 1
        else:
            return arr[mid]
    
    return closest

n, k = map(int, input().split())
first_array = list(map(int, input().split()))
second_array = list(map(int, input().split()))

for num in second_array:
    result = find_closest(first_array, num)
    print(result)