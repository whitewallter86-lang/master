
n, m = map(int, input().split())


first_list = list(map(int, input().split()))

second_list = list(map(int, input().split()))


for num in second_list:

    first_occurrence = -1
    for i in range(n):
        if first_list[i] == num:
            first_occurrence = i + 1  
            break
    
    if first_occurrence == -1:
        print(0)
    else:
        last_occurrence = first_occurrence
        for i in range(first_occurrence - 1, n):
            if first_list[i] == num:
                last_occurrence = i + 1
        
        print(first_occurrence, last_occurrence)