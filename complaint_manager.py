import pandas as pd
from datetime import datetime
import os


def save_complaint(
    road_name,
    issue_type,
    description
):

    file_path = "data/complaints.csv"

    if os.path.exists(file_path):

        df = pd.read_csv(file_path)

    else:

        df = pd.DataFrame(
            columns=[
                "complaint_id",
                "road_name",
                "issue_type",
                "description",
                "date",
                "status"
            ]
        )

    complaint_id = (
        "RW" +
        str(len(df) + 1001)
    )

    new_row = {
        "complaint_id": complaint_id,
        "road_name": road_name,
        "issue_type": issue_type,
        "description": description,
        "date": datetime.now().strftime("%d-%m-%Y"),
        "status": "Submitted"
    }

    df.loc[len(df)] = new_row

    df.to_csv(
        file_path,
        index=False
    )

    return complaint_id
