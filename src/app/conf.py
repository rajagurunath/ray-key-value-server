import os

# curr_dir =
curr_dir = os.path.dirname(os.path.realpath(__file__))

resource_dir = os.path.dirname(curr_dir) + "/resources/example.input.data"
print(resource_dir)
NUM_REPLICAS = 2
STORAGE_PATH = os.environ.get("STORAGE_PATH", resource_dir)


APPROACH2_MASTER_REPLICAS = 1
APPROACH2_WORKER_REPLICAS = 1
APPROACH2_PLANNER_PARTITIONS = 4

UUID_PATTERN = (
    r"\b([a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12})\b"
)
