import backend


def handle_employee():
    pass


def create_user():
    firstname = input("Enter first name: ")
    lastname = input("Enter last name: ")
    housenumber = int(input("Enter house number: "))
    street = input("Enter street: ")
    city = input("Enter city: ")
    province = input("Enter province: ")
    return backend.create_user(firstname, lastname, housenumber, street, city, province)


def handle_host():
    existing_user = int(input("(1) Login, (2) Register: "))
    user_id = -1

    if existing_user == 1:
        user_id = int(input("Enter your id "))
    else:
        user_id = create_user()
        print(user_id)

    while True:
        choice = int(input("(1) View listings, (2) Add listing: "))
        if choice == 1:
            listing_type = int(input("(1) Experience or (2) Property: "))


def handle_guest():
    pass


while True:
    user_type = input(
        "Welcome to the Airbnb application, are you a (G)uest, (H)ost, or (E)mployee? "
    )

    if user_type == "E":
        handle_employee()
    elif user_type == "H":
        handle_host()
    else:
        handle_guest()
