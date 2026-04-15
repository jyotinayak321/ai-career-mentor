import httpx

# Login karo
login = httpx.post(
    'http://localhost:8000/api/auth/login',
    json={
        'email': 'jyoti@gmail.com',
        'password': 'jyoti123'
    }
)
print('Login status:', login.status_code)
token = login.json().get('token', '')
print('Token milya:', token[:30])

# Jobs fetch karo
jobs_response = httpx.get(
    'http://localhost:8000/api/jobs/recommend',
    headers={'Authorization': f'Bearer {token}'}
)
print('Jobs status:', jobs_response.status_code)
result = jobs_response.json()
print('Jobs found:', len(result.get('jobs', [])))
if result.get('jobs'):
    print('First job:', result['jobs'][0]['title'])