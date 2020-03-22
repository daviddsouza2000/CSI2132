import pandas as pd
import random as rand

names_df = pd.read_csv("temp/names.csv")
branch_df = pd.read_csv("sample_branches.csv")

first_names = list(set(names_df["FirstName"]))
last_names = list(set(names_df["Surname"]))
branch_ids =  list(branch_df["BranchId"])
min_id = 1000
max_id = 999999
min_salary = 3000
max_salary = 8000
positions = ["software engineer", "customer representative", "accountant", "sales", "support"]
num_employees = 300
used_ids = set()

result_df = pd.DataFrame(columns=["EmployeeId", "BranchId", "FirstName", "LastName", "Position", "Salary"])

for i in range(num_employees):
    emp_id = rand.randint(min_id, max_id)
    while(emp_id in used_ids):
        emp_id = rand.randint(min_id, max_id)
    used_ids.add(emp_id)
    branch_id = rand.choice(branch_ids)
    fname = rand.choice(first_names)
    lname = rand.choice(last_names)
    pos = rand.choice(positions)
    salary = rand.randint(min_salary, max_salary)
    result_df = result_df.append({"EmployeeId": emp_id, "BranchId":branch_id, "FirstName": fname, "LastName": lname, "Position": pos, "Salary": salary }, ignore_index = True)

result_df.to_csv("sample_employees.csv")
    

