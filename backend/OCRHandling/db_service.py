# # backend/services/db_service.py

# from sqlalchemy.orm import Session


# def save_to_db(db: Session, data, user_id: int, filename: str):
#     # Step 1: Create report entry
#     report = Report(
#         user_id=user_id,
#         file_name=filename
#     )
#     db.add(report)
#     db.commit()
#     db.refresh(report)  # get report.id

#     # Step 2: Insert tests linked to report
#     for test in data["tests"]:
#         record = TestResult(
#             report_id=report.id,
#             test_name=test.get("test_name"),
#             value=str(test.get("value")),
#             unit=test.get("unit"),
#             reference_range=test.get("reference_range"),
#             status=test.get("status")
#         )
#         db.add(record)

#     db.commit()