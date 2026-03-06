
from collections import deque

def bfs_shortest_path(graph, start, end):
    n = len(graph)
    visited = [False] * n
    queue = deque([(start, 0)])
    visited[start] = True
    
    while queue:
        vertex, distance = queue.popleft()
        
        if vertex == end:
            return distance
        
        for neighbor in range(n):
            if graph[vertex][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, distance + 1))
    
    return -1

n = int(input())
graph = []
for i in range(n):
    row = list(map(int, input().split()))
    graph.append(row)

start, end = map(int, input().split())
start -= 1
end -= 1

result = bfs_shortest_path(graph, start, end)
print(result)