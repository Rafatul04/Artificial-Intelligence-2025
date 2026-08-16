
courses = ["CS101", "CS102", "CS103", "CS104", "CS105"]
times = ["Mon 9am", "Mon 11am", "Tue 9am", "Tue 11am", "Wed 9am"]
rooms = ["RoomA", "RoomB", "RoomC"]
professors = ["ProfA", "ProfB", "ProfC"]

availability = {
    "ProfA": [t for t in times if t != "Mon 9am"],
    "ProfB": [t for t in times if t != "Tue 9am"],
    "ProfC": [t for t in times if t != "Wed 9am"]
}

domains = {}
for course in courses:
    domains[course] = []
    for t in times:
        for r in rooms:
            for p in professors:
                if t not in availability[p]:
                    continue
                if course == "CS105" and r != "RoomC":
                    continue
                if course == "CS101" and p != "ProfA":
                    continue
                if course == "CS103" and p != "ProfB":
                    continue
                domains[course].append((t, r, p))


def is_valid(assignment, course, value):
    t, r, p = value

    
    for c, (t2, r2, p2) in assignment.items():
        if t == t2 and r == r2:
            return False  

    
    for c, (t2, r2, p2) in assignment.items():
        if t == t2 and p == p2:
            return False  

    return True


def backtrack(assignment):
    if len(assignment) == len(courses):
        return [assignment.copy()]

    solutions = []
    print
    unassigned = [c for c in courses if c not in assignment][0]

    for value in domains[unassigned]:
        if is_valid(assignment, unassigned, value):
            assignment[unassigned] = value
            solutions.extend(backtrack(assignment))
            del assignment[unassigned]  
    return solutions


solutions = backtrack({})

if solutions:
    print(f"Total valid schedules found: {len(solutions)}\n")
    sol = solutions[1400]
    print("Course | Time      | Room   | Professor")
    print("----------------------------------------")
    for c in courses:
        t, r, p = sol[c]
        print(f"{c:6} | {t:9} | {r:6} | {p}")
else:
    print("No valid schedule found.")
