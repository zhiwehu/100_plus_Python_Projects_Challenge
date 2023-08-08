# English French Translation

## Requirements

1. Run the code in console using command line.
2. It'll ask you to input English or French words or sentence. Then it'll print the related translation text.
3. If you input 'q' it'll stop to ask then quit the program.

## What will we practice in this project?

- while loop
- input text
- if conditions
- dictionary
- googletrans module

## A reference code

```python
from googletrans import Translator

def translator():
    translator = Translator()
    while True:
        given = input("Please input English or French word for translation : ")
        if given == 'q':
            break
        language = translator.detect(given).lang
        if language == 'en':
            ans = translator.translate(given, dest='fr')
            print("Translation of your english word is : " + ans.text)
        elif language == 'fr':
            ans = translator.translate(given, dest='en')
            print("Translation of your french word is : " + ans.text)
        else:
            print("Give a proper input")
translator()

```
