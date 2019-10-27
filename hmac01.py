import hmac, hashlib, datetime, sys

def sign_hex(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).hexdigest()

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

secret_key = "jlp+/fOeTqGTRke7w1wNiqJQLfjy+uui6eebu7Vf"
service = 'rds'
host = 'rds.ap-northeast-1.amazonaws.com'
region = 'ap-northeast-1'
t = datetime.datetime.utcnow()
datestamp = t.strftime('%Y%m%d')
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
print amzdate

signing_key = getSignatureKey(secret_key, datestamp, region, service)

for c in signing_key:
    sys.stdout.write(c.encode('hex'))

print

