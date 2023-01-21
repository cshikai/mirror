import requests

def test_send_query():
    item = {'query': 'Hello World'}
    response = requests.post(url="http://localhost:3000/query", json=item, headers={'content-type':'application/json'})
    print(response)

if __name__ == '__main__':
    test_send_query()