def handle_employee():
    pass

def handle_host():
    pass

def handle_guest():
    pass

while True:
    user_type = str(
        input(
            "Welcome to the Airbnb application, are you a (G)uest, (H)ost, or (E)mployee? "
        )
    )
    if user_type == "E":
        handle_employee()
    else if user_type == "H":
        handle_host()
    else:
        handle_guest()



