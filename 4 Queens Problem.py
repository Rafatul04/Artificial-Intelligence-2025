
N = 4

def print_solution(assignment):
    """Pretty print the board from assignment."""
    for r in range(N):
        row = ["Q" if assignment[r] == c else "." for c in range(N)]
        print(" ".join(row))
    print()

def is_consistent(assignment, row, col):
    """Check if placing queen at (row, col) satisfies constraints."""
    for r in range(row):
        c = assignment[r]
        # Same column
        if c == col:
            return False
        # Same diagonal
        if abs(c - col) == abs(r - row):
            return False
    return True

def csp_backtrack(assignment, row, solutions):
    """Recursive backtracking with forward checking."""
    if row == N:
        # Found one complete solution
        solutions.append(assignment[:])
        print_solution(assignment)
        return

    for col in range(N):
        if is_consistent(assignment, row, col):
            assignment[row] = col
            csp_backtrack(assignment, row + 1, solutions)
            assignment[row] = -1  # backtrack

def solve_n_queens():
    assignment = [-1] * N  # -1 = unassigned
    solutions = []
    csp_backtrack(assignment, 0, solutions)
    print("Total solutions found:", len(solutions))

if __name__ == "__main__":
    solve_n_queens()
