import random
import re
import uuid
from typing import Dict

import ray
import requests
from fastapi import FastAPI
from ray import serve
from ray.serve.handle import DeploymentHandle

from app.conf import (
    APPROACH2_MASTER_REPLICAS,
    APPROACH2_PLANNER_PARTITIONS,
    APPROACH2_WORKER_REPLICAS,
    STORAGE_PATH,
)

ray.data.DataContext.get_current().execution_options.verbose_progress = True
random.seed(42)
ray.init(address="auto", ignore_reinit_error=True)
serve.start()

app = FastAPI(debug=True)


class KVWorker:
    def __init__(self, ray_ds) -> None:
        self.storage = ray_ds

    async def get_value(self, key):
        value_list = self.storage.filter(lambda x: x["key"] == key).take()

        print("KVWorker", value_list)
        print(self.storage.count())
        print(self.storage.show())
        # raise Exception(value_list)
        if value_list:
            return value_list[0]
        # else:
        #     raise HTTPException(status_code=404,detail=f"key {key} not found")


@serve.deployment(num_replicas=APPROACH2_MASTER_REPLICAS, name="KVStoreMaster")
@serve.ingress(app)
class KVStoreMaster:
    def __init__(self, mod_actor):
        #    self.parition_dataset = parition_dataset
        self.mod_actor = mod_actor

    #    self.mod_actor : Dict[int,DeploymentHandle]= {}
    #    for k,v in self.parition_dataset.items():
    #       print(k,v.count())
    #       self.mod_actor[k] = serve.deployment(num_replicas=APPROACH2_WORKER_REPLICAS,
    #                                  name=f"KVStoreWorker_{k}")(KVWorker).bind(v)
    #   self.mod_actor[k] = KVWorker.bind(v)

    @app.get("/{key}")
    def get_value(self, key):
        # given_key_mod = uuid.UUID(key).int%(APPROACH2_PLANNER_PARTITIONS)
        given_key_mod = 3
        print(key, given_key_mod)
        # res = ray.get(self.mod_actor[given_key_mod].get_value.bind(key).execute())
        res = self.mod_actor[given_key_mod].get_value.bind(key).execute()

        print(dir(res))
        print("=====================", __name__, res, key, given_key_mod)
        return res


class Planner:
    def __init__(self, hash_mod) -> None:
        self.ray_ds = ray.data.read_text(STORAGE_PATH)
        self.transformed_ray_ds = self.ray_ds.map(self.extract_uuid_and_string)
        self.hash_mod_range = hash_mod

    def extract_uuid_and_string(self, row):
        sentence = row["text"]
        pattern = (
            r"\b([a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12})\b"
        )
        match = re.search(pattern, sentence)
        if match:
            _uuid = match.group(1)
            string_without_uuid = sentence[: match.start()] + sentence[match.end() :]
            return {
                "key": _uuid,
                "value": string_without_uuid,
                "mod": uuid.UUID(_uuid).int % (self.hash_mod_range),
            }
        else:

            return {"key": None, "value": sentence, "mod": 0}

    def get_partitioned_ds(self, *args, **kwds):
        # count = self.transformed_ray_ds.count()
        hash_ray_ds = {}
        for m in range(self.hash_mod_range):
            hash_ray_ds[m] = self.transformed_ray_ds.filter(lambda x: x["mod"] == m)
        return hash_ray_ds


if __name__ == "__main__":
    pass

    import requests

    serve_planner = Planner(APPROACH2_PLANNER_PARTITIONS)
    paritioned_ds = serve_planner.get_partitioned_ds()

    mod_actor: Dict[int, DeploymentHandle] = {}
    for k, v in paritioned_ds.items():
        print(k, v.count())
        mod_actor[k] = serve.deployment(
            num_replicas=APPROACH2_WORKER_REPLICAS, name=f"KVStoreWorker_{k}"
        )(KVWorker).bind(v)

    # modActor = {}
    # for k,v in paritioned_ds.items():
    #     modActor[k]=serve.deployment(num_replicas=APPROACH2_WORKER_REPLICAS,
    #                                  name=f"KVStoreWorker_{k}")(KVWorker).bind(v)
    print(mod_actor)
    res = mod_actor[0].get_value.bind("f48604c8-c420-4954-8296-fe74d476e7a8")
    print(ray.get(res.execute()))
    serve.run(KVStoreMaster.bind(mod_actor=mod_actor), route_prefix="/v2/getValue")
    response = requests.get(
        "http://localhost:8000/v2/getValue/426f89d1-76ec-4954-814f-283063308fdb"
    )
    print(response.text)

    # time.sleep(100)
