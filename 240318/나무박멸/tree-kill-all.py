n, m, k, c = map(int, input().split())
tree = [list(map(int, input().split())) for _ in range(n)]
# 제초제 뿌릴 나무 체크
remove = [[0]*n for _ in range(n)]
# 상하좌우
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]
# 대각선
dx = [-1, 1, 1, -1]
dy = [1, 1, -1, -1]

ans = 0

for year in range(m):
    # 번식
    increase = []
    for i in range(n):
        for j in range(n):
            if tree[i][j] > 0:
                # 성장
                cnt = 0
                # 번식
                empty = []  # 빈칸 인덱스
                blank = 0  # 각 인데스 인접 빈칸수
                for z in range(4):
                    ni = i + di[z]
                    nj = j + dj[z]
                    if 0 <= ni < n and 0 <= nj < n:
                        # 성장 수
                        if tree[ni][nj] > 0:
                            cnt += 1
                        # 번식
                        elif tree[ni][nj] == 0 and remove[ni][nj] >= 0:
                            empty.append((ni, nj))
                            blank += 1
                # 성장
                tree[i][j] += cnt
                # 번식
                if blank:
                    increase.append((tree[i][j] // blank, empty))
    # 번식
    for num, idx in increase:
        for x, y in idx:
            tree[x][y] += num

    # 제초제 뿌릴 위치 선정
    maxV = kx = ky = 0
    for x in range(n):
        for y in range(n):
            if tree[x][y] > 0:
                remove[x][y] = tree[x][y]
                for z in range(4):
                    for expand in range(1, k+1):
                        nx = x + dx[z] * expand
                        ny = y + dy[z] * expand
                        if 0 <= nx < n and 0 <= ny < n:
                            if tree[nx][ny] > 0:
                                remove[x][y] += tree[nx][ny]
                            else:
                                break

                if maxV < remove[x][y]:
                    maxV = remove[x][y]
                    kx = x
                    ky = y

            elif remove[x][y] < 0:
                remove[x][y] += 1
    # 제거
    ans += maxV
    tree[kx][ky] = 0
    remove[kx][ky] = -c
    for z in range(4):
        for expand in range(1, k+1):
            nx = kx + dx[z] * expand
            ny = ky + dy[z] * expand
            if 0 <= nx < n and 0 <= ny < n:
                # 제초제 영향
                remove[nx][ny] = -c
                if tree[nx][ny] > 0:
                    tree[nx][ny] = 0
                else:
                    break
print(ans)