from fastapi.testclient import TestClient

from app.approach1.main import app

# app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/v1/getValue?key=f48604c8-c420-4954-8296-fe74d476e7a8")
    assert response.status_code == 200
    assert response.content == "kro jexcltykgv wgw bqu y lwrqvk wquaduhnu bes"
