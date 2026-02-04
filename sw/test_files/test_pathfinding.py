from sw.course_graph import course, start_point, pickup_1

START = 35
END = 20

print(f"{START} --> ", end='')
for p in course.shortest_path(START, END):
    print(f"{p}", end='')
    if p != END:
        print(" --> ", end='')
    else:
        print("")