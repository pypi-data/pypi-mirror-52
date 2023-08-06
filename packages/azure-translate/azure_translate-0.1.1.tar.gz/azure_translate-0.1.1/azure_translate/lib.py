name = "azure_translator_python3"
"""Azure Translator module."""
import http.client, urllib.parse, uuid, json, requests
from future.builtins import str


class Translator(object):
    host = 'api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'

    def __init__(self, key):
        self.key = key

    def translate(self, content, target='en', source='en'):
        if type(content) == str:
            requestBody = [{
                'Text': content,
            }]
            content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
            params = "&to=" + target
            if source:
                params += "&from=" + source
            headers = {
                'Ocp-Apim-Subscription-Key': self.key,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }

            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", self.path + params, content, headers)
            response = conn.getresponse()
            return \
                json.loads(json.dumps(json.loads(response.read()), indent=4, ensure_ascii=False))[0]["translations"][0][
                    "text"]
        if type(content) == list:
            string_list = []
            for item in content:
                requestBody = [{
                    'Text': item,
                }]
                content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
                params = "&to=" + target
                if source:
                    params += "&from=" + source
                headers = {
                    'Ocp-Apim-Subscription-Key': self.key,
                    'Content-type': 'application/json',
                    'X-ClientTraceId': str(uuid.uuid4())
                }

                conn = http.client.HTTPSConnection(self.host)
                conn.request("POST", self.path + params, content, headers)
                string_list.append(conn.getresponse().read())
            output_list = []
            for each_result in string_list:
                print(each_result)
                print(target)
                try:
                    output_list.append(json.loads(json.dumps(json.loads(each_result), indent=4, ensure_ascii=False))[0][
                                           "translations"][0]["text"])
                except KeyError:
                    output_list.append("")
            return output_list


if __name__ == "__main__":
    key = "<your_azure_translator_secret_key>"
    t = Translator(key)
    print(t.translate("Сьешь же ещё этих мягких французских булочек да выпей же чаю",target='en',source='ru'))
