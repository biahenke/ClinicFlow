import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add ID to the red dot and hide it initially
pattern_bell = r'<span class="absolute top-0 right-0 w-2\.5 h-2\.5 bg-red-500 rounded-full border-2 border-\[#0b1221\]"></span>'
new_bell = r'<span id="notification-dot" class="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-[#0b1221] hidden"></span>'
content = re.sub(pattern_bell, new_bell, content)

# 2. Add the notification check logic
js_logic = """
let consultasDeHoje = [];

function checkNotifications() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const currentTime = `${hours}:${minutes}`;
    
    let hasAlert = false;
    consultasDeHoje.forEach(c => {
        if(c.horario && c.horario.startsWith(currentTime)) {
            // It's exactly the time!
            hasAlert = true;
        }
    });
    
    const dot = document.getElementById('notification-dot');
    if(dot) {
        if(hasAlert) dot.classList.remove('hidden');
        // We could also play a sound or show a toast here
    }
}

// Check every 30 seconds
setInterval(checkNotifications, 30000);
"""

# Insert JS logic
content = content.replace('async function loadAgenda() {', js_logic + '\nasync function loadAgenda() {')

# Modify loadAgenda to store `res.items` globally
pattern_load_agenda = r'const res = await window\.api\.getConsultas\(0, 100, { data: today }\);'
new_load_agenda = r"""const res = await window.api.getConsultas(0, 100, { data: today });
        if(res.items) consultasDeHoje = res.items;
        checkNotifications(); // check immediately"""
content = content.replace(pattern_load_agenda, new_load_agenda)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Notification logic added.")
