from dns.resolver import Resolver

print 111
namelist = open('subnames.txt').readlines()
qs = Resolver()
for name in namelist:
   subdomain = name.strip()+'.'+'qq.com'
   answers = qs.query(subdomain)
   print subdomain,
   if answers:
      for answer in answers:
          print answer.address
