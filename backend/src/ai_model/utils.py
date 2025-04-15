"""
utils.py

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

import re

# Yksinkertainen HTML-formatoija, jos haluat säilyttää samaa logiikkaa
def formatGeminiResponse(text: str) -> str:
    # Lihavoi **merkinnät**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Muunna markdown-listat HTML-listoiksi
    lines = text.split("\n")
    for i, line in enumerate(lines):
        match = re.match(r'^\*\s+(.*?)$', line)
        if match:
            lines[i] = f"- {match.group(1)}"

    return "<br>".join(lines)
