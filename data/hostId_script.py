import pandas as pd
import random as rand

ny = pd.read_csv("temp/newyork_listings.csv")
to = pd.read_csv("temp/toronto_listings.csv")
frames = [ny, to]
result = pd.concat(frames)

users = pd.read_csv("sample_users.csv")
user_ids = users["UserId"]

hostId = [0] * len(result)


for i in range(len(result)):
    hostId[i] = rand.choice(user_ids)

result["HostId"] = hostId
result = result.drop(
    [
        "Unnamed: 0",
        "scrape_id",
        "last_scraped",
        "experiences_offered",
        "neighborhood_overview",
        "notes",
        "transit",
        "access",
        "interaction",
        "house_rules",
        "thumbnail_url",
        "medium_url",
        "picture_url",
        "xl_picture_url",
        "host_id",
        "host_url",
        "host_name",
        "host_since",
        "host_location",
        "host_about",
        "host_response_time",
        "host_response_rate",
        "host_acceptance_rate",
        "host_is_superhost",
        "host_thumbnail_url",
        "host_picture_url",
        "host_neighbourhood",
        "host_listings_count",
        "host_total_listings_count",
        "host_verifications",
        "host_has_profile_pic",
        "host_identity_verified",
        "neighbourhood",
        "neighbourhood_cleansed",
        "neighbourhood_group_cleansed",
        "street",
        "zipcode",
        "market",
        "smart_location",
        "latitude",
        "longitude",
        "is_location_exact",
        "calendar_updated",
        "has_availability",
        "availability_30",
        "availability_60",
        "availability_90",
        "availability_365",
        "calendar_last_scraped",
    ],
    axis=1,
)

result = result.drop(
    [
        "bed_type",
        "square_feet",
        "security_deposit",
        "cleaning_fee",
        "guests_included",
        "extra_people",
        "minimum_nights",
        "maximum_nights",
        "minimum_minimum_nights",
        "maximum_minimum_nights",
        "minimum_maximum_nights",
        "maximum_maximum_nights",
        "minimum_nights_avg_ntm",
        "maximum_nights_avg_ntm",
        "number_of_reviews",
        "number_of_reviews_ltm",
        "first_review",
        "last_review",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_communication",
        "review_scores_location",
        "review_scores_value",
        "requires_license",
        "license",
        "jurisdiction_names",
        "instant_bookable",
        "is_business_travel_ready",
        "cancellation_policy",
        "require_guest_profile_picture",
        "require_guest_phone_verification",
        "calculated_host_listings_count",
        "calculated_host_listings_count_entire_homes",
        "calculated_host_listings_count_private_rooms",
        "calculated_host_listings_count_shared_rooms",
        "reviews_per_month",
    ],
    axis=1,
)
result.to_csv("sample_properties.csv", index=False)
