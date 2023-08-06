```
# 
key = "<your_azure_translator_secret_key>"
text="Сьешь же ещё этих мягких французских булочек да выпей же чаю"
treanslator = Translator(key)
print(treanslator.translate(text))
print(treanslator.translate(text,target='en',source='ru'))

```
