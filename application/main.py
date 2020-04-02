import backend
from enums import *
from prettytable import PrettyTable
from datetime import datetime, timedelta


def setup_index_types():
    amenities = backend.get_amenities()
    inclusions = backend.get_inclusions()
    languages = backend.get_languages()
    create_list = lambda x: [t[0] for t in x]

    index_types["Amenities"] = create_list(amenities)
    index_types["Inclusions"] = create_list(inclusions)
    index_types["Languages"] = create_list(languages)


branch_names = backend.get_branches()

integer_types = set(
    [
        "Employee Id",
        "id",
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
        "day",
        "month",
        "year",
        "amenity",
        "inclusion",
        "language",
        "value",
        "House Number",
    ]
)

float_types = set(["price", "Price"])
time_types = set(["duration", "Duration", "time"])
time_unit_types = set(["hours", "minutes", "seconds"])
datetime_types = set(["startdate", "enddate"])
const_types = {"Branch Name": branch_names, "Payment Type": ["cash", "credit", "debit"]}
index_types = {"Amenities": [], "Inclusions": [], "Languages": []}

setup_index_types()

property_attributes = [
    "Branch Name",
    "Title",
    "Description",
    "Number of Guests",
    "Number of Bedrooms",
    "Number of Beds",
    "Number of Baths",
    "Price",
    "Amenities",
]

experience_attributes = [
    "Branch Name",
    "Title",
    "Description",
    "Duration",
    "Group Size",
    "Price",
    "Inclusions",
    "Languages",
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
    valid_provinces = set(
        ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU",]
    )
    firstname = input("Enter first name: ")
    lastname = input("Enter last name: ")
    housenumber = input_attribute("House Number")
    street = input("Enter street: ")
    city = input("Enter city: ")
    province = input("Enter province ({0}): ".format(",".join(valid_provinces)))
    while province not in valid_provinces:
        province = input("Enter province({0}): ".format(",".join(valid_provinces)))
    return backend.create_user(firstname, lastname, housenumber, street, city, province)


def get_int_input(message, max_val, includes_zero=False):
    while True:
        try:
            inp = int(input(message))
            if inp <= max_val and (inp > 0 or (inp == 0 and includes_zero)):
                return inp
            else:
                print("Error: did not select a valid choice")
        except:
            print("Error: must be an integer")


def get_user_id():
    existing_user = get_int_input("(1) Login, (2) Register: ", 2)
    user_id = -1

    if existing_user == 1:
        while True:
            user_id = input_attribute("id")
            if backend.is_valid_user_id(user_id):
                return user_id
            else:
                print("Error: Entered Id does not exist")
    else:
        user_id = create_user()
        print(
            "Your user id is {0}. Do not forget this value if you wish to return.".format(
                user_id
            )
        )
    return user_id


def get_employee_id():
    while True:
        emp_id = input_attribute("Employee Id")
        if backend.is_valid_employee_id(emp_id):
            return emp_id
        else:
            print("Error: Entered Id does not exist")


def get_listing_type_input():
    val = get_int_input("(1) Property or (2) Experience: ", 2)
    return ListingType(val)


def yes_or_no_input(message):
    while True:
        inp = input(message)
        if inp.lower() not in ["y", "n"]:
            print("Error: must enter 'y' or 'n')")
        else:
            return inp.lower() == "y"


def handle_employee():
    emp_id = get_employee_id()
    while True:
        choice = get_int_input(
            "(1) View all listings | (2) View listing given branch | (3) View all users | (4) View all hosts | (5) View all superhosts: ",
            5,
        )

        if choice == 1:
            listing_type = get_listing_type_input()
            listings = display_employee_listings(listing_type, None)
        elif choice == 2:
            branch = input_attribute("Branch Name")
            listing_type = get_listing_type_input()
            listings = display_employee_listings(listing_type, branch)
        elif choice == 3:
            display_users()
        elif choice == 4:
            display_hosts(False)
        elif choice == 5:
            display_hosts(True)


def handle_host():
    user_id = get_user_id()
    while True:
        choice = get_int_input("(1) View listings | (2) Add listing: ", 2)
        if choice == 1:
            listing_type = get_listing_type_input()
            listings = display_listings(listing_type, user_id)
            view_listing = yes_or_no_input(
                "Would you like to view a specific listing? (y/n) "
            )
            if view_listing:
                index = get_int_input(
                    "Enter the index of the listing you wish to view: ", len(listings)
                )
                listing = listings[index - 1]
                display_listing(listing, listing_type)
                action = get_int_input(
                    "Actions: (0) Go back | (1) Edit attribute | (2) Delete listing | (3) View bookings: ",
                    3,
                    includes_zero=True,
                )
                if action == 1:
                    edit_listing_attribute(listing, listing_type)
                elif action == 2:
                    delete_listing(listing, listing_type)
                elif action == 3:
                    display_listing_bookings(listing_type, listing)
        else:
            listing_type = get_listing_type_input()
            create_listing(user_id, listing_type)


def handle_guest():
    user_id = get_user_id()
    while True:
        choice = get_int_input("(1) View listings | (2) View your bookings: ", 2)
        if choice == 1:
            listing_type = get_listing_type_input()
            listings = display_listings(listing_type, None)
            view_listing = yes_or_no_input(
                "Would you like to view a specific listing? (y/n) "
            )
            if view_listing:
                index = get_int_input(
                    "Enter the index of the listing you wish to view: ", len(listings)
                )
                listing = listings[index - 1]
                display_listing(listing, listing_type)
                action = get_int_input(
                    "Actions: (0) Go back | (1) Create Booking: ", 1, includes_zero=True
                )
                if action == 1:
                    if listing_type == ListingType.Property:
                        booking_id = create_property_booking(listing, user_id)
                    else:
                        booking_id = create_experience_booking(listing, user_id)
                    make_payment(booking_id, listing[0], listing_type)

        else:
            listing_type = get_listing_type_input()
            bookings = display_user_bookings(listing_type, user_id)
            interact_booking = yes_or_no_input(
                "Would you like to interact with a specific booking? (y/n) "
            )

            if interact_booking:
                index = get_int_input(
                    "Enter the index of the booking you wish to interact with: ",
                    len(bookings),
                )
                booking = bookings[index - 1]
                action = get_int_input(
                    "Actions: (0) Go back | (1) Delete Booking: ", 1, includes_zero=True
                )
                if action == 1:
                    delete_booking(booking, listing_type)


def display_users():
    headers = [
        "UserId",
        "FirstName",
        "LastName",
        "House Number",
        "Street",
        "City",
        "Province",
        "Is Super Host",
    ]
    t = PrettyTable(headers)
    users = backend.get_all_users()
    for user in users:
        t.add_row(list(user))
    print(t)


def display_hosts(only_super_host):
    headers = [
        "UserId",
        "FirstName",
        "LastName",
        "House Number",
        "Street",
        "City",
        "Province",
        "Is Super Host",
    ]
    t = PrettyTable(headers)
    users = backend.get_all_hosts(only_super_host)
    for user in users:
        t.add_row(list(user))
    print(t)


def make_payment(booking_id, prop_exp_id, listing_type):
    payment_type = input_attribute("Payment Type")
    backend.create_payment(booking_id, prop_exp_id, payment_type, listing_type)


def delete_booking(booking, listing_type):
    backend.delete_booking(booking, listing_type)
    print("Successfully deleted booking")


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
    else:
        for attrib in experience_attributes:
            inputs.append(input_attribute(attrib))

    inputs = [host_id] + inputs
    backend.insert_listing(listing_type, inputs)


def delete_listing(listing, listing_type):
    backend.delete_listing(listing, listing_type)
    print("Successfully deleted listing")


def create_experience_booking(listing, user_id):
    max_guests = listing[6]
    duration = listing[5]
    invalid_intervals = backend.get_unavailable_intervals(
        listing, ListingType.Experience
    )
    display_invalid_intervals(invalid_intervals)

    inputs = [listing[0], user_id]

    while True:
        num_guests = input_attribute("numguests")
        if num_guests > max_guests:
            print(
                "Error: there cannot be more than the max({0}) number of guests".format(
                    max_guests
                )
            )
        else:
            inputs.append(num_guests)
            break
    date_booked = datetime.today()
    date_booked_str = date_booked.strftime("%m/%d/%Y %H:%M:%S")
    inputs.append(date_booked_str)
    while True:
        start_date = input_attribute("startdate")
        if date_booked >= start_date:
            print("Error: Start Date must be after Date Booked")
            continue
        if date_within_unavailable_interval(invalid_intervals, start_date):
            print("Error: start date falls within another booking")
            continue
        duration_delta = timedelta(hours=duration.hour, minutes=duration.minute)
        end_date = start_date + duration_delta
        if date_within_unavailable_interval(invalid_intervals, end_date):
            print(
                "Error: Chosen start date does not provide enough time to complete experience"
            )
            continue
        inputs.append(start_date.strftime("%m/%d/%Y %H:%M:%S"))
        inputs.append(end_date.strftime("%m/%d/%Y %H:%M:%S"))
        break

    price = listing[-1]
    inputs.append(price)
    return backend.create_booking(ListingType.Experience, inputs)


def display_invalid_intervals(intervals):
    print("----")
    print("Unavailable between the following intervals: ")
    for interval in intervals:
        i1 = interval[0].strftime("%m/%d/%Y %H:%M:%S")
        i2 = interval[1].strftime("%m/%d/%Y %H:%M:%S")
        print(i1, "to", i2)
    print("----")


def create_property_booking(listing, user_id):
    max_guests = listing[5]
    invalid_intervals = backend.get_unavailable_intervals(listing, ListingType.Property)
    display_invalid_intervals(invalid_intervals)

    inputs = [listing[0], user_id]
    while True:
        num_guests = input_attribute("numguests")
        if num_guests > max_guests:
            print(
                "Error: there cannot be more than the max({0}) number of guests".format(
                    max_guests
                )
            )
        else:
            inputs.append(num_guests)
            break
    date_booked = datetime.today()
    date_booked_str = date_booked.strftime("%m/%d/%Y %H:%M:%S")
    inputs.append(date_booked_str)

    while True:
        start_date = input_attribute("startdate")
        if date_booked >= start_date:
            print("Error: Start Date must be after Date Booked")
            continue
        if date_within_unavailable_interval(invalid_intervals, start_date):
            print("Error: start date falls within another booking")
            continue
        inputs.append(start_date.strftime("%m/%d/%Y %H:%M:%S"))
        break

    while True:
        end_date = input_attribute("enddate")
        if end_date <= start_date:
            print("Error: End Date must be after Start Date")
            continue
        if date_within_unavailable_interval(invalid_intervals, end_date):
            print("Error: End Date falls within another booking")
            continue
        inputs.append(end_date.strftime("%m/%d/%Y %H:%M:%S"))
        break
    price = listing[-1]
    inputs.append(price)
    return backend.create_booking(ListingType.Property, inputs)


def date_within_unavailable_interval(intervals, date):
    # no intervals means any date is fine
    if len(intervals) == 0:
        return False

    for interval in intervals:
        if date >= interval[0] and date <= interval[1]:
            return True
    return False


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
        elif attribute_name in index_types:
            options = index_types[attribute_name]
            valid_nums = list(range(0, len(options)))
            print("----")
            for i in range(len(options)):
                print("{0}: {1}".format(i + 1, options[i]))
            print("----")
            print(
                "Enter the numbers for the types of {0} you want (enter 0 to stop)".format(
                    attribute_name
                )
            )
            chosen_values = []
            while True:
                value = input_attribute("value")
                if value == 0:
                    break
                elif value >= len(options):
                    print("Error: chosen option is out of bounds")
                    continue
                chosen_values.append(options[value - 1])
                print("You selected {0}".format(chosen_values[-1]))
            return chosen_values
        elif attribute_name in datetime_types:
            print("Enter {0} (all integers): ".format(attribute_name))
            day = input_attribute("day")
            month = input_attribute("month")
            year = input_attribute("year")
            if not is_valid_date(day, month, year):
                print("Error: Invalid date")
                continue
            time = input_attribute("time")
            components = time.split(":")
            hours = int(components[0])
            minutes = int(components[1])

            return datetime(year, month, day, hours, minutes)

        else:
            value = input("Enter value for {0}: ".format(attribute_name))

        return value


def is_type(x, t):
    try:
        t(x)
        return True
    except:
        return False


def is_valid_date(day, month, year):
    try:
        datetime(year, month, day)
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


def display_employee_listings(listing_type, branch_name):
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
    rows = backend.employee_select_listings(listing_type, branch_name)
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


def display_listing_bookings(listing_type, listing):
    headers = [
        "Index",
        "BookingID",
        "Property/Experience ID",
        "UserId",
        "NumGuests",
        "DateBooked",
        "StartDateTime",
        "EndDateTime",
        "Price",
    ]
    t = PrettyTable(headers)

    rows = backend.get_listing_bookings(listing, listing_type)
    index = 1
    for row in rows:
        row = list(row)
        t.add_row([index] + row)
        index += 1
    print(t)
    return rows


def display_user_bookings(listing_type, user_id):
    headers = [
        "Index",
        "BookingID",
        "Property/Experience ID",
        "UserId",
        "NumGuests",
        "DateBooked",
        "StartDateTime",
        "EndDateTime",
        "Price",
    ]
    t = PrettyTable(headers)

    rows = backend.get_user_bookings(listing_type, user_id)
    index = 1
    for row in rows:
        row = list(row)
        t.add_row([index] + row)
        index += 1
    print(t)
    return rows


def display_listing(listing, listing_type):
    headers = []
    amenities_str = ""
    inclusions_str = ""
    languages_str = ""
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
        amenities = backend.get_property_amenities(listing[0])
        for a in amenities:
            amenities_str += a[0] + ","
        amenities_str = amenities_str[:-1]

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
        inclusions = backend.get_experience_inclusions(listing[0])
        for i in inclusions:
            inclusions_str += i[0] + ","
        inclusions_str = inclusions_str[:-1]

        languages = backend.get_experience_languages(listing[0])
        for l in languages:
            languages_str += l[0] + ","
        languages_str = languages_str[:-1]

    for i in range(len(listing)):
        print("{0}: {1}".format(headers[i], listing[i]))
    if listing_type == ListingType.Property:
        print("Amenities: " + amenities_str)
    else:
        print("Inclusions: " + inclusions_str)
        print("Languages: " + languages_str)


while True:
    print("Welcome to the Airbnb application")
    while True:
        user_type = input("Are you a (G)uest, (H)ost, or (E)mployee? ")
        if user_type not in ["G", "H", "E"]:
            print("Error: must enter one of 'G', 'H', 'E'")
        else:
            break

    if user_type == "E":
        handle_employee()
    elif user_type == "H":
        handle_host()
    else:
        handle_guest()
