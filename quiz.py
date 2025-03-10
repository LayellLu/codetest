def reverse_list(l: list) -> list:
    reversed_list = []
    for i in range(len(l) - 1, -1, -1):
        reversed_list.append(l[i])
    return reversed_list


def solve_sudoku(matrix: list) -> list:
    # 查找一个空白位置，返回(row, col)，如果没有空位则返回None
    def find_empty():
        for r in range(9):
            for c in range(9):
                if matrix[r][c] == 0:
                    return r, c
        return None

    # 判断在位置(r, c)放入num是否符合数独规则
    def is_valid(r: int, c: int, num: int) -> bool:
        # 检查所在行和列是否存在相同的数字
        for k in range(9):
            if matrix[r][k] == num or matrix[k][c] == num:
                return False
        # 检查所在3x3小宫格是否存在相同的数字
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if matrix[i][j] == num:
                    return False
        return True

    # 查找下一个空白格
    empty_cell = find_empty()
    if not empty_cell:
        return matrix
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(row, col, num):
            matrix[row][col] = num
            # 成功则直接返回解出的棋盘
            solved = solve_sudoku(matrix)
            if solved:
                return solved
            # 不成功则回溯，恢复为空白
            matrix[row][col] = 0

    return None
