th_to_eng = {
    '-': '`', 'ๅ': '1', '/': '2', '_': '3', 'ภ': '4', 'ถ': '5', 'ุ': '6', 'ึ': '7','ค': '8', 'ต': '9', 'จ': '0', 'ข': '-', 'ช': '=',
    '%':'~', '+':'!', '๑':'@', '๒':'#', '๓':'$', '๔':'%', 'ู':'^', '฿':'&', '๕':'*', '๖':'(', '๗':')', '๘':'_', '๙':'+',

    'ๆ': 'q', 'ไ': 'w', 'ำ': 'e', 'พ': 'r', 'ะ': 't', 'ั': 'y', 'ี': 'u', 'ร': 'i', 'น': 'o', 'ย': 'p','บ': '[', 'ล': ']', 'ฃ': '\\',
    '๐': 'Q', '"': 'W', 'ฎ': 'E', 'ฑ': 'R', 'ธ': 'T', 'ํ': 'Y', '๊': 'U', 'ณ': 'I', 'ฯ': 'O', 'ญ': 'P','ฐ': '{', ',': '}', 'ฅ': '|',

    'ฟ': 'a', 'ห': 's', 'ก': 'd', 'ด': 'f', 'เ': 'g', '้': 'h', '่': 'j', 'า': 'k', 'ส': 'l', 'ว': ';','ง': "'",
    'ฤ': 'A', 'ฆ': 'S', 'ฏ': 'D', 'โ': 'F', 'ฌ': 'G', '็': 'H', '๋': 'J', 'ษ': 'K', 'ศ': 'L', 'ซ': ':', '.':'"',

    'ผ': 'z', 'ป': 'x', 'แ': 'c', 'อ': 'v', 'ิ': 'b', 'ื': 'n', 'ท': 'm', 'ม': ',', 'ใ': '.', 'ฝ': '/',
    '(': 'Z', ')': 'X', 'ฉ': 'C', 'ฮ': 'V', '.': 'B', '์': 'N', '?': 'M', 'ฒ': '<', 'ฬ': '>', 'ฦ': '?'
}

eng_to_th = {v: k for k, v in th_to_eng.items()}

def convert_text(text, mapping):
    result = ''
    for char in text:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    return result

def is_thai_text(text):
    # Count how many chars are in th_to_eng keys (Thai chars)
    count = 0
    for char in text:
        if char in th_to_eng:
            count += 1
    return count > len(text) / 2  # More than half are Thai chars

def is_english_text(text):
    # Count how many chars are in eng_to_th keys (English chars)
    count = 0
    for char in text:
        if char in eng_to_th:
            count += 1
    return count > len(text) / 2

def main():
    print("Keyboard Converter (Auto-detect TH <-> ENG)")
    text = input("Enter text to convert: ")

    if is_thai_text(text):
        converted = convert_text(text, th_to_eng)
        print("Detected Thai layout. Converted to English:")
    elif is_english_text(text):
        converted = convert_text(text, eng_to_th)
        print("Detected English layout. Converted to Thai:")
    else:
        print("Could not confidently detect input language/layout. Showing input as-is.")
        converted = text

    print(converted)

if __name__ == '__main__':
    main()
