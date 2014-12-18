import pyotp
import time
import base64
import hashlib

from hotpie import HOTP, TOTP

key = 'ngocson2vn@gmail.com'
t1 = TOTP(key, digits=10)      # <time-based-value>
print "totp1:%s length:%d" % (t1, len(str(t1)))

secret = base64.b32encode(key)
totp = pyotp.TOTP(secret, 10, hashlib.sha512, interval=30)
t2 = totp.now()

print "totp2:%s length:%d" % (t2, len(str(t2)))


if str(t1) == str(t2):
	text = 'ngocson2vn@gmail.com:%s' % t1
	print text
	print base64.b64encode(text)
