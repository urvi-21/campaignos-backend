def clean_retrieval_results(results):

    cleaned_results = []

    seen_content = set()

    sources = results.get("sources", {})

    print("\n===================================")
    print("CLEANING RETRIEVAL RESULTS")
    print("===================================\n")

    for source_name, source_payload in sources.items():

        print(f"\nSOURCE: {source_name}")

        if source_payload.get("status") != "success":

            print("SKIPPED — source not successful")
            continue

        source_data = source_payload.get("data", [])

        print(f"RAW ITEMS: {len(source_data)}")

        if not isinstance(source_data, list):
            continue

        for item in source_data:

            content = ""

            # =====================================================
            # STRING ITEMS
            # =====================================================

            if isinstance(item, str):

                content = item.strip()

            # =====================================================
            # DICTIONARY ITEMS
            # =====================================================

            elif isinstance(item, dict):

                content = (
                    item.get("content")
                    or item.get("raw_content")
                    or item.get("snippet")
                    or item.get("text")
                    or item.get("caption")
                    or item.get("title")
                    or ""
                )

                content = str(content).strip()

            # =====================================================
            # INVALID
            # =====================================================

            else:
                continue

            # =====================================================
            # FILTERS
            # =====================================================

            if not content:
                continue

            if len(content) < 25:
                continue

            normalized = content.lower().strip()

            if normalized in seen_content:
                continue

            seen_content.add(normalized)

            cleaned_results.append({

                "source": source_name,

                "content": content
            })

        print(f"CLEANED ITEMS: {len(cleaned_results)}")

    print("\n===================================")
    print(f"TOTAL CLEANED SIGNALS: {len(cleaned_results)}")
    print("===================================\n")

    return cleaned_results