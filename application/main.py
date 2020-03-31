import backend
from enums import *
from prettytable import PrettyTable

integer_types = set(["groupsize", "numguests", "numbedrooms", "numbaths", "numbeds"])
float_types = set(["price"])
time_types = set(["duration"])

valid_attributes = {
    "Property": set(
        [
            "title",
            "description",
            "numguests",
            "numbedrooms",
            "numbeds",
            "numbaths",
            "price",
        ]
    ),
    "Experience": set(["title", "description", "duration", "groupsize", "price"]),
}


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
        user_id = int(input("Enter your id: "))
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
            listing_type = ListingType(int(input("(1) Property or (2) Experience: ")))
            listings = display_listings(listing_type, user_id)
            view_listing = (
                input("Would you like to view a specific listing? (y/n) ") == "y"
            )
            if view_listing:
                index = int(input("Enter the index of the listing you wish to view: "))
                listing = listings[index - 1]
                display_listing(listing, listing_type)
                action = int(
                    input(
                        "Actions: (0) Go back | (1) Edit attribute | (2) Delete listing | (3) View bookings: "
                    )
                )
                if action == 1:
                    edit_listing_attribute(listing, listing_type)


def handle_guest():
    pass


def edit_listing_attribute(listing, listing_type):
    while True:
        attrib = input("Enter the attribute you would like to edit: ").lower()
        if attrib not in valid_attributes[listing_type.name]:
            print("Error: invalid attribute")
            continue
        value = input("Enter the updated value ")
        if attrib in integer_types:
            if not isinstance(value, int):
                print("Error: value must be an integer")
                continue
            value = int(value)
        elif attrib in float_types:
            if not isinstance(value, float):
                print("Error: value must be a float")
                continue
            value = float(value)

        backend.update_listing(listing_type, listing, attrib, value)
        yes = input("Would you like to update another value? (y/n)") == "y"
        if not yes:
            break


# TODO: consider instead of branch_id actualy getting the branch name as that makes more sense to users
def display_listings(listing_type, host_id):
    headers = []
    if listing_type == ListingType.Property:
        headers = [
            "Index",
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
            "Index",
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
    index = 1
    for row in rows:
        row = list(row)
        # This is to truncate the description
        row[4] = row[4][:50] + "..."
        t.add_row([index] + row)
        index += 1
    print(t)
    return rows


def display_listing(listing, listing_type):
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
    for i in range(len(headers)):
        print("{0}: {1}".format(headers[i], listing[i]))


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
