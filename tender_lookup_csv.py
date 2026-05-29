# For reading the CSV files for roads

import pandas as pd


def get_tender_details(road_name):

    df = pd.read_csv(
        "data/tenders/tender_data.csv"
    )

    road_name = road_name.lower().strip()

    for _, row in df.iterrows():

        tender_road = (
            str(row["road"])
            .lower()
            .strip()
        )

        if (
            road_name in tender_road
            or
            tender_road in road_name
        ):

            return {
                "road": row["road"],
                "work": row["work"],
                "department": row["department"],
                "budget": row["budget"],
                "date": row["date"]
            }

    return None


# # Test
# if __name__ == "__main__":

#     result = get_tender_details(
#         "Perungudi MRTS Road"
#     )

#     print(result)

if __name__ == "__main__":

    import pandas as pd

    df = pd.read_csv(
        "data/tenders/tender_data.csv"
    )

    print(df["road"].tolist())

    result = get_tender_details(
        "Velachery Bypass Road"
    )

    print(result)