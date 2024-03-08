import ray

ray.init(namespace="KVStore")

# Define your tasks and functions here

# To keep the cluster running in the background, you can add an infinite loop
# or any other method to keep the script running indefinitely
try:
    while True:
        pass
except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Stopping Ray cluster.")
