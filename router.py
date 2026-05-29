# Find the contact details of that particular authority like if its TN highway who is responsible

import pandas as pd


def get_tn_highways_contact(road_name):
    df = pd.read_excel("data/contacts/tn_highways.xlsx")

    df = df[df["District"].notna()]

    chennai_matches = df[
        df["District"].astype(str).str.contains("Chennai", case=False, na=False)
    ]

    if not chennai_matches.empty:
        return chennai_matches.iloc[0]

    return None


def get_gcc_contact():
    gcc_contact = {
        "Contact Person": "GCC Zonal Office",
        "District": "Chennai",
        "Phone No.": "1913",
        "E-mail ID": "complaints@chennaicorporation.gov.in"
    }

    return gcc_contact

# # Find the contact details of that particular authority like if its TN highway who is responsible

# import pandas as pd


# def get_tn_highways_contact(road_name):
#     df = pd.read_excel("data/contacts/tn_highways.xlsx")

#     df = df[df["District"].notna()]

#     chennai_matches = df[
#         df["District"].astype(str).str.contains("Chennai", case=False, na=False)
#     ]

#     if not chennai_matches.empty:
#         return chennai_matches.iloc[0]

#     return None


# # Testing
# if __name__ == "__main__":
#     contact = get_tn_highways_contact("Anna Salai")
#     print(contact)

# import pandas as pd

# def get_tn_highways_contacts():
#     df = pd.read_excel("data/contacts/tn_highways.xlsx")

#     df = df[df["District"].notna()]

#     return df

# if __name__ == "__main__":
#     contacts = get_tn_highways_contacts()
#     print(contacts.head())

# import pandas as pd

# df = pd.read_excel("data/contacts/tn_highways.xlsx")

# df = df[df["District"].notna()]

# target_districts = ["Chennai", "Chengalpattu", "Kancheepuram", "Thiruvallur"]

# filtered_contacts = df[
#     df["District"].astype(str).apply(
#         lambda x: any(district in x for district in target_districts)
#     )
# ]

# print(filtered_contacts)