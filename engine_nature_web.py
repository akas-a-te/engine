import csv
import json
import os

def build_html_dashboard(input_csv="bikes_analyzed.csv", output_html="index.html"):
    if not os.path.exists(input_csv):
        print(f"Error: Target data source '{input_csv}' not found.")
        return

    print(f"Reading telemetry from '{input_csv}'...")
    bikes_list = []

    with open(input_csv, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                bikes_list.append({
                    "name": row["bike_name"],
                    "hp": float(row["power_hp"]),
                    "torque": float(row["torque_nm"]),
                    "weight": float(row["weight_kg"]),
                    "norm_torque": float(row["norm_torque"]),
                    "feel": row["energy_feel"],
                    "motion": row["movement_motion"],
                    "profile": row["full_profile"]
                })
            except (KeyError, ValueError):
                continue

    json_data = json.dumps(bikes_list, indent=4)

    # All CSS and JS braces have been doubled up to escape the f-string engine safely
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vehicle Telemetry Matrix</title>
    <style>
        :root {{
            --bg-main: #0f172a; --bg-card: #1e293b; --border: #334155;
            --text-main: #f8fafc; --text-muted: #94a3b8; --accent-wild: #ec4899;
            --accent-unapologetic: #f59e0b; --accent-alive: #10b981;
            --accent-calm: #3b82f6; --accent-dead: #ef4444;
        }}
        body {{ font-family: -apple-system, sans-serif; background-color: var(--bg-main); color: var(--text-main); padding: 2rem; margin: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{ margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem; }}
        h1 {{ margin: 0 0 0.5rem 0; font-size: 2rem; letter-spacing: -0.05em; }}
        p.subtitle {{ color: var(--text-muted); margin: 0; }}
        .controls {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; background-color: var(--bg-card); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 2rem; }}
        .control-group {{ display: flex; flex-direction: column; gap: 0.5rem; }}
        label {{ font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; }}
        select, input {{ background-color: var(--bg-main); border: 1px solid var(--border); color: var(--text-main); padding: 0.6rem; border-radius: 6px; outline: none; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; }}
        .card {{ background-color: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; }}
        .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }}
        .bike-name {{ font-size: 1.2rem; font-weight: 700; margin: 0; }}
        .badge {{ font-size: 0.75rem; font-weight: bold; padding: 0.25rem 0.6rem; border-radius: 4px; text-transform: uppercase; }}
        .badge-dead {{ background-color: rgba(239, 68, 68, 0.2); color: #f87171; }}
        .badge-calm {{ background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; }}
        .badge-alive {{ background-color: rgba(16, 185, 129, 0.2); color: #34d399; }}
        .badge-unapologetic {{ background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; }}
        .badge-wild {{ background-color: rgba(236, 72, 153, 0.2); color: #f472b6; }}
        .specs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.9rem; margin-bottom: 1rem; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 0.75rem 0; }}
        .spec-item {{ display: flex; flex-direction: column; }}
        .spec-label {{ color: var(--text-muted); font-size: 0.75rem; }}
        .spec-val {{ font-weight: 600; }}
        .profile-footer {{ font-size: 0.75rem; color: var(--text-muted); font-family: monospace; background: rgba(0,0,0,0.2); padding: 0.5rem; border-radius: 4px; text-align: center; }}
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>Vehicle Telemetry Matrix</h1>
        <p class="subtitle">System compiled UI displaying processed machine characteristics.</p>
    </header>
    <div class="controls">
        <div class="control-group">
            <label for="search">Search Vehicle</label>
            <input type="text" id="search" placeholder="Type vehicle name...">
        </div>
        <div class="control-group">
            <label for="feelFilter">Energy Feel</label>
            <select id="feelFilter">
                <option value="ALL">All Energy Levels</option>
                <option value="Dead">Dead</option>
                <option value="Calm">Calm</option>
                <option value="Alive">Alive</option>
                <option value="Unapologetic">Unapologetic</option>
                <option value="Wild">Wild</option>
            </select>
        </div>
        <div class="control-group">
            <label for="motionFilter">Movement Motion</label>
            <select id="motionFilter">
                <option value="ALL">All Motions</option>
                <option value="Shrinked">Shrinked</option>
                <option value="Open-Hearted">Open-Hearted</option>
                <option value="Steady">Steady</option>
                <option value="Electric">Electric</option>
                <option value="Chaotic">Chaotic</option>
            </select>
        </div>
    </div>
    <div class="grid" id="matrixGrid"></div>
</div>
<script>
    const dataset = {json_data};

    const grid = document.getElementById('matrixGrid');
    const searchInput = document.getElementById('search');
    const feelFilter = document.getElementById('feelFilter');
    const motionFilter = document.getElementById('motionFilter');

    function displayCards(data) {{
        grid.innerHTML = '';
        if(data.length === 0) {{
            grid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No machines found.</p>`;
            return;
        }}
        data.forEach(bike => {{
            const card = document.createElement('div');
            card.className = 'card';
            const badgeClass = `badge badge-${{bike.feel.toLowerCase()}}`;
            card.innerHTML = `
                <div>
                    <div class="card-header">
                        <h3 class="bike-name">${{bike.name}}</h3>
                        <span class="${{badgeClass}}">${{bike.feel}}</span>
                    </div>
                    <div class="specs">
                        <div class="spec-item"><span class="spec-label">Power</span><span class="spec-val">${{bike.hp}} HP</span></div>
                        <div class="spec-item"><span class="spec-label">Torque</span><span class="spec-val">${{bike.torque}} Nm</span></div>
                        <div class="spec-item"><span class="spec-label">Weight</span><span class="spec-val">${{bike.weight}} kg</span></div>
                        <div class="spec-item"><span class="spec-label">Norm. Torque</span><span class="spec-val">${{parseFloat(bike.norm_torque).toFixed(1)}} Nm/t</span></div>
                    </div>
                </div>
                <div class="profile-footer">${{bike.profile}}</div>
            `;
            grid.appendChild(card);
        }});
    }}

    function filterData() {{
        const query = searchInput.value.toLowerCase();
        const feel = feelFilter.value;
        const motion = motionFilter.value;
        const filtered = dataset.filter(bike => {{
            return bike.name.toLowerCase().includes(query) && 
                   (feel === 'ALL' || bike.feel === feel) && 
                   (motion === 'ALL' || bike.motion === motion);
        }});
        displayCards(filtered);
    }}

    searchInput.addEventListener('input', filterData);
    feelFilter.addEventListener('change', filterData);
    motionFilter.addEventListener('change', filterData);
    displayCards(dataset);
</script>
</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as outfile:
        outfile.write(html_template)
    
    print(f"Success! Dashboard pipeline rendered fully into '{output_html}'.")

if __name__ == "__main__":
    build_html_dashboard(r'bikes_analyzed.csv',r'index.html')
