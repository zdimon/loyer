import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' ,
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache'
    
}

location = 'http://auth.zakon.kz//login/autologin?returnApp=sud&returnUrl=http%3A%2F%2Fonline.zakon.kz%2Fsud%2F%2F'
print 'Try to go to 301 loc %s' % location
sec_cookie = {'SessionId': 'OTQ4NjIyMTc=', 'PHPSESSID': 'bmk1vqvf437jv8saimadgk1uv4'}
r = requests.get(location,headers=headers, cookies = sec_cookie, allow_redirects=False)
print r.status_code

location = r.headers['Location']

print location

