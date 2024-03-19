from copy import deepcopy

# 1.나무 성장
def tree_growth():
    # 나무 위치 찾기
    for i in range(n):
        for j in range(n):
            # 나무가 있으면 인접한 네 개의 칸 탐색
            if graph[i][j] > 0:
                # 인접한 칸 중 나무가 있으면 현재 나무 +1 
                for x in range(4):
                    ni = i + di[x]
                    nj = j + dj[x]
                    if 0 <= ni < n and 0 <= nj < n and graph[ni][nj] > 0:
                        graph[i][j] += 1

# 2.나무 번식
def tree_propagation():
    global graph
    copy_graph = deepcopy(graph)

    # 나무 위치 찾기
    for i in range(n):
        for j in range(n):
            # 나무가 있으면 인접한 네 개의 칸 탐색
            if graph[i][j] > 0:
                # 번식 가능한 위치 
                propagation = []
                cnt = 0
                # 인접한 칸 중 탐색
                for x in range(4):
                    ni = i + di[x]
                    nj = j + dj[x]
                    # 벽, 다른 나무, 제초제 모두 없는 칸이며 번식 진행
                    if 0 <= ni < n and 0 <= nj < n and graph[ni][nj] == 0 and herbicide[ni][nj] == 0:
                        propagation.append((ni, nj))
                        cnt += 1
                # 나무 그루 수 // 총 번식이 가능한 칸의 개수 = 번식 그루 수
                for ni, nj in propagation:
                    copy_graph[ni][nj] += graph[i][j]//cnt
    graph = copy_graph

# 3.제초제 뿌리기
def spray_herbicide():
    global answer, graph, herbicide
    # 제초제 뿌릴 위치 찾기
    # 박멸되는 나무 수 
    maxV = 0
    # 나무가 박멸되는 위치
    exterminated_tree = []
    # 나무 위치 찾기
    for i in range(n):
        for j in range(n):
            # 나무가 있으면 대각선 나무 탐색
            if graph[i][j] > 0:
                currV = graph[i][j]
                curr_affected = [(i, j)]
                # 대각선 방향
                for x in range(4):
                    # k번 만큼 이어짐
                    for y in range(1, k+1):
                        ni = i + dih[x]*y
                        nj = j + djh[x]*y
                        if 0 <= ni < n and 0 <= nj < n:
                            # 나무면 제초제 이어서 뿌림
                            if graph[ni][nj] > 0:
                                currV += graph[ni][nj]
                                # 제초제 뿌리기
                                curr_affected.append((ni, nj))
                            elif graph[ni][nj] == 0:
                                # 빈칸이면 제초제 뿌리고 멈춤
                                # 제초제 뿌리기
                                curr_affected.append((ni, nj))
                                break
                            else:
                                # 벽이면 멈춤
                                break
                        else:
                            # 다른 방향 탐색
                            break
                # 박멸되는 나무 수가 저장된 수보다 크면 제초제의 영향받는 위치/나무 수 갱신
                if maxV < currV:
                    maxV = currV
                    exterminated_tree = curr_affected
    # 박멸한 나무 수 저장
    answer += maxV
    # 제초제 뿌리기
    for i, j in exterminated_tree:
        # 나무가 있으면 박멸
        graph[i][j] = 0
        # 제초제 뿌리기
        herbicide[i][j] = c

def reduce_herbicide():
    global herbicide
    # 제초제 위치 찾기
    for i in range(n):
        for j in range(n):
            # 제초제가 뿌려져 있으면 줄이기
            if herbicide[i][j] > 0:
                herbicide[i][j] -= 1


# 격자의 크기 n, 박멸이 진행되는 년 수 m, 제초제의 확산 범위 k, 제초제가 남아있는 년 수 c
n, m, k, c = map(int, input().split())
# 나무의 그루 수, 벽의 정보 (벽은 -1)
graph =[list(map(int, input().split())) for _ in range(n)]
# 동 남 서 북 / 대각선
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]
dih = [-1, 1, 1, -1]
djh = [1, 1, -1, -1]
# 제초제 유지 기간 저장
herbicide = [[0]*n for _ in range(n)]
# m년 동안 총 박멸한 나무 수
answer = 0
# m년 동안 수행
for _ in range(m):
    # 1.나무 성장
    tree_growth()
    # 2.나무 번식
    tree_propagation()
    # 3.제초제 줄이기
    reduce_herbicide()
    # 4.제초제 뿌리기
    spray_herbicide()

print(answer)