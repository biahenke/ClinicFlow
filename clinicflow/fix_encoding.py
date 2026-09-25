import os

directory = 'c:/Users/Public/ClinicFlow/clinicflow/frontend'

replacements = {
    'Ã¡': 'á', 'Ã ': 'à', 'Ã¢': 'â', 'Ã£': 'ã', 'Ã¤': 'ä',
    'Ã©': 'é', 'Ã¨': 'è', 'Ãª': 'ê', 'Ã«': 'ë',
    'Ã­': 'í', 'Ã¬': 'ì', 'Ã®': 'î', 'Ã¯': 'ï',
    'Ã³': 'ó', 'Ã²': 'ò', 'Ã´': 'ô', 'Ãµ': 'õ', 'Ã¶': 'ö',
    'Ãº': 'ú', 'Ã¹': 'ù', 'Ã»': 'û', 'Ã¼': 'ü',
    'Ã§': 'ç', 'Ã±': 'ñ',
    'Ã ': 'Á', 'Ã€': 'À', 'Ã‚': 'Â', 'Ãƒ': 'Ã', 'Ã„': 'Ä',
    'Ã‰': 'É', 'Ãˆ': 'È', 'ÃŠ': 'Ê', 'Ã‹': 'Ë',
    'Ã ': 'Í', 'ÃŒ': 'Ì', 'ÃŽ': 'Î', 'Ã ': 'Ï',
    'Ã“': 'Ó', 'Ã’': 'Ò', 'Ã”': 'Ô', 'Ã•': 'Õ', 'Ã–': 'Ö',
    'Ãš': 'Ú', 'Ã™': 'Ù', 'Ã›': 'Û', 'Ãœ': 'Ü',
    'Ã‡': 'Ç', 'Ã‘': 'Ñ',
    'â€¢': '•', 'â€“': '–', 'â€”': '—', 'â€˜': '‘', 'â€™': '’', 'â€œ': '“', 'â€ ': '”',
    'Âº': 'º', 'Âª': 'ª', 'Â°': '°', 'Â´': '´',
    'Â': ''
}

for filename in os.listdir(directory):
    if filename.endswith('.html') or filename.endswith('.js'):
        filepath = os.path.join(directory, filename)
        
        # Read as UTF-8
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        fixed_content = content
        
        # fallback to replace dict if direct conversion fails (or to be safe)
        if 'Ã' in content or 'â€' in content or 'Â' in content:
            # We try the standard approach first
            try:
                fixed_content = content.encode('latin1').decode('utf-8')
            except Exception:
                for wrong, right in replacements.items():
                    fixed_content = fixed_content.replace(wrong, right)
            
            # Save fixed content back
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(fixed_content)
            print(f'Fixed encoding for {filename}')
            
