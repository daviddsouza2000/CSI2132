import pandas as pd
import random

user_df = pd.read_csv("sample_users.csv")
property_df = pd.read_csv("sample_properties.csv")

min_id = 1000
max_id = 999999
used_ids = set()
num_reviews = 1000
property_ids = property_df["id"]
user_ids = user_df["UserId"]
lorem = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque venenatis vitae diam eget finibus. Ut lacinia porta mauris eu blandit. Sed vel mattis dolor. Duis mollis, nisi vitae venenatis luctus, lorem sem hendrerit neque, sed maximus justo mauris eget felis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer hendrerit at turpis non sollicitudin. Duis maximus at ligula et congue. Maecenas pellentesque magna dolor, eu aliquet metus rhoncus eget. Donec blandit elementum justo, eget lacinia ligula finibus non. Nam sed turpis ligula. In blandit suscipit tellus, ut venenatis dui convallis a. Mauris vehicula finibus urna, sed tempus tellus tempor nec. Vivamus sagittis est nibh, non accumsan ligula dignissim ac.

Nulla sollicitudin lorem ac leo sagittis convallis. Suspendisse potenti. Morbi dui neque, interdum ut pulvinar ut, euismod at dolor. Sed eu eros elit. Integer at malesuada arcu. Aenean pulvinar odio dolor, vitae eleifend lorem tincidunt eget. Maecenas mauris nisl, gravida vel elit et, molestie ultrices sapien.

Curabitur et dolor nibh. Vivamus sit amet sollicitudin dolor, sed maximus tortor. Quisque semper justo velit, eget rutrum arcu lobortis vitae. Aliquam augue orci, convallis at condimentum at, porta quis ante. Maecenas arcu neque, ornare sed scelerisque ac, faucibus condimentum dui. Nullam fermentum egestas neque id interdum. Aenean ut justo lectus. Proin at risus quis ligula aliquam blandit molestie nec leo. Nullam et scelerisque ante. Praesent eu ante non neque finibus porttitor. Suspendisse potenti. Morbi eu mauris ante.

Aliquam ac leo feugiat, congue dui sed, aliquam dui. Morbi a ante lacus. Vivamus eleifend vel ipsum sit amet euismod. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In lacinia sapien et nibh aliquet vulputate. Aenean feugiat, elit id pellentesque tincidunt, ligula leo vestibulum neque, id dictum urna lorem vitae lectus. Ut dignissim vehicula dui non rhoncus. Aliquam erat volutpat. Suspendisse aliquet ullamcorper odio, eget sagittis nisi interdum in. Donec non vestibulum turpis, vel finibus ipsum. Duis tincidunt et velit at egestas.

Aliquam gravida sapien vitae sem accumsan, sed aliquet quam iaculis. Nunc ornare ante dignissim sapien molestie, vel elementum tellus egestas. Nam rutrum scelerisque nulla ut luctus. Nulla et urna quis massa suscipit venenatis id pretium elit. In molestie urna lorem, a placerat tortor vestibulum ut. Cras ut nisl sed odio vulputate dapibus ut ut lectus. Vestibulum varius, enim sed faucibus gravida, odio nunc dictum odio, non venenatis lectus libero ut urna. Nullam ornare sapien vel mi mollis, vitae gravida erat interdum. Cras non rutrum erat, et congue tortor. Quisque urna sem, dapibus id viverra sed, dapibus id erat. Morbi vel neque ullamcorper nisi ultrices ullamcorper. Donec eget ipsum tincidunt, venenatis elit fringilla, vulputate enim. Suspendisse gravida, magna ut consequat eleifend, magna quam mattis ipsum, consequat sollicitudin mi nisi vel ante. Integer lacus lorem, accumsan id odio accumsan, mollis porta ex.
"""

result_df = pd.DataFrame(
    columns=[
        "ReviewId",
        "PropertyId",
        "UserId",
        "Description",
        "Rating",
        "Communications",
        "Cleanliness",
        "Value",
    ]
)

for i in range(num_reviews):
    review_id = random.randint(min_id, max_id)
    while review_id in used_ids:
        review_id = random.randint(min_id, max_id)

    used_ids.add(review_id)
    prop_id = random.choice(property_ids)
    user_id = random.choice(user_ids)
    inf = random.randint(0, len(lorem) - 2)
    sup = random.randint(inf, len(lorem))
    description = lorem[inf:sup]

    rating = random.randint(1, 5)
    communications = random.randint(1, 5)
    cleanliness = random.randint(1, 5)
    value = random.randint(1, 5)
    result_df = result_df.append(
        {
            "ReviewId": review_id,
            "PropertyId": prop_id,
            "UserId": user_id,
            "Description": description,
            "Rating": rating,
            "Communications": communications,
            "Cleanliness": cleanliness,
            "Value": value,
        },
        ignore_index=True,
    )
result_df.to_csv("sample_prop_reviews.csv")
