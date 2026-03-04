#!/usr/bin/env python3
"""Generate a dynamic Philadelphia skyline SVG based on current weather and time."""

import os
import random
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

WIDTH = 1200
HEIGHT = 300
TIMEZONE = "America/New_York"
LAT = 39.9526
LON = -75.1652

# WMO weather codes → (main category, description)
WMO_CODES = {
    0: ("Clear", "clear sky"),
    1: ("Clear", "mainly clear"),
    2: ("Clouds", "partly cloudy"),
    3: ("Clouds", "overcast"),
    45: ("Fog", "fog"),
    48: ("Fog", "depositing rime fog"),
    51: ("Drizzle", "light drizzle"),
    53: ("Drizzle", "moderate drizzle"),
    55: ("Drizzle", "dense drizzle"),
    56: ("Drizzle", "freezing drizzle"),
    57: ("Drizzle", "dense freezing drizzle"),
    61: ("Rain", "slight rain"),
    63: ("Rain", "moderate rain"),
    65: ("Rain", "heavy rain"),
    66: ("Rain", "freezing rain"),
    67: ("Rain", "heavy freezing rain"),
    71: ("Snow", "slight snow"),
    73: ("Snow", "moderate snow"),
    75: ("Snow", "heavy snow"),
    77: ("Snow", "snow grains"),
    80: ("Rain", "slight rain showers"),
    81: ("Rain", "moderate rain showers"),
    82: ("Rain", "violent rain showers"),
    85: ("Snow", "slight snow showers"),
    86: ("Snow", "heavy snow showers"),
    95: ("Thunderstorm", "thunderstorm"),
    96: ("Thunderstorm", "thunderstorm with slight hail"),
    99: ("Thunderstorm", "thunderstorm with heavy hail"),
}


def get_weather():
    """Fetch current weather from Open-Meteo (free, no API key needed)."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&current=temperature_2m,apparent_temperature,weather_code"
        f"&temperature_unit=fahrenheit"
    )
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()["current"]
    code = data["weather_code"]
    main, desc = WMO_CODES.get(code, ("Clear", "clear sky"))
    return {
        "weather": [{"main": main, "description": desc}],
        "main": {
            "temp": data["temperature_2m"],
            "feels_like": data["apparent_temperature"],
        },
    }


def get_time_period(hour):
    if hour < 5 or hour >= 21:
        return "night"
    elif hour < 7:
        return "dawn"
    elif hour < 10:
        return "morning"
    elif hour < 17:
        return "day"
    elif hour < 19:
        return "sunset"
    else:
        return "dusk"


def darken(hex_color, factor):
    r = int(int(hex_color[1:3], 16) * factor)
    g = int(int(hex_color[3:5], 16) * factor)
    b = int(int(hex_color[5:7], 16) * factor)
    return f"#{min(r,255):02x}{min(g,255):02x}{min(b,255):02x}"


def sky_gradient(period, weather):
    palettes = {
        "night":   [("#050B18", 0), ("#0B1628", 40), ("#162447", 100)],
        "dawn":    [("#1a1a2e", 0), ("#c0392b", 35), ("#f39c12", 70), ("#ffecd2", 100)],
        "morning": [("#2980b9", 0), ("#5dade2", 50), ("#aed6f1", 100)],
        "day":     [("#1a6fc4", 0), ("#4fb4f7", 40), ("#87CEEB", 100)],
        "sunset":  [("#1a1a2e", 0), ("#c0392b", 30), ("#e67e22", 60), ("#fdebd0", 100)],
        "dusk":    [("#0f0c29", 0), ("#302b63", 50), ("#544a7d", 100)],
    }
    colors = palettes.get(period, palettes["day"])
    if weather in ("Rain", "Thunderstorm", "Drizzle"):
        colors = [(darken(c, 0.5), p) for c, p in colors]
    elif weather == "Clouds":
        colors = [(darken(c, 0.75), p) for c, p in colors]
    elif weather == "Snow":
        colors = [(darken(c, 0.7), p) for c, p in colors]
    return colors


def render_stars(period):
    if period not in ("night", "dusk", "dawn"):
        return ""
    random.seed(42)
    count = {"night": 30, "dusk": 18, "dawn": 10}[period]
    base_op = {"night": 0.8, "dusk": 0.5, "dawn": 0.3}[period]
    lines = []
    for i in range(count):
        x = random.randint(20, WIDTH - 20)
        y = random.randint(8, 130)
        r = round(random.uniform(0.5, 1.5), 1)
        cls = f"s{(i % 5) + 1}"
        lines.append(f'  <circle class="{cls}" cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="{base_op}"/>')
    return "\n".join(lines)


def render_clouds(weather):
    if weather != "Clouds":
        return ""
    return """  <g opacity="0.3" class="cloud1">
    <ellipse cx="180" cy="55" rx="55" ry="18" fill="#8B949E"/>
    <ellipse cx="215" cy="48" rx="40" ry="16" fill="#8B949E"/>
    <ellipse cx="155" cy="52" rx="32" ry="14" fill="#8B949E"/>
  </g>
  <g opacity="0.22" class="cloud2">
    <ellipse cx="750" cy="40" rx="48" ry="16" fill="#8B949E"/>
    <ellipse cx="780" cy="34" rx="35" ry="14" fill="#8B949E"/>
    <ellipse cx="725" cy="37" rx="28" ry="12" fill="#8B949E"/>
  </g>
  <g opacity="0.18" class="cloud1">
    <ellipse cx="1020" cy="60" rx="42" ry="14" fill="#8B949E"/>
    <ellipse cx="1045" cy="55" rx="30" ry="12" fill="#8B949E"/>
  </g>"""


def render_rain():
    random.seed(789)
    lines = []
    for _ in range(40):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        length = random.randint(10, 22)
        delay = round(random.uniform(0, 1.5), 2)
        op = round(random.uniform(0.2, 0.5), 2)
        lines.append(
            f'  <line x1="{x}" y1="{y}" x2="{x - 3}" y2="{y + length}" '
            f'stroke="#58A6FF" stroke-width="1" opacity="{op}">'
            f'<animate attributeName="y1" from="-20" to="{HEIGHT}" dur="1s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" from="{-20 + length}" to="{HEIGHT + length}" dur="1s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</line>'
        )
    return "\n".join(lines)


def render_snow():
    random.seed(101)
    lines = []
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = round(random.uniform(1, 3), 1)
        delay = round(random.uniform(0, 3), 2)
        drift = random.randint(-15, 15)
        lines.append(
            f'  <circle cx="{x}" cy="{y}" r="{r}" fill="white" opacity="0.6">'
            f'<animate attributeName="cy" from="-10" to="{HEIGHT + 10}" dur="4s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{x};{x + drift};{x}" dur="4s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "\n".join(lines)


def render_sun_moon(period):
    if period == "day" or period == "morning":
        return (
            '  <circle cx="950" cy="60" r="30" fill="#f9d71c" opacity="0.9"/>\n'
            '  <circle cx="950" cy="60" r="36" fill="#f9d71c" opacity="0.15"/>'
        )
    elif period == "night":
        return (
            '  <circle cx="980" cy="50" r="18" fill="#e8e8e8" opacity="0.85"/>\n'
            '  <circle cx="972" cy="44" r="16" fill="url(#sky)" opacity="0.8"/>'
        )
    elif period in ("sunset", "dawn"):
        color = "#f5a623" if period == "dawn" else "#e74c3c"
        return (
            f'  <circle cx="600" cy="260" r="35" fill="{color}" opacity="0.7"/>\n'
            f'  <circle cx="600" cy="260" r="50" fill="{color}" opacity="0.12"/>'
        )
    return ""


SKYLINE = """  <rect x="0" y="242" width="40" height="58" fill="#0D1117"/>
  <rect x="45" y="252" width="30" height="48" fill="#0D1117"/>
  <rect x="80" y="238" width="35" height="62" fill="#0D1117"/>
  <rect x="120" y="248" width="25" height="52" fill="#0D1117"/>
  <rect x="155" y="212" width="28" height="88" fill="#0D1117"/>
  <rect x="150" y="210" width="38" height="4" fill="#0D1117"/>
  <rect x="200" y="218" width="35" height="82" fill="#0D1117"/>
  <ellipse cx="217" cy="218" rx="17.5" ry="7" fill="#0D1117"/>
  <rect x="248" y="258" width="55" height="42" fill="#0D1117"/>
  <rect x="252" y="254" width="47" height="6" fill="#0D1117"/>
  <rect x="315" y="242" width="25" height="58" fill="#0D1117"/>
  <rect x="345" y="232" width="30" height="68" fill="#0D1117"/>
  <rect x="390" y="178" width="30" height="122" fill="#0D1117"/>
  <rect x="385" y="175" width="40" height="5" fill="#0D1117"/>
  <rect x="403" y="168" width="4" height="9" fill="#0D1117"/>
  <rect x="440" y="192" width="32" height="108" fill="#0D1117"/>
  <polygon points="456,192 440,212 472,212" fill="#0D1117"/>
  <rect x="454" y="178" width="4" height="16" fill="#0D1117"/>
  <rect x="482" y="202" width="28" height="98" fill="#0D1117"/>
  <polygon points="496,202 482,218 510,218" fill="#0D1117"/>
  <rect x="494" y="192" width="4" height="12" fill="#0D1117"/>
  <rect x="518" y="235" width="22" height="65" fill="#0D1117"/>
  <rect x="546" y="228" width="20" height="72" fill="#0D1117"/>
  <rect x="578" y="222" width="50" height="78" fill="#0D1117"/>
  <rect x="593" y="202" width="20" height="24" fill="#0D1117"/>
  <rect x="600" y="188" width="6" height="16" fill="#0D1117"/>
  <rect x="602" y="182" width="2" height="8" fill="#0D1117"/>
  <rect x="642" y="198" width="30" height="102" fill="#0D1117"/>
  <rect x="637" y="195" width="40" height="5" fill="#0D1117"/>
  <rect x="688" y="212" width="28" height="88" fill="#0D1117"/>
  <rect x="724" y="238" width="22" height="62" fill="#0D1117"/>
  <rect x="752" y="228" width="30" height="72" fill="#0D1117"/>
  <rect x="790" y="242" width="25" height="58" fill="#0D1117"/>
  <rect x="822" y="235" width="32" height="65" fill="#0D1117"/>
  <rect x="862" y="248" width="28" height="52" fill="#0D1117"/>
  <rect x="898" y="238" width="22" height="62" fill="#0D1117"/>
  <rect x="928" y="252" width="35" height="48" fill="#0D1117"/>
  <rect x="970" y="245" width="25" height="55" fill="#0D1117"/>
  <rect x="1002" y="258" width="28" height="42" fill="#0D1117"/>
  <rect x="1038" y="252" width="20" height="48" fill="#0D1117"/>
  <rect x="1068" y="262" width="35" height="38" fill="#0D1117"/>
  <rect x="1110" y="258" width="28" height="42" fill="#0D1117"/>
  <rect x="1145" y="265" width="25" height="35" fill="#0D1117"/>
  <rect x="1175" y="268" width="25" height="32" fill="#0D1117"/>
  <rect x="0" y="298" width="1200" height="2" fill="#0D1117"/>"""


def render_windows(period):
    color = "#58A6FF" if period in ("night", "dusk", "dawn") else "#ffffff"
    op_base = 0.5 if period in ("night", "dusk", "dawn") else 0.15
    positions = [
        (398, 188, "w1"), (406, 200, "w2"), (398, 215, "w3"), (410, 228, "w1"),
        (398, 245, "w2"), (406, 260, "w3"), (402, 275, "w1"),
        (449, 222, "w2"), (459, 238, "w3"), (451, 255, "w1"), (462, 270, "w2"),
        (490, 228, "w3"), (500, 245, "w1"), (492, 265, "w2"),
        (588, 242, "w1"), (602, 238, "w3"), (612, 252, "w2"), (596, 262, "w1"),
        (650, 212, "w2"), (660, 232, "w3"), (652, 255, "w1"), (662, 270, "w2"),
        (696, 228, "w3"), (704, 248, "w1"), (698, 268, "w2"),
        (92, 258, "w1"), (165, 235, "w3"), (212, 242, "w2"), (352, 252, "w1"),
        (532, 252, "w3"), (738, 258, "w2"), (762, 248, "w1"), (835, 255, "w3"),
        (875, 268, "w2"), (942, 268, "w1"),
    ]
    lines = []
    for x, y, cls in positions:
        s = 3 if x < 720 else 2
        op = round(op_base + random.uniform(-0.1, 0.2), 2)
        lines.append(
            f'  <rect class="{cls}" x="{x}" y="{y}" width="{s}" height="{s}" '
            f'rx="0.5" fill="{color}" opacity="{max(0.1, op)}"/>'
        )
    return "\n".join(lines)


def generate_svg(weather_data, now):
    hour = now.hour
    period = get_time_period(hour)
    weather_main = weather_data["weather"][0]["main"]
    weather_desc = weather_data["weather"][0]["description"]
    temp = round(weather_data["main"]["temp"])
    feels = round(weather_data["main"]["feels_like"])

    colors = sky_gradient(period, weather_main)
    gradient_stops = "\n".join(
        f'      <stop offset="{pct}%" stop-color="{c}"/>' for c, pct in colors
    )

    weather_fx = ""
    if weather_main in ("Rain", "Drizzle", "Thunderstorm"):
        weather_fx = render_rain()
    elif weather_main == "Snow":
        weather_fx = render_snow()

    clouds = render_clouds(weather_main)
    stars = render_stars(period)
    sun_moon = render_sun_moon(period)

    random.seed(42)
    windows = render_windows(period)

    time_str = now.strftime("%-I:%M %p")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <linearGradient id="sky" x1="0%" y1="0%" x2="0%" y2="100%">
{gradient_stops}
    </linearGradient>
    <linearGradient id="cityGlow" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#58A6FF" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#58A6FF" stop-opacity="0"/>
    </linearGradient>
    <style>
      @keyframes twinkle1 {{ 0%,100% {{ opacity: 0.2; }} 50% {{ opacity: 1; }} }}
      @keyframes twinkle2 {{ 0%,100% {{ opacity: 0.5; }} 50% {{ opacity: 0.9; }} }}
      @keyframes twinkle3 {{ 0%,100% {{ opacity: 0.1; }} 50% {{ opacity: 0.8; }} }}
      @keyframes windowGlow {{ 0%,100% {{ opacity: 0.25; }} 50% {{ opacity: 0.8; }} }}
      @keyframes cloudDrift {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(30px); }} }}
      @keyframes fadeIn {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
      .s1 {{ animation: twinkle1 3s ease-in-out infinite; }}
      .s2 {{ animation: twinkle2 2.5s ease-in-out infinite 0.8s; }}
      .s3 {{ animation: twinkle3 4s ease-in-out infinite 1.5s; }}
      .s4 {{ animation: twinkle1 3.5s ease-in-out infinite 2s; }}
      .s5 {{ animation: twinkle2 2s ease-in-out infinite 0.3s; }}
      .w1 {{ animation: windowGlow 4s ease-in-out infinite; }}
      .w2 {{ animation: windowGlow 3s ease-in-out infinite 1s; }}
      .w3 {{ animation: windowGlow 5s ease-in-out infinite 2s; }}
      .cloud1 {{ animation: cloudDrift 20s ease-in-out infinite alternate; }}
      .cloud2 {{ animation: cloudDrift 25s ease-in-out infinite alternate-reverse; }}
      .name-text {{
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 52px; font-weight: 700; fill: #FFFFFF;
        animation: fadeIn 2s ease-in;
      }}
      .sub-text {{
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 13px; font-weight: 400; fill: #58A6FF;
        letter-spacing: 5px; animation: fadeIn 3s ease-in;
      }}
      .weather-text {{
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 11px; fill: #8B949E; letter-spacing: 1px;
      }}
    </style>
  </defs>

  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)"/>
  <ellipse cx="600" cy="300" rx="550" ry="80" fill="url(#cityGlow)"/>

{sun_moon}
{stars}
{clouds}
{weather_fx}

  <text class="name-text" x="600" y="120" text-anchor="middle">Zakir Jiwani</text>
  <text class="sub-text" x="600" y="148" text-anchor="middle">PHILADELPHIA, PA</text>
  <text class="weather-text" x="1175" y="18" text-anchor="end">{temp}F / {weather_desc.title()}</text>
  <text class="weather-text" x="1175" y="32" text-anchor="end">{time_str} ET</text>

{SKYLINE}
{windows}
</svg>"""


def main():
    weather = get_weather()
    now = datetime.now(ZoneInfo(TIMEZONE))
    svg = generate_svg(weather, now)

    out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "banner.svg")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(svg)

    print(f"Generated banner: {now.strftime('%Y-%m-%d %I:%M %p')} ET")
    print(f"Weather: {weather['weather'][0]['description']}, {round(weather['main']['temp'])}F")
    print(f"Period: {get_time_period(now.hour)}")


if __name__ == "__main__":
    main()
