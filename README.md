## Hosting Object IDs

### Setup a virtualenv

```sh
virtualenv -p python3 venv
```

### install dev and application requirements
```sh
pip3 install -r requirements.txt
pip3 install -r dev-requirements.txt

```

Approach:
- Controller and Deployment setup (Actor replicas) (approach1)
- Controller , Router and Hash based Actor setup (approach2)
    - Planner and Tree based router
- Btree kind of implementation (approach3) - design document


For more detailed Documentation please refer below links:

[Approach1](docs/approach1.md)
[Approach2](docs/approach2.md)
[Approach3](docs/approach3.md)
