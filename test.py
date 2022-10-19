import requests




BASE="http://127.0.0.1:5000/"
parameters_1={
    "name":"any thing",
    "views":2000,
    "likes":10,
    "date":"2000-09-01"
}

response=requests.put(BASE+"video/3",parameters_1)

