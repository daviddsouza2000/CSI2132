import backend
from enums import *
from prettytable import PrettyTable

branch_names = backend.get_branches()

integer_types = set(
    [
        "groupsize",
        "numguests",
        "numbedrooms",
        "numbaths",
        "numbeds",
        "Number of Guests",
        "Number of Bedrooms",
        "Number of Beds",
        "Number of Baths",
        "Group Size",
        "hours",
        "minutes",
        "seconds",
    ]
)
float_types = set(["price", "Price"])
time_types = set(["duration", "Duration"])
time_unit_types = set(["hours", "minutes", "seconds"])
date_types = set()
const_types = {"Branch Name": branch_names}

# TODO: add branchid later
property_attributes = [
    "Branch Name",
    "Title",
    "Description",
    "Number of Guests",
    "Number of Bedrooms",
    "Number of Beds",
    "Number of Baths",
    "Price",
]

experience_attributes = [
    "Branch Name",
    "Title",
    "Description",
    "Duration",
    "Group Size",
    "Price",
]

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
                elif action == 2:
                    delete_listing(listing, listing_type)
        else:
            listing_type = ListingType(int(input("(1) Property or (2) Experience: ")))
            create_listing(user_id, listing_type)


def handle_guest():
    pass


def edit_listing_attribute(listing, listing_type):
    while True:
        attrib = input("Enter the attribute you would like to edit: ").lower()
        if attrib not in valid_attributes[listing_type.name]:
            print("Error: invalid attribute")
            continue
        value = input_attribute(attrib)

        backend.update_listing(listing_type, listing, attrib, value)
        yes = input("Would you like to update another value? (y/n) ") == "y"
        if not yes:
            break


def create_listing(host_id, listing_type):
    inputs = []
    if listing_type == ListingType.Property:
        for attrib in property_attributes:
            inputs.append(input_attribute(attrib))
        inputs = [host_id] + inputs
        backend.insert_listing(listing_type, inputs)
    else:
        for attrib in experience_attributes:
            inputs.append(input_attribute(attrib))
        inputs = [host_id] + inputs
        backend.insert_listing(listing_type, inputs)


def delete_listing(listing, listing_type):
    backend.delete_listing(listing, listing_type)
    print("Successfully deleted listing")


def input_attribute(attribute_name):
    while True:
        if attribute_name in integer_types:
            value = input("Enter value for {0}: ".format(attribute_name))
            if not is_type(value, int):
                print("Error: value must be an integer")
                continue
            value = int(value)
            if value < 0:
                print("Error: value must be nonnegative")
                continue
            if attribute_name in time_unit_types:
                if attribute_name == "hours":
                    if value > 24:
                        print("Error: hours must be less than or equal to 24 hours")
                        continue
                if attribute_name == "minutes":
                    if value > 59:
                        print("Error: minutes must be between range [0, 59]")
                        continue
        elif attribute_name in float_types:
            value = input("Enter value for {0}: ".format(attribute_name))
            if not is_type(value, float):
                print("Error: value must be a float")
                continue
            value = float(value)
            if value < 0:
                print("Error: value must be nonnegative")
                continue
        elif attribute_name in time_types:
            print("Enter values for {0}: ".format(attribute_name))
            hours = input_attribute("hours")
            if hours != 24:
                minutes = input_attribute("minutes")
            else:
                minutes = 0
            value = format_time(hours, minutes)
        elif attribute_name in const_types:
            valid_values = const_types[attribute_name]
            value = input(
                "Enter value for {0} (valid values: {1}): ".format(
                    attribute_name, ",".join(valid_values)
                )
            )
            if value not in valid_values:
                print("Error: invalid value")
                continue
        else:
            value = input("Enter value for {0}: ".format(attribute_name))

        return value


def is_type(x, t):
    try:
        t(x)
        return True
    except:
        return False


def format_time(hours, minutes):
    duration_template = "{0}:{1}:00"
    if hours < 10:
        hours = "0" + str(hours)
    if minutes < 10:
        minutes = "0" + str(minutes)
    return duration_template.format(hours, minutes)


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
        # This is to truncate the description, otherwise the table looks gross
        if len(row[4]) > 50:
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
