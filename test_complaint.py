from complaint_manager import save_complaint

complaint_id = save_complaint(
    "Anna Salai",
    "Pothole",
    "Large pothole near signal"
)

print(
    "Complaint Submitted:",
    complaint_id
)