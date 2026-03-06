
from collections import deque

def find_shortest_path():
    n = int(input())
    graph = []
    for i in range(n):
        row = list(map(int, input().split()))
        graph.append(row)
    
    start, end = map(int, input().split())
    start -= 1  
    end -= 1
    
    if start == end:
        print(0)
        return

    queue = deque([start])
    visited = [False] * n
    parent = [-1] * n
    visited[start] = True
    
    while queue:
        current = queue.popleft()
        
        for neighbor in range(n):
            if graph[current][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = current
                queue.append(neighbor)
                
                if neighbor == end:
                    path = []
                    node = end
                    while node != -1:
                        path.append(node + 1)  
                        node = parent[node]
                    path.reverse()
                    
                    print(len(path) - 1)
                    print(*path)
                    return
    
    print(-1)

find_shortest_path()