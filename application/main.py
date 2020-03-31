import backend
from enums import *
from prettytable import PrettyTable


def create_user():
    firstname = input("Enter first name: ")
    lastname = input("Enter last name: ")
    housenumber = int(input("Enter house number: "))
    street = input("Enter street: ")
    city = input("Enter city: ")
    province = input("Enter province: ")
    return backend.create_user(firstname, lastname, housenumber, street, city, province)


def handle_employee():
    pass


def handle_host():
    existing_user = int(input("(1) Login, (2) Register: "))
    user_id = -1

    if existing_user == 1:
        user_id = int(input("Enter your id "))
    else:
        user_id = create_user()
        print(
            "Your user id is {0}. Do not forget this value if you wish to return.".format(
                user_id
            )
        )

    while True:
        choice = int(input("(1) View listings, (2) Add listing: "))
        if choice == 1:
            listing_type = ListingType(int(input("(1) Experience or (2) Property: ")))


def handle_guest():
    pass


# TODO: consider instead of branch_id actualy getting the branch name as that makes more sense to users
def display_listings(listing_type, host_id):
    headers = []
    if listing_type == ListingType.Property:
        headers = [
            "PropertyId",
            "HostId",
            "BranchId",
            "Title",
            "Description",
            "NumGuests",
            "NumBedrooms",
            "NumBeds",
            "NumBaths",
            "Price",
        ]
    else:
        headers = [
            "ExperienceId",
            "HostId",
            "BranchId",
            "Title",
            "Description",
            "Duration",
            "GroupSize",
            "Price",
        ]

    t = PrettyTable(headers)

    rows = backend.host_select_listings(listing_type, host_id)

    for row in rows:
        row = list(row)
        # This is to truncate the description
        row[4] = row[4][:50] + "..."
        t.add_row(row)
    print(t)


while True:
    user_type = input(
        "Welcome to the Airbnb application, are you a (G)uest, (H)ost, or (E)mployee? "
    )
    display_listings(ListingType.Property, 851012)

    if user_type == "E":
        handle_employee()
    elif user_type == "H":
        handle_host()
    else:
        handle_guest()
