from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

th_to_eng = {
    '-': '`', 'ๅ': '1', '/': '2', '_': '3', 'ภ': '4', 'ถ': '5', 'ุ': '6', 'ึ': '7','ค': '8', 'ต': '9', 'จ': '0', 'ข': '-', 'ช': '=',
    '%':'~', '+':'!', '๑':'@', '๒':'#', '๓':'$', '๔':'%', 'ู':'^', '฿':'&', '๕':'*', '๖':'(', '๗':')', '๘':'_', '๙':'+',
    'ๆ': 'q', 'ไ': 'w', 'ำ': 'e', 'พ': 'r', 'ะ': 't', 'ั': 'y', 'ี': 'u', 'ร': 'i', 'น': 'o', 'ย': 'p','บ': '[', 'ล': ']', 'ฃ': '\\',
    '๐': 'Q', '"': 'W', 'ฎ': 'E', 'ฑ': 'R', 'ธ': 'T', 'ํ': 'Y', '๊': 'U', 'ณ': 'I', 'ฯ': 'O', 'ญ': 'P','ฐ': '{', ',': '}', 'ฅ': '|',
    'ฟ': 'a', 'ห': 's', 'ก': 'd', 'ด': 'f', 'เ': 'g', '้': 'h', '่': 'j', 'า': 'k', 'ส': 'l', 'ว': ';','ง': "'",
    'ฤ': 'A', 'ฆ': 'S', 'ฏ': 'D', 'โ': 'F', 'ฌ': 'G', '็': 'H', '๋': 'J', 'ษ': 'K', 'ศ': 'L', 'ซ': ':', '.':'"',
    'ผ': 'z', 'ป': 'x', 'แ': 'c', 'อ': 'v', 'ิ': 'b', 'ื': 'n', 'ท': 'm', 'ม': ',', 'ใ': '.', 'ฝ': '/',
    '(': 'Z', ')': 'X', 'ฉ': 'C', 'ฮ': 'V', 'ฺ': 'B', '์': 'N', '?': 'M', 'ฒ': '<', 'ฬ': '>', 'ฦ': '?'
}

eng_to_th = {v: k for k, v in th_to_eng.items()}

def convert_text(text, mapping):
    return ''.join(mapping.get(c, c) for c in text)

def is_thai_text(text):
    return sum(c in th_to_eng for c in text) > len(text)/2

def is_english_text(text):
    return sum(c in eng_to_th for c in text) > len(text)/2

HTML_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Thai-English Keyboard Converter</title>
<style>
  body {
    margin: 0; min-height: 100vh;
    background: linear-gradient(135deg, #8dc6ff 0%, #ffffff 100%);
    font-family: 'Inter', sans-serif;
    display: flex; justify-content: center; align-items: center; padding: 20px;
  }
  .container {
    background: #fff; max-width: 600px; width: 100%;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12), 0 4px 12px rgba(0,0,0,0.08);
    padding: 32px 36px; box-sizing: border-box;
  }
  h1 {
    margin: 0 0 24px; font-weight: 600; color: #1e293b; font-size: 28px; text-align: center;
  }
  label {
    font-weight: 600; color: #334155; margin-bottom: 10px; display: block; font-size: 16px;
  }
  textarea {
    width: 100%; height: 130px; font-size: 16px;
    padding: 14px 18px; border-radius: 12px; border: 1.8px solid #cbd5e1;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    font-family: 'Inter', sans-serif; resize: vertical; outline-offset: 2px; color: #0f172a;
    box-sizing: border-box; line-height: 1.5;
  }
  textarea::placeholder {
    color: #94a3b8; font-style: italic;
  }
  textarea:focus {
    border-color: #6366f1;
    box-shadow: 0 0 10px rgba(99,102,241,0.4);
    outline: none;
  }
  .result {
    margin-top: 28px; background: #f1f5f9; border-radius: 14px;
    padding: 24px 28px; font-size: 18px; line-height: 1.6; color: #334155;
    min-height: 130px; user-select: text; white-space: pre-wrap;
    opacity: 0; transform: translateY(12px); filter: blur(4px);
    transition: opacity 0.45s ease, transform 0.45s ease, filter 0.45s ease;
  }
  .result.visible {
    opacity: 1; transform: translateY(0); filter: blur(0);
  }
  .message {
    font-weight: 700; margin-bottom: 14px; color: #4f46e5;
    letter-spacing: 0.03em; user-select: none;
  }
  .buttons {
    margin-top: 16px; display: flex; gap: 12px; justify-content: flex-end;
  }
  button {
    padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer;
    transition: background-color 0.3s ease;
  }
  #copy_btn {
    background-color: #6366f1; border: none; color: white;
  }
  #toggle_btn {
    background-color: #f3f4f6; border: 1.8px solid #cbd5e1; color: #334155;
  }
  #toast {
    visibility: hidden; min-width: 180px;
    background-color: #4f46e5; color: white; text-align: center;
    border-radius: 8px; padding: 12px 20px;
    position: fixed; bottom: 30px; right: 30px;
    font-weight: 600; font-family: 'Inter', sans-serif; font-size: 16px;
    box-shadow: 0 4px 14px rgba(79,70,229,0.4);
    opacity: 0; transition: opacity 0.4s ease; z-index: 9999;
  }
  @media (max-width: 480px) {
    .container {padding: 24px 20px;}
    h1 {font-size: 24px;}
    .result {font-size: 16px; padding: 20px 18px; min-height: 110px;}
    textarea {height: 110px;}
  }
</style>
</head>
<body>
<div class="container">
  <h1>Thai-English Keyboard Converter</h1>
  <label for="input_text">Type or paste your text below:</label>
  <textarea id="input_text" placeholder="Start typing in Thai or English keyboard layout..."></textarea>
  <div class="result" id="result"></div>
  <div class="buttons">
    <button id="copy_btn" type="button">Copy</button>
    <button id="toggle_btn" type="button">Toggle Mapping</button>
  </div>
</div>
<div id="toast"></div>

<script>
const input = document.getElementById('input_text');
const resultDiv = document.getElementById('result');
const copyBtn = document.getElementById('copy_btn');
const toggleBtn = document.getElementById('toggle_btn');
const toast = document.getElementById('toast');

let lastConvertedText = '';
let currentDirection = ''; // 'thai_to_eng' or 'eng_to_th'
let timeoutId = null;

// Initial paste from clipboard if text length < 100
navigator.clipboard.readText().then(text => {
  if(text.length > 0 && text.length < 100) {
    input.value = text;
    triggerConvert(text);
  }
}).catch(() => {});

function triggerConvert(text) {
  fetch('/convert', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text})
  }).then(res => res.json())
    .then(data => {
      resultDiv.classList.remove('visible');
      setTimeout(() => {
        resultDiv.innerHTML = '<div class="message">' + data.message + '</div>' + data.converted_text;
        resultDiv.classList.add('visible');
        lastConvertedText = data.converted_text;
        currentDirection = data.direction;
      }, 50);
    }).catch(() => {
      resultDiv.textContent = 'Oops! Something went wrong.';
      resultDiv.classList.add('visible');
    });
}

input.addEventListener('input', () => {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    triggerConvert(input.value);
  }, 300);
});

copyBtn.addEventListener('click', () => {
  if (!lastConvertedText) return;
  navigator.clipboard.writeText(lastConvertedText)
    .then(() => showToast('Copied to clipboard!'))
    .catch(() => showToast('Failed to copy.'));
});

toggleBtn.addEventListener('click', () => {
  if (!lastConvertedText) return;
  const newDirection = currentDirection === 'thai_to_eng' ? 'eng_to_th' : 'thai_to_eng';
  fetch('/toggle_convert', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: lastConvertedText, direction: newDirection})
  }).then(res => res.json())
    .then(data => {
      resultDiv.classList.remove('visible');
      setTimeout(() => {
        resultDiv.innerHTML = '<div class="message">' + data.message + '</div>' + data.converted_text;
        resultDiv.classList.add('visible');
        lastConvertedText = data.converted_text;
        currentDirection = newDirection;
      }, 50);
    }).catch(() => {
      showToast('Error toggling conversion.');
    });
});

function showToast(message) {
  toast.textContent = message;
  toast.style.visibility = 'visible';
  toast.style.opacity = '1';
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => {
      toast.style.visibility = 'hidden';
    }, 400);
  }, 2000);
}
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json(force=True)
    text = data.get('text', '')

    if is_thai_text(text):
        converted = convert_text(text, th_to_eng)
        message = "Detected Thai layout. Converted to English:"
        direction = 'thai_to_eng'
    elif is_english_text(text):
        converted = convert_text(text, eng_to_th)
        message = "Detected English layout. Converted to Thai:"
        direction = 'eng_to_th'
    else:
        message = "Could not confidently detect input layout. Showing original text."
        converted = text
        direction = 'none'

    return jsonify({'converted_text': converted, 'message': message, 'direction': direction})

@app.route('/toggle_convert', methods=['POST'])
def toggle_convert():
    data = request.get_json(force=True)
    text = data.get('text', '')
    direction = data.get('direction', '')

    if direction == 'thai_to_eng':
        converted = convert_text(text, th_to_eng)
        message = "Toggled: Thai to English conversion"
    elif direction == 'eng_to_th':
        converted = convert_text(text, eng_to_th)
        message = "Toggled: English to Thai conversion"
    else:
        converted = text
        message = "No conversion applied"

    return jsonify({'converted_text': converted, 'message': message, 'direction': direction})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
