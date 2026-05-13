try:
    import chromadb
except Exception:
    chromadb = None


_collection = None
_collection_error = None


def _get_collection():

    global _collection, _collection_error

    if _collection is not None:
        return _collection

    if chromadb is None:
        _collection_error = "chromadb is not installed or failed to import"
        return None

    try:
        client = chromadb.Client()
        _collection = client.get_or_create_collection(
            name="campaign_memory"
        )
        return _collection

    except Exception as e:
        _collection_error = str(e)
        return None


def store_campaign_memory(
    campaign_id,
    text,
    metadata
):

    collection = _get_collection()

    if collection is None:
        return {
            "status": "skipped",
            "service": "chromadb",
            "error": _collection_error
        }

    try:
        collection.upsert(
            documents=[text],
            metadatas=[metadata],
            ids=[campaign_id]
        )

        return {
            "status": "success",
            "service": "chromadb"
        }

    except Exception as e:
        return {
            "status": "failed",
            "service": "chromadb",
            "error": str(e)
        }


def retrieve_similar_campaigns(query, n_results=3):

    collection = _get_collection()

    if collection is None:
        return {
            "documents": [],
            "metadatas": [],
            "ids": [],
            "service_status": {
                "status": "skipped",
                "service": "chromadb",
                "error": _collection_error
            }
        }

    try:
        return collection.query(
            query_texts=[query],
            n_results=n_results
        )

    except Exception as e:
        return {
            "documents": [],
            "metadatas": [],
            "ids": [],
            "service_status": {
                "status": "failed",
                "service": "chromadb",
                "error": str(e)
            }
        }
