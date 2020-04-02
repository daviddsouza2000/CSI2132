import backend
from enums import *
from prettytable import PrettyTable
from datetime import datetime, timedelta

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
        "day",
        "month",
        "year",
    ]
)
float_types = set(["price", "Price"])
time_types = set(["duration", "Duration", "time"])
time_unit_types = set(["hours", "minutes", "seconds"])
datetime_types = set(["startdate", "enddate"])
const_types = {"Branch Name": branch_names, "Payment Type": ["cash", "credit", "debit"]}

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


def get_user_id():
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
    return user_id


def handle_employee():
    pass


def handle_host():
    user_id = get_user_id()
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
                elif action == 3:
                    display_listing_bookings(listing_type, listing)
        else:
            listing_type = ListingType(int(input("(1) Property or (2) Experience: ")))
            create_listing(user_id, listing_type)


def handle_guest():
    user_id = get_user_id()
    while True:
        choice = int(input("(1) View listings |  (2) View your bookings: "))
        if choice == 1:
            listing_type = ListingType(int(input("(1) Property or (2) Experience: ")))
            listings = display_listings(listing_type, None)
            view_listing = (
                input("Would you like to view a specific listing? (y/n) ") == "y"
            )
            if view_listing:
                index = int(input("Enter the index of the listing you wish to view: "))
                listing = listings[index - 1]
                display_listing(listing, listing_type)
                action = int(input("Actions: (0) Go back | (1) Create Booking: "))
                if action == 1:
                    if listing_type == ListingType.Property:
                        booking_id = create_property_booking(listing, user_id)
                    else:
                        booking_id = create_experience_booking(listing, user_id)
                    make_payment(booking_id, listing[0], listing_type)

        else:
            listing_type = ListingType(int(input("(1) Property or (2) Experience: ")))
            bookings = display_user_bookings(listing_type, user_id)
            interact_booking = (
                input("Would you like to interact with a specific booking? (y/n) ")
                == "y"
            )
            if interact_booking:
                index = int(
                    input("Enter the index of the booking you wish to interact with: ")
                )
                booking = bookings[index - 1]
                action = int(
                    input(
                        "Actions: (0) Go back | (1) Make Payment | (2) Delete Booking: "
                    )
                )
                if action == 1:
                    break
                elif action == 2:
                    delete_booking(booking, listing_type)


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


def create_experience_booking(listing, user_id):
    max_guests = listing[6]
    duration = listing[5]
    invalid_intervals = backend.get_unavailable_intervals(
        listing, ListingType.Experience
    )
    print(invalid_intervals)

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


def create_property_booking(listing, user_id):
    max_guests = listing[5]
    invalid_intervals = backend.get_unavailable_intervals(listing, ListingType.Property)
    print(invalid_intervals)

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
    user_type = input(
        "Welcome to the Airbnb application, are you a (G)uest, (H)ost, or (E)mployee? "
    )

    if user_type == "E":
        handle_employee()
    elif user_type == "H":
        handle_host()
    else:
        handle_guest()
