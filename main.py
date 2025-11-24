import re
import sys
from pathlib import Path

import requests


def gfont_woff2_downloader(font_name: str, output_dir='fonts'):
    """Download all WOFF2 files of a Google Font.

    Args:
        font_name: Name of the font (e.g., "Roboto")
        output_dir: Local folder to save fonts

    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Format font name for Google Fonts URL
    font_name_url = font_name.replace(' ', '+')
    css_url = f'https://fonts.googleapis.com/css?family={font_name_url}&subset=all'

    print(f'Fetching CSS for {font_name} ...')
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        )
    }
    r = requests.get(css_url, headers=headers)
    r.raise_for_status()
    css_content = r.text

    # Extract all @font-face blocks
    font_blocks = re.findall(r'@font-face {[^}]+}', css_content)

    if not font_blocks:
        print('No font-face blocks found!')
        return

    # Create output folder
    font_folder = output_dir / font_name.replace(' ', '_')
    font_folder.mkdir(exist_ok=True)

    for block in font_blocks:
        # Extract font-family
        family_match = re.search(r"font-family:\s*'([^']+)'", block)
        # weight_match = re.search(r'font-weight:\s*(\d+)', block)
        # style_match = re.search(r'font-style:\s*(\w+)', block)
        url_match = re.search(r'url\((https://fonts.gstatic.com/.*?\.woff2)\)', block)

        # if not (family_match and weight_match and style_match and url_match):
        if not (family_match and url_match):
            continue

        family = family_match.group(1).replace(' ', '')
        # weight = weight_match.group(1)
        # style = style_match.group(1)
        url = url_match.group(1)

        # filename = f'{family}-{weight}-{style}.woff2'
        filename = f'{family}.woff2'
        filepath = font_folder / filename

        if filepath.exists():
            print(f'Skipping {filename}, already exists')
            continue

        print(f'Downloading {filename} ...')
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(r.content)

    print(f'All fonts saved to {font_folder}')


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "Noto Sans"')
        print('Or: uv run main.py "Noto Sans"')
        sys.exit(1)

    font_name = sys.argv[1]
    gfont_woff2_downloader(font_name)


if __name__ == '__main__':
    main()

