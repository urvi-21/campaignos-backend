def clean_retrieval_results(results):

    cleaned_results = []

    seen_content = set()

    # =========================================================
    # GET SOURCES
    # =========================================================

    sources = results.get("sources", {})

    # =========================================================
    # ITERATE THROUGH SOURCES
    # =========================================================

    for source_name, source_payload in sources.items():

        if source_payload.get("status") != "success":
            continue

        source_data = source_payload.get("data", [])

        if not isinstance(source_data, list):
            continue

        for item in source_data:

            # =================================================
            # HANDLE STRING ITEMS
            # =================================================

            if isinstance(item, str):

                content = item.strip()

            # =================================================
            # HANDLE DICTIONARY ITEMS
            # =================================================

            elif isinstance(item, dict):

                content = item.get("content", "").strip()

            else:
                continue

            # =================================================
            # FILTER LOW-QUALITY CONTENT
            # =================================================

            if not content:
                continue

            if len(content) < 40:
                continue

            if content in seen_content:
                continue

            seen_content.add(content)

            cleaned_results.append({
                "source": source_name,
                "content": content
            })

    # =========================================================
    # RETURN CLEANED INTELLIGENCE
    # =========================================================

    return cleaned_results