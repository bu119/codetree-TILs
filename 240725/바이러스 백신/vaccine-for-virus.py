# M개의 병원을 적절히 골라 최대한 빨리 바이러스를 없애
# 골라진 병원들을 시작으로 매 초마다 상하좌우로 인접한 지역 중 벽을 제외한 지역에 백신이 공급
# queue
# 바이러스를 전부 없애는데 걸리는 시간 중 최소 시간


from itertools import combinations
from collections import deque

# 3.dfs 4방향 탐색 -> 최소 시간 반환
def bfs(startingPoint):
    queue = deque()
    visited = [[-1] * n  for _ in range(n)]
    for x, y in startingPoint:
        visited[x][y] = 0
        queue.append((x, y))
    # 방문한 바이러스 개수
    virusCnt = 0
    time = 0

    while queue:
        x, y = queue.popleft()

        if board[x][y] == 0 and time < visited[x][y]:
            time = visited[x][y]
            # 최소 시간을 넘으면 탐색 종료
            if time >= minV:
                return time
            
        for k in range(4):
            nx = x + di[k]
            ny = y + dj[k]
            if 0 <= nx < n and 0<= ny < n and visited[nx][ny] == -1 and board[nx][ny] != 1:
                visited[nx][ny] = visited[x][y] + 1
                # 바이러스 이면
                if board[nx][ny] == 0:
                    virusCnt += 1
                queue.append((nx, ny))

    # 모든 바이러스를 제거 못 했으면 최대 값 반환
    if virusCnt != totalVirus:
        return 250
    return time

n, m = map(int, input().split())
# 전체 바이러스 개수 저장
totalVirus = 0
hospitals = []
board = []
# 최소 시간 저장
minV = 250

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        # 바이러스이면 개수 세기
        if row[j] == 0:
            totalVirus += 1
        # 병원이면 저장
        elif row[j] == 2:
            hospitals.append((i,j))
    # N*N 배열 만들기
    board.append(row)

di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]

# 1.병원 m개 고르고
# 2.선택된 m개의 병원 탐색
for selectedHospitals in combinations(hospitals, m):
    time = bfs(selectedHospitals)
    # 최소값 갱신
    if time < minV:
        minV = time

# 4.모든 바이러스 없앴는지 확인 -> 불가면 -1 반환
if minV == 250:
    print(-1)
else:
    print(minV)