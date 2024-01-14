# 1. 주사위 동, 남, 서, 북으로 굴리기 (바뀐 숫자 위치 반환)
def changeDiceBottom(dice, d):
    # 동
    if d == 0:
        nextDice = {'top': dice['left'], 'bottom': dice['right'], 'left': dice['bottom'], 'right': dice['top'], 'front':dice['front'], 'back': dice['back']}
    # 남
    elif d == 1:
        nextDice = {'top': dice['back'], 'bottom': dice['front'], 'left': dice['left'], 'right': dice['right'], 'front':dice['top'], 'back': dice['bottom']}
    # 서
    elif d == 2:
        nextDice = {'top': dice['right'], 'bottom': dice['left'], 'left': dice['top'], 'right': dice['bottom'], 'front':dice['front'], 'back': dice['back']}
    # 북 d == 3 
    else:
        nextDice = {'top': dice['front'], 'bottom': dice['back'], 'left': dice['left'], 'right': dice['right'], 'front':dice['bottom'], 'back': dice['top']}
    return nextDice

# 2.주사위 바닥과 인접한 같은 숫자 합 구하기
def bfs(i, j):
    visited = [[0]*n for _ in range(n)]
    # 바닥 숫자로 방문 체크
    visited[i][j] = board[i][j]
    stack = [(i, j)]
    score = board[i][j]
    while stack:
        i, j = stack.pop()

        for k in range(4):
            ni = i + di[k]
            nj = j + dj[k]
            if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj] and board[ni][nj] == visited[i][j]:
                score += board[ni][nj]
                visited[ni][nj] = visited[i][j]
                stack.append((ni, nj))
    return score

# 3. 주사위 m번 굴리기 (+진행 방향 변경)
def rollDice(dice, d, i, j):
    totalScore = 0
    for _ in range(m):
        ni = i + di[d]
        nj = j + dj[d]
        # 격자를 벗어나면
        if not (0 <= ni < n and 0 <= nj < n):
            # 반대 방향으로 이동
            d = (d+2)%4
            ni = i + di[d]
            nj = j + dj[d]
        # 주사위 이동
        i = ni
        j = nj
        # 인접한 같은 숫자 합
        totalScore += bfs(i, j)
        # 주사위 굴리기
        dice = changeDiceBottom(dice, d)
        if dice['bottom'] > board[i][j]:
            # 90' 시계방향으로 회전
            d = (d+1)%4
        elif dice['bottom'] < board[i][j]:
            # 90' 반시계방향으로 회전
            d = (d-1)%4
    return totalScore


n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
# 처음 주사위 위치 딕셔너리로 저장
firstDice = {'top': 1, 'bottom': 6, 'left': 4, 'right': 3, 'front':2, 'back': 5}
# 동 남 서 북 이동
di = [0, 1, 0, -1]
dj = [1, 0, -1, 0]
print(rollDice(firstDice, 0, 0, 0))