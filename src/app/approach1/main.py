import os
import re
import uuid
from typing import Annotated

import pandas as pd
import ray
import requests
from fastapi import FastAPI, HTTPException, Query
from ray import serve

from app.conf import NUM_REPLICAS, STORAGE_PATH, UUID_PATTERN

ray.init(address="auto", ignore_reinit_error=True)
serve.start()

app = FastAPI(debug=True)


@serve.deployment(num_replicas=NUM_REPLICAS, name="KVSTORE1")
@serve.ingress(app)
class KVStore1:
    def __init__(self):
        self.storage = self._get_kvpairs()

    def extract_uuid_and_string(self, sentence):
        pattern = UUID_PATTERN
        match = re.search(pattern, sentence)
        if match:
            _uuid = match.group(1)
            string_without_uuid = sentence[: match.start()] + sentence[match.end() :]
            return _uuid, string_without_uuid, uuid.UUID(_uuid).int % 10
        else:
            return None, sentence, None

    def _get_kvpairs(self):
        print(os.getcwd())
        df = pd.read_csv(STORAGE_PATH, names=["text"])
        tuple_series = df.text.apply(self.extract_uuid_and_string)
        return pd.DataFrame(
            [[a, b, c] for a, b, c in tuple_series.values],
            columns=["key", "value", "mod"],
        )

    def _get_value(self, key):
        result = self.storage[self.storage["key"] == key].to_dict(orient="records")
        if result:
            return result[0]["value"]
        else:
            HTTPException(404, f"Requested {key} key not found")

    @app.get("/{key}")
    async def get_value(
        self, key: Annotated[str | None, Query(pattern=UUID_PATTERN)] = None
    ):
        """get value for the given Key

        Args:
            key (Annotated[ str  |  None, Query, optional): _description_. Defaults to UUID_PATTERN)]=None.
            - Validates whether the given key adheres to the UUID regex pattern
        Returns:
            _type_: _description_
        """
        return self._get_value(key)


if __name__ == "__main__":
    pass

    import requests

    serve.run(KVStore1.bind(), route_prefix="/v1/getValue")
    response = requests.get(
        "http://localhost:8000/getValue/f48604c8-c420-4954-8296-fe74d476e7a8"
    )
    print(response.text)
    # time.sleep(100)
