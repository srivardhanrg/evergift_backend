import re

def extract_url(filename, label):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find URLs starting with https://
            urls = re.findall(r'https://[^\s\)\"]+', content)
            if urls:
                # Get the last URL found (most recent run)
                last_url = urls[-1]
                with open("clean_urls.txt", "a") as out:
                    out.write(f"{label}: {last_url}\n")
            else:
                with open("clean_urls.txt", "a") as out:
                    out.write(f"{label}: No URL found\n")
    except Exception as e:
        with open("clean_urls.txt", "a") as out:
            out.write(f"{label}: Error reading file ({e})\n")

open("clean_urls.txt", "w").close() # Clear file
extract_url('res_id.txt', '1. RESEMBLANCE (Flux PuLID)')
extract_url('res_style.txt', '2. STYLE (Painterly)')
extract_url('res_scene.txt', '3. SCENE (Flux Kontext)')

