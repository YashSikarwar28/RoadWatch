# Finding the road for the user input

import geopandas as gpd

from classifier import classify_road
from router import get_tn_highways_contact, get_gcc_contact
from tender_lookup import get_tender_details


# Load OSM data
gpkg_path = "data/osm/planet_80.11,12.783_80.612,13.099.gpkg"

gdf = gpd.read_file(gpkg_path, layer="lines")


# User input
road_name = input("Enter road name : ")


# Search road
matches = gdf[
    gdf["name"].str.contains(
        road_name,
        case=False,
        na=False
    )
]


if not matches.empty:

    first_match = matches.iloc[0]

    road_name_found = first_match["name"]
    highway_type = first_match["highway"]

    road_class, authority = classify_road(
        highway_type
    )

    print("\nRoad found:", road_name_found)
    print("Highway type:", highway_type)
    print("Road class:", road_class)
    print("Authority:", authority)

    # ----------------------------------------
    # TENDER INFORMATION
    # ----------------------------------------

    tender = get_tender_details(
        road_name_found
    )

    if tender:

        print("\nRecent Government Work")

        print(
            "Work:",
            tender["work"]
        )

        print(
            "Department:",
            tender["department"]
        )

        print(
            "Budget:",
            tender["budget"]
        )

        print(
            "Date:",
            tender["date"]
        )

    else:

        print(
            "\nNo tender information available."
        )

    # ----------------------------------------
    # TN HIGHWAYS
    # ----------------------------------------

    if authority == "TN Highways":

        contacts = get_tn_highways_contact(
            road_name_found
        )

        print("\nRelevant contact data:")

        print(
            "Contact Person:",
            contacts["Contact Person"]
        )

        print(
            "District:",
            contacts["District"]
        )

        print(
            "Phone:",
            contacts["Phone No."]
        )

        email = contacts["E-mail ID"]

        email = (
            email
            .replace("[at]", "@")
            .replace("[dot]", ".")
        )

        print(
            "Email:",
            email
        )

    # ----------------------------------------
    # GCC
    # ----------------------------------------

    elif authority == "GCC":

        contacts = get_gcc_contact()

        print("\nRelevant contact data:")

        print(
            "Contact Person:",
            contacts["Contact Person"]
        )

        print(
            "District:",
            contacts["District"]
        )

        print(
            "Phone:",
            contacts["Phone No."]
        )

        print(
            "Email:",
            contacts["E-mail ID"]
        )

else:

    print("Road not found.")



# # Finding the road for the user input

# import geopandas as gpd
# from classifier import classify_road
# from router import get_tn_highways_contact, get_gcc_contact

# gpkg_path = "data/osm/planet_80.11,12.783_80.612,13.099.gpkg"

# gdf = gpd.read_file(gpkg_path, layer="lines")

# road_name = input("Enter road name : ")

# matches = gdf[gdf["name"].str.contains(road_name, case=False, na=False)]

# if not matches.empty:
#     first_match = matches.iloc[0]

#     road_name_found = first_match["name"]
#     highway_type = first_match["highway"]

#     road_class, authority = classify_road(highway_type)

#     print("Road found:", road_name_found)
#     print("Highway type:", highway_type)
#     print("Road class:", road_class)
#     print("Authority:", authority)

#     # TN Highways Routing
#     if authority == "TN Highways":
#         contacts = get_tn_highways_contact(road_name_found)

#         print("\nRelevant contact data:")

#         print("Contact Person:", contacts["Contact Person"])
#         print("District:", contacts["District"])
#         print("Phone:", contacts["Phone No."])

#         email = contacts["E-mail ID"]
#         email = email.replace("[at]", "@").replace("[dot]", ".")

#         print("Email:", email)

#     # GCC Routing
#     elif authority == "GCC":
#         contacts = get_gcc_contact()

#         print("\nRelevant contact data:")

#         print("Contact Person:", contacts["Contact Person"])
#         print("District:", contacts["District"])
#         print("Phone:", contacts["Phone No."])
#         print("Email:", contacts["E-mail ID"])

# else:
#     print("Road not found.")


# import geopandas as gpd
# from classifier import classify_road

# gpkg_path = "data/osm/planet_80.11,12.783_80.612,13.099.gpkg"

# gdf = gpd.read_file(gpkg_path, layer="lines")

# road_name = "Anna Salai"

# matches = gdf[gdf["name"].str.contains(road_name, case=False, na=False)]

# if not matches.empty:
#     first_match = matches.iloc[0]

#     road_name_found = first_match["name"]
#     highway_type = first_match["highway"]

#     road_class, authority = classify_road(highway_type)

#     print("Road found:", road_name_found)
#     print("Highway type:", highway_type)
#     print("Road class:", road_class)
#     print("Authority:", authority)

# else:
#     print("Road not found.")


# import geopandas as gpd

# gpkg_path = "data/osm/planet_80.11,12.783_80.612,13.099.gpkg"

# gdf = gpd.read_file(gpkg_path, layer="lines")

# road_name = "Anna Salai"

# matches = gdf[gdf["name"].str.contains(road_name, case=False, na=False)]

# print(matches[["name", "highway"]].head(10))


# # import geopandas as gpd

# # gpkg_path = "data/osm/planet_80.11,12.783_80.612,13.099.gpkg"

# # gdf = gpd.read_file(gpkg_path, layer="lines")

# # print("Road layer loaded!")
# # print(gdf.head())
# # print("\nColumns:")
# # print(gdf.columns)