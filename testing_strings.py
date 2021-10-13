import re

def remove_string(text):
    string = ""
    text_start = 0
    text_end = 0
    d = True

    for m in re.finditer('\"', text):
        if d:
            d = False
            text_start = m.start()
        else:
            text_end = m.end()

    string = text[text_start:text_end]
    text = text[:text_start] + "~" + text[text_end:]
    print(text)
    print(string)

    return (text, string)
        
if __name__ == "__main__":
    remove_string()
