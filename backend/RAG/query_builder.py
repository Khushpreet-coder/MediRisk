# def build_query(structured_data):

#     tests = structured_data.get("tests", [])

#     queries = []

#     for test in tests:

#         test_name = test.get("test_name", "").strip()

#         status = test.get("status", "").strip()

#         value = test.get("value", "")

#         # skip normal tests
#         if status.lower() == "normal":
#             continue

#         # build query
#         query = f"{test_name} {status} {value}"

#         queries.append(query)

#     # combine all queries
#     final_query = " ".join(queries)

#     return final_query

def build_queries(structured_data):

    tests = structured_data.get("tests", [])

    queries = []

    for test in tests:

        test_name = test.get("test_name", "").strip()

        status = test.get("status", "").strip()

        value = test.get("value", "")

        # skip normal tests
        if not status or status.lower() == "normal":
            continue

        # build query
        query = f"{test_name} {status}"

        queries.append(query)

    return queries