import requests
while True:
    url = "http://192.168.1.101/ctf/ctf-php-rand.php?"
    req = requests.session()
    state = []
    for i in range(32):
        state.append(int(req.get(url).text.split('<code>')[0].strip()))
    state.append(int(req.get("%sgo=1"%url).text.strip()[:-32]))
    for i in range(5):
        index = len(state)
        mod = (state[index-3]+state[index-31])%2147483648 #参考rand的GLIBC实现http://www.mscs.dal.ca/~selinger/random/
        state.append(mod)
        url += 'check[]=%s&'%mod
    res = req.get(url).text
    print(res)
    if res.find('flag')!=-1:
        break
