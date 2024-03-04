from copy import deepcopy
from collections import deque

# 기사 이동
def move_knight(starter, direction):
    global knightsInfo
    
    # 체스판에서의 기사 위치 저장
    knights = [[0]*l for _ in range(l)]
    # 살아있는 기사들 표시
    for num in knightsInfo:
        r, c, h, w, k, damage = knightsInfo[num]
        for x in range(r, r+h):
            for y in range(c, c+w):
                knights[x][y] = num

    # 방문 체크
    visited.add(starter)
    # 만난 순서대로 체크
    deq = deque()
    deq.append(starter)
    while deq:
        mover = deq.popleft()
        r, c, h, w, k, damage = knightsInfo[mover]

        if k <= damage or mover not in knightsInfo:
            continue

        for x in range(r, r + h):
            for y in range(c, c + w):
                nx = x + di[direction]
                ny = y + dj[direction]
                # 격자 밖으로 나가거나 벽을 만나면 이동 불가
                if 0 > nx or nx >= l or 0 > ny or ny >= l or graph[nx][ny] == 2:
                    return False
                # 빈 공간을 만나면 이동 가능 (이후 탐색 필요 없음)
                if knights[nx][ny] == 0:
                    continue
                
                # 다른 기사 만나면 방문 체크하고 계속 탐색
                if knights[nx][ny] != mover and knights[nx][ny] not in visited:
                    visited.add(knights[nx][ny])
                    deq.append(knights[nx][ny])
        
    # 이동 가능하면 밀린 기사 시작 위치 변경
    for num in visited:
        knightsInfo[num][0] += di[direction]
        knightsInfo[num][1] += dj[direction]
        
    return True

# 데미지 적용
def apply_damage(starter, direction):
    global knightsInfo

    # 이동한 기사들의 데미지 적용
    for num in visited:
        # 명령받은 기사는 통과
        if starter == num:
            continue
        r, c, h, w, k, damage = knightsInfo[num]
        # 데미지 적용
        for x in range(r, r + h):
            for y in range(c, c + w):
                knightsInfo[num][5] += graph[x][y]

        # 체력보다 데미지가 더 많으면 기사 삭제
        if knightsInfo[num][4] <= knightsInfo[num][5]:                               
            del knightsInfo[num]


l, n, q = map(int, input().split())
# 0은 빈칸, 1은 함정, 2는 벽
graph = [list(map(int, input().split())) for _ in range(l)]
# 기사별 정보 (r,c,h,w,k): 위치 (r,c), 세로 h, 가로 w, 체력 k
knightsInfo = dict()

for num in range(1, n+1):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    # 데미지 추가, 기사 정보 저장
    knightsInfo[num] = [r, c, h, w, k, 0]

# 북 동 남 서
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

for _ in range(q):
    i, d = map(int, input().split())

    if i not in knightsInfo:
        continue
    # 이동 가능한 기사들 번호 저장
    visited = set()
    # 기사 이동
    if move_knight(i, d):
        # 데미지 적용
        apply_damage(i, d)

answer = 0 
for survivor in knightsInfo:
    answer += knightsInfo[survivor][5]
print(answer)