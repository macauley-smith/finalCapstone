# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password

#=====importing libraries===========
import os
from datetime import datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n---\n")
    task_data = [t for t in task_data if t != ""]

# read from tasks.txt, create a list and convert components to dictionary
task_list = []
for t_str in task_data:
    curr_t = {}
    
    # Split by line break and manually add each component
    task_components = t_str.split("\n")
    curr_t['username'] = task_components[0].split(":")[1].strip()
    curr_t['title'] = task_components[1].split(":")[1].strip()
    curr_t['description'] = task_components[2].split(":")[1].strip()
    curr_t['due_date'] = datetime.strptime(task_components[3].split(":")[1].strip(), DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4].split(":")[1].strip(), DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5].split(":")[1].strip() == "Yes" else False

    task_list.append(curr_t)

#==== Login Section ====
# This code reads usernames and password from the user.txt file to allow a user to login.
   
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("Username: admin\nPassword: password\n")

# Read in user_data and convert non-empty lines to a string, stored as user_data list
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    user_data = [u for u in user_data if u.startswith("Username: ") or u.startswith("Password: ")]

# Convert to a dictionary
username_password = {}
for i in range(0, len(user_data), 2):
    username = user_data[i].split("Username: ")[1].strip()
    password = user_data[i + 1].split("Password: ")[1].strip()
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#====== Functions ===========

# Writing content to tasks.txt in the correct format
def update_task_file(task_list):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                f"Username: {t['username']}\n",
                f"Title: {t['title']}\n",
                f"Description: {t['description']}\n",
                f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n",
                f"Assigned Date: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n",
                f"Completed: {'Yes' if t['completed'] else 'No'}\n",
                "---\n"  # Separator between tasks
            ]
            task_list_to_write.append("".join(str_attrs))
        task_file.write("".join(task_list_to_write))

# Registering a user
def reg_user():
    new_username = input("New Username (enter 'q' to return to the main menu): ")
    # allows user to exit to main menu if they no longer wish to enter a user
    if new_username.strip().lower() == 'q':
        return True
    
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # checks for existing user and adds the user if no existing user was found in username_password dict
    if new_username in username_password:
        print("Error, user already exists. Try again.")
        return False
    elif new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as user_file:
            user_data = []
            for k in username_password:
                user_data.append(f"Username: {k}\nPassword: {username_password[k]}\n")
            user_file.write("\n".join(user_data))
            return True
    else:
        print("Passwords do not match")
        return False

# Adding a task
def add_task():
    print("Enter task information:")
    username = input("Username: ")
    title = input("Task title: ")
    description = input("Task description: ")
    due_date_str = input("Task due date (YYYY-MM-DD): ")
    due_date = datetime.strptime(due_date_str, DATETIME_STRING_FORMAT)

    task = {
        "username": username,
        "title": title,
        "description": description,
        "due_date": due_date,
        "assigned_date": datetime.now(),
        "completed": False,
    }

    task_list.append(task)
    update_task_file(task_list)
    print("Task added.")

# Viewing all tasks
def view_all():
    task_count = 0
    for t in task_list:
        task_count +=1
        disp_str = f"Task {task_count}: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
        print(disp_str)

# Viewing all tasks assigned to the user
def view_mine():
    user_tasks = [t for t in task_list if t['username'] == curr_user]
    task_count = 0
    for t in user_tasks:
        if t['username'] == curr_user:
            task_count += 1
            disp_str = f"Task {task_count}: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)
    return user_tasks

# Function for changing the completion status of tasks
def update_task_completion_status():
    user_tasks = view_mine()
    task_num = int(input("Enter the task number and press enter to change its completion status or -1 to go back: "))
    if task_num == -1:
        return
    elif 0 < task_num <= len(user_tasks):
        task_index = task_num - 1
        task_list[task_index]['completed'] = not task_list[task_index]['completed']
        print(f"Task '{task_list[task_index]['title']}' completion status updated.")
        
        update_task_file(task_list)
    
    else:
        print("Invalid task number.")

# Editing tasks
def edit_task():
    user_tasks = view_mine()
    task_num = int(input("Enter the task number to edit or 0 to go back: "))
    # input validation to check the task exists
    if task_num == 0:
        return
    elif 0 < task_num <= len(user_tasks):
        task_index = task_list.index(user_tasks[task_num-1])
        if task_list[task_index]['completed']:
            print("This task is already completed and cannot be edited.")
            return
        
        edit_option = input("Enter 'user' to edit the username or 'dd' to edit the due date: ").strip().lower()
        if edit_option == 'user':
            new_username = input("Enter the new username: ")
            # input validation to check that the task is being assigned to an existing user
            if new_username not in username_password.keys():
                print("User does not exist. Please enter a valid username.")
            else:
                task_list[task_index]['username'] = new_username
                print(f"Task '{task_list[task_index]['title']}' assigned to user '{new_username}'.")
        elif edit_option == 'dd':
            while True:
                try:
                    new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT).date()
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified.")
            task_list[task_index]['due_date'] = due_date_time
            print(f"Task '{task_list[task_index]['title']}' due date updated to '{due_date_time.strftime(DATETIME_STRING_FORMAT)}'.")
        else:
            print("Invalid option. Returning to main menu.")
        
        update_task_file(task_list)

    else:
        print("Invalid task number.")

# Generating reports
def generate_reports():
    # task_overview - calculations stored as variables
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < datetime.now().date())
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

     # creates a file called task_overview and displays the data there
    with open("task_overview.txt", "w") as task_overview:
        task_overview.write(f"Total tasks: {total_tasks}\n")
        task_overview.write(f"Completed tasks: {completed_tasks}\n")
        task_overview.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
        task_overview.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

    # user overview
    total_users = len(username_password)
    user_task_counts = {}
    for t in task_list:
        if t['username'] in user_task_counts:
            user_task_counts[t['username']] += 1
        else:
            user_task_counts[t['username']] = 1

    with open("user_overview.txt", "w") as user_overview:
        user_overview.write(f"Total users: {total_users}\n")
        user_overview.write(f"Total tasks: {total_tasks}\n\n")
        for user in user_task_counts:
            task_count = user_task_counts[user]
            task_percentage = (task_count / total_tasks) * 100
            user_tasks = [t for t in task_list if t['username'] == user]
            completed_tasks = sum(1 for t in user_tasks if t['completed'])
            overdue_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'].date() < datetime.now().date())

            completed_percentage = (completed_tasks / task_count) * 100
            uncompleted_percentage = 100 - completed_percentage
            overdue_percentage = (overdue_tasks / task_count) * 100

            user_overview.write(f"{user}:\n")
            user_overview.write(f"  Total tasks assigned: {task_count}\n")
            user_overview.write(f"  Percentage of total tasks: {task_percentage:.2f}%\n")
            user_overview.write(f"  Percentage of completed tasks: {completed_percentage:.2f}%\n")
            user_overview.write(f"  Percentage of uncompleted tasks: {uncompleted_percentage:.2f}%\n")
            user_overview.write(f"  Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

# display statistics from user.txt and tasks.txt
def display_statistics():
    num_tasks = len(task_list)
    num_users = len(user_data)

    print("Number of tasks: " + str(num_tasks))
    print("Number of users: " + str(num_users))


#====== Main Loop ==========
while True:
    # Displays the menu options for the user to select from
    menu = input('''Select one of the following options below:

r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit

Select from the menu and then press enter: ''').lower().strip()

    # Register a user
    if menu == 'r':
        while True:
            user_added = reg_user()
            if user_added == True:
                break
    # Add a task
    elif menu == 'a':
        add_task()
    # View all tasks
    elif menu == 'va':
        view_all()
    # View tasks (user specific) and mark as complete and/or edit the task       
    elif menu == 'vm':
        while True:
            view_mine()
            menu_option = input("Enter 'et' to edit tasks, or 'cs' to change completion status, 'exit' to return to main menu: ")
            if menu_option == 'et'.strip().lower():
                edit_task()
            elif menu_option == 'cs'.strip().lower():
                update_task_completion_status()
            elif menu_option == 'exit'.strip().lower():
                break
            else:
                print("Invalid input. Please select from the menu options.")
    # Generate reports
    elif menu == 'gr':
        generate_reports()
        print("Reports have been generated successfully.")
        
        # Display statistics, only if the user is admin
    elif menu == 'ds' and curr_user == 'admin': 
        display_statistics()    

    # exit the application
    elif menu == 'e':
        print('The application will now close.')
        exit()
    else:
        print("Invalid input. Please only select from the listed menu options.")