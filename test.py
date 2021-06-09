import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name": "Bob", "age": 14, "gender": 1},
        {"name": "Andrew","age": 20,"gender": 1},
        {"name": "Michelle","age": 28,"gender": 0},
        {"name": "Desmond","age": 18,"gender": 1},
        {"name": "Jessica","age": 24,"gender": 0}]

for i in range(1, len(data)+1):
    response = requests.post(BASE + "users/" + str(i), data[i-1])
    print(response.json())

input()
response = requests.patch(BASE + "users/2", {"age": 19, "gender": 0})
print(response.json())

input()
response = requests.delete(BASE + "users/1")
print(response)
