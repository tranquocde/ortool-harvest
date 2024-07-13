from ortools.sat.python import cp_model
import sys
import random
import time
def gen_data(N):
    field_products = [random.randint(1,10) for i in range(N)]
    start_days = [random.randint(1,10) for i in range(N)]
    end_days = [random.randint(start_days[i]+1,20) for i in range(N)]
    return field_products , start_days,end_days


def Solver(N):
    # Data
    max_capacity = 24 #M
    min_capacity = 1 #m
    num_fields = N #N
    fields_products , start_days,end_days = gen_data(N=num_fields)
    # print(fields_products)
    # print(start_days)
    # print(end_days)
    print(f"Total products : {sum(fields_products)}")
    assert(len(fields_products) == num_fields)

    #Model
    model = cp_model.CpModel()


    #Main variables
    start = min(start_days)
    end = max(end_days)
    all_day_available=range(start,end + 1)
    all_fields = range(num_fields)

    x = {}
    for field in all_fields:
        for day in all_day_available:
            x[(day,field)] = model.NewIntVar(0,1,f"x_{day}_{field}") 
            #1 nếu thu hoạch field 
            #vào ngày đó còn không thu hoạch thì là 0
    #loads variable
    loads = [model.NewIntVar(min_capacity , max_capacity,f"{i}") for i in all_day_available]

    #link loads and x ,  add constraints
    for day in all_day_available:
        model.Add(loads[day-start]==sum(x[(day,field)] * fields_products[field]
                                        for field in all_fields))
    for field in all_fields:
        model.Add(1 >= sum(x[(day,field)] for day in all_day_available))
        for day in all_day_available:
            if day < start_days[field] or day > end_days[field]:
                model.Add(0 == x[(day,field)])
    #Maximize sum of loads
    model.Maximize(sum(loads))
    #Solves and prints out the solution
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(f"Solve status: {solver.StatusName(status)}")
    if status == cp_model.OPTIMAL:
        print(f"Total harvest products : {solver.ObjectiveValue()}")
        available = 0
        for field in all_fields:
            flag = True
            for day in all_day_available:
                temp = solver.Value(x[(day,field)])
                if temp == 1:
                    available += 1
                    print(f"{field+1} {day}")
                    flag = False
            # if flag:
                # print(f"{field+1} -1") 
        print(f"Days of harvesting : {available}")
start = time.time()
N = int(sys.argv[1])
Solver(N)
end = time.time()
run_time = round(end - start , 5)
print(f"Running time: {run_time} s")
