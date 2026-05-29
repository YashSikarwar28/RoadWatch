from tender_data import TENDER_DATA


def get_tender_details(road_name):

    road_name = road_name.lower().strip()

    for tender in TENDER_DATA:

        tender_road = tender["road"].lower().strip()

        # Partial matching
        if (
            road_name in tender_road
            or
            tender_road in road_name
        ):
            return tender

    return None


# Test
if __name__ == "__main__":

    result = get_tender_details(
        "Anna Salai"
    )

    print(result)



# from tender_data import TENDER_DATA


# def get_tender_details(road_name):

#     for tender in TENDER_DATA:

#         if tender["road"].lower() == road_name.lower():

#             return tender

#     return None


# # Test
# if __name__ == "__main__":

#     result = get_tender_details(
#         "Anna Salai (Mount Road)"
#     )

#     print(result)

