import pandas as pd
import random as rand

employee_df = pd.read_csv("sample_employees.csv")
branch_df = pd.read_csv("sample_branches.csv")
managers = employee_df.sample(n=len(branch_df))
new_branches_df = pd.DataFrame(columns = ["BranchId", "ManagerId", "Name"])
for i, line in branch_df.iterrows():
    new_branches_df = new_branches_df.append({"BranchId": line["BranchId"], "ManagerId": managers.iloc[i]["EmployeeId"], "Name": line["Name"]}, ignore_index=True)

new_branches_df.to_csv("sample_branches.csv")

    
