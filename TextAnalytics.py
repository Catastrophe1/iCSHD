import http.client, urllib.request, urllib.parse, urllib.error, base64

token = '186fd31dd05b48cdadd9bc370615ed60'

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': token,
}

params = urllib.parse.urlencode({
    # Request parameters
    'showStats': 'true',
})

body = {
  "documents": [
    {
      "language": "en",
      "id": "1",
      "text": "Hello world. This is some input text that I love."
    }
  ]
}

try:
    conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
    conn.request("POST", "/text/analytics/v2.1/sentiment?%s" % params, str(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))