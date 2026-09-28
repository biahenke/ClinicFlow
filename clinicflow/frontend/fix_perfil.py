import re

path = r'c:\Users\Public\ClinicFlow\clinicflow\frontend\perfil.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace classes
content = content.replace('class="form-control"', 'class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"')
content = content.replace('class="form-control bg-opacity-50"', 'class="w-full bg-[#0b1221] bg-opacity-50 border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 cursor-not-allowed"')
content = content.replace('class="form-label"', 'class="block text-xs font-semibold text-slate-400 mb-1"')

# Button replacements
# First standard btn-primary
content = content.replace('class="btn-primary flex items-center gap-2"', 'class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-bold text-sm transition-colors flex items-center gap-2"')
# Remove inline style for rose button and add tailwind classes
content = content.replace('class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-bold text-sm transition-colors flex items-center gap-2" style="background: #f43f5e;"', 'class="bg-rose-600 hover:bg-rose-500 text-white px-4 py-2 rounded-lg font-bold text-sm transition-colors flex items-center gap-2"')

# Add toast CSS back just in case it was deleted
toast_css = """
    .toast { position: fixed; bottom: 20px; right: 20px; padding: 1rem 1.5rem; border-radius: 0.75rem; color: white; font-weight: 500; display: flex; align-items: center; gap: 1rem; z-index: 1000; transition: opacity 0.3s; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5); }
    .toast.success { background-color: #10b981; }
    .toast.error { background-color: #ef4444; }
  </style>
"""
if '.toast {' not in content:
    content = content.replace('</style>', toast_css)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Perfil HTML fixed.")
