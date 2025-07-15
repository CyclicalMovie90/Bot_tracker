from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_verify():
    response = client.post("/api/verify", headers={"x-api-key": "e5a74d0c291f4603f99de0cf607492a6"}, json={
        "userAgent": "Test",
        "screen": {"width": 1920, "height": 1080},
        "timezoneOffset": 0,
        "language": "en-US",
        "plugins": ["TestPlugin"],
        "touchSupport": False,
        "mouseMovements": [{"x": 10, "y": 20, "t": 123}],
        "canvasFingerprint": "abc",
        "timing": {"loadStart": 0, "loadEnd": 100}
    })
    assert response.status_code == 200