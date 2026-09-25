import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add id="hero-weather"
weather_pattern = r'<div class="flex items-center gap-2 mt-1">'
weather_new = r'<div class="flex items-center gap-2 mt-1" id="hero-weather">'
content = content.replace(weather_pattern, weather_new)

# Add logic to JS block
js_insertion = """
function renderHeroDateAndWeather() {
    const today = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    let dateStr = today.toLocaleDateString('pt-BR', options);
    dateStr = dateStr.charAt(0).toUpperCase() + dateStr.slice(1);
    
    const heroDate = document.getElementById('hero-date');
    if (heroDate) heroDate.innerText = dateStr;
    
    // Fetch Weather (São Paulo coordinates as default for Brazil)
    fetch('https://api.open-meteo.com/v1/forecast?latitude=-23.5505&longitude=-46.6333&current_weather=true')
        .then(r => r.json())
        .then(data => {
            const temp = Math.round(data.current_weather.temperature);
            const code = data.current_weather.weathercode;
            
            let condition = "Céu limpo";
            let icon = "ph-sun text-yellow-400";
            if (code >= 1 && code <= 3) { condition = "Parcialmente nublado"; icon = "ph-cloud-sun text-slate-300"; }
            if (code >= 45 && code <= 48) { condition = "Nevoeiro"; icon = "ph-cloud text-slate-400"; }
            if (code >= 51 && code <= 67) { condition = "Chuva"; icon = "ph-cloud-rain text-blue-400"; }
            if (code >= 80 && code <= 82) { condition = "Pancadas de chuva"; icon = "ph-cloud-showers text-blue-500"; }
            if (code >= 95) { condition = "Tempestade"; icon = "ph-cloud-lightning text-purple-500"; }
            
            const weatherEl = document.getElementById('hero-weather');
            if(weatherEl) {
                weatherEl.innerHTML = `<i class="ph-fill ${icon} text-xl"></i>
                    <span class="text-white font-bold">${temp}°C</span>
                    <span class="text-xs text-slate-300">${condition}</span>`;
            }
        })
        .catch(e => console.error("Weather error:", e));
}
"""

# Insert into <script> block before renderCalendar
content = content.replace('<script>\nfunction renderCalendar', '<script>\n' + js_insertion + '\nfunction renderCalendar')

# Call renderHeroDateAndWeather() inside DOMContentLoaded
content = content.replace("renderCalendar();", "renderHeroDateAndWeather();\n    renderCalendar();")

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Hero date and weather updated.")
