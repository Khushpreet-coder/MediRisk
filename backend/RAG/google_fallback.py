from googlesearch import search


def google_fallback(query):

    results = []

    try:

        for url in search(query, num_results=5):

            results.append(url)

    except Exception as e:

        print("Google Search Error:", e)

    return results