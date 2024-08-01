# 각 학생별로 좋아하는 학생이 정확히 4명씩 정해져 있다.
# 자기 자신을 좋아하는 학생은 없고,
# 학생의 번호가 중복하여 주어지는 경우도 없다.
# 입력으로 주어진 순서대로 다음 조건에 따라 가장 우선순위가 높은 칸으로 탑승
# 1.격자를 벗어나지 않는 4방향으로 인접한 칸 중 앉아있는 좋아하는 친구의 수가 가장 많은 위치로
# 2. 1번 조건 여러 곳이라면, 인접한 칸 중 비어있는 칸의 수가 가장 많은 위치로
# 3. 2번 조건 여러 곳이라면, 행 번호가 가장 작은 위치로
# 4. 3번 조건 여러 곳이라면, 열 번호가 가장 작은 위치로
# 첫번째 학생은 1번 경우 패스!

# 좋아하는 학생이 주변에 있는지 탐색 -> 개수 반환
def favorite_cnt(row, col, favoriteP):
    cnt = 0
    for k in range(4):
        nx = row + di[k]
        ny = col + dj[k]
        if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] in favoriteP:
            cnt += 1
    return cnt

# 빈칸 개수 찾기
def find_blank(row, col):
    cnt = 0
    for k in range(4):
        nx = row + di[k]
        ny = col + dj[k]
        if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == 0:
            cnt += 1
    return cnt

def not_favorite():
    maxBlankCnt = 0
    newPosi = (-1, -1)
    for i in range(n):
        for j in range(n):
            if visited[i][j] == 0:
                blankCnt = find_blank(i, j)
                if maxBlankCnt < blankCnt:
                    maxBlankCnt = blankCnt
                    newPosi = (i, j)

                    if blankCnt == 4:
                        return newPosi
    return newPosi


n = int(input())
peopleNum = n*n
board = [list(map(int, input().split())) for _ in range(peopleNum)]
# 방문한 사람 저장
visited = [[0]*n for _ in range(n)]
people = dict()

di = [-1, 0, 0, 1]
dj = [0, -1, 1, 0]

for i in range(peopleNum):
    student, *like = board[i]
    # 첫번째 순서는 조건에 따라 위치가 (1,1) 고정
    if i == 0:
        visited[1][1] = student
        people[student] = (1, 1)
    else:
        # 좋아하는 사람 있는 지 체크 (번호)
        likes = set(like)
        favorite = set()
        favorite = likes & set(people)
        # 좋아하는 사람 있으면 위치, 최대 수 저장
        maxCnt = 0
        posi = (-1, -1)
        if favorite:
            if len(favorite) == 1:
                x, y = people[list(favorite)[0]]
                # 좋아하는 사람 위치에서 빈칸 탐색
                for k in range(4):
                    nx = x + di[k]
                    ny = y + dj[k]
                    if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == 0:
                        # 학생 위치 저장
                        posi = (nx,ny)
                        break
                    
            else:
                # 좋아하는 사람 여러명 존재하면
                # 빈칸있는지
                # 다른 좋아하는 사람 있는지 체크
                check = set()
                for num in favorite:
                    x, y = people[num]
                    # 좋아하는 사람 위치에서 빈칸 탐색
                    for k in range(4):
                        nx = x + di[k]
                        ny = y + dj[k]
                        if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == 0 and (nx, ny) not in check:
                            check.add((nx, ny))
                            # 빈칸에서 4방향 탐색
                            newCnt = favorite_cnt(nx, ny, likes)
                            if maxCnt < newCnt:
                                maxCnt = newCnt
                                posi = (nx,ny)

        if not favorite or posi == (-1, -1):
            # 좋아하는 사람 없으면
            # 조건 2, 4, 3
            posi = not_favorite()
        
        # 학생 위치 저장
        visited[posi[0]][posi[1]] = student
        people[student] = posi

score = [0, 1, 10, 100, 1000]
result = 0
for i in range(peopleNum):
    student, *like = board[i]
    x, y = people[student]
    result += score[favorite_cnt(x, y, set(like))]
print(result)