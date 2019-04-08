ss="""TW5650Y - 0TS UZ50S S0V LZW UZ50WKW 9505KL4G 1X WVMUSL510 S001M0UWV 910VSG S0 WFLW0K510 1X LZW54 WF5KL50Y 2S4L0W4KZ52 L1 50U14214SLW X5L0WKK S0V TSK7WLTS88 VWNW8129W0L 50 W8W9W0LS4G, 95VV8W S0V Z5YZ KUZ118K SU41KK UZ50S.LZW S001M0UW9W0L ESK 9SVW SL S K5Y050Y UW4W910G L1VSG TG 0TS UZ50S UW1 VSN5V KZ1W9S7W4 S0V FM LS1, V54WUL14 YW0W4S8 1X LZW 50LW40SL510S8 U112W4SL510 S0V WFUZS0YW VW2S4L9W0L 1X LZW 9505KL4G 1X WVMUSL510.
"EW S4W WFU5LWV L1 T41SVW0 1M4 2S4L0W4KZ52 E5LZ LZW 9505KL4G 1X WVMUSL510 L1 9S7W S 810Y-8SKL50Y 592SUL 10 LZW 85NWK 1X UZ50WKW KLMVW0LK LZ41MYZ S 6150L8G-VWK5Y0WV TSK7WLTS88 UM445UM8M9 S0V S E5VW 4S0YW 1X KUZ118 TSK7WLTS88 241Y4S9K," KS5V KZ1W9S7W4. "LZ5K U1995L9W0L 9S47K S01LZW4 958WKL10W 50 LZW 0TS'K G1MLZ S0V TSK7WLTS88 VWNW8129W0L WXX14LK 50 UZ50S." X8SY { YK182V9ZUL9STU5V}"""

def rot(s, f, ranged=range(1000)):
    if ord(s) in ranged:
        return chr(ord(s)+f)
    return s
def rot_2(s,offSet=13):
     d={chr(i+c) : chr((i+offSet) % 26 + c) for i in range(26) for c in (65,97)}
     return ''.join([d.get(c, c) for c in s])

print(ss)
print('---------------------------------')
ss=rot_2(ss)
print(ss)
print('---------------------------------')
a=''
for i in ss:
    a+=rot(i,27,range(65,97))
print(a)
print('---------------------------------')
b=''
for j in a:
    b+=rot(j,62,range(48,53))
print(b)
print('---------------------------------')
c=''
for j in b:
    c+=rot(j,52,range(53,58))
print(c)
