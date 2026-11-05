"""Check actual services running in the CI runner's local Docker network."""
import json
import time
import urllib.error
import urllib.request

BASE = 'http://127.0.0.1:8000'
for attempt in range(60):
    try:
        with urllib.request.urlopen(BASE + '/djangoapp/get_dealers', timeout=10) as response:
            dealers = json.load(response)
        if dealers['status'] == 200 and len(dealers['dealers']) == 50:
            break
    except (urllib.error.URLError, TimeoutError):
        pass
    time.sleep(5)
else:
    raise RuntimeError('Container stack failed to become ready')

for path in ['/', '/about/', '/contact/', '/djangoapp/get_cars']:
    with urllib.request.urlopen(BASE + path, timeout=15) as response:
        assert response.status == 200, path
        if path.endswith('get_cars'):
            assert len(json.load(response)['CarModels']) > 0
with urllib.request.urlopen('http://127.0.0.1:5050/analyze/Fantastic%20services', timeout=15) as response:
    assert json.load(response)['sentiment'] == 'positive'
print('PASS: Docker MongoDB/Express, Flask sentiment, and Django/React endpoints')
