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

    # Completely modernized UI layout while preserving feature parity and f-string safety
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vehicle Telemetry Matrix</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #0b0f19; 
            --bg-card: #131c2e; 
            --bg-input: #1b263b;
            --border: rgba(255, 255, 255, 0.06);
            --border-hover: rgba(255, 255, 255, 0.12);
            --text-main: #f3f4f6; 
            --text-muted: #6b7280; 
            --text-secondary: #9ca3af;
            
            /* Modernized dynamic glow accents */
            --accent-wild: #f43f5e;
            --accent-unapologetic: #f59e0b; 
            --accent-alive: #10b981;
            --accent-calm: #3b82f6; 
            --accent-dead: #ef4444;
        }}
        
        body {{ 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: var(--bg-main); 
            color: var(--text-main); 
            padding: 3rem 2rem; 
            margin: 0;
            letter-spacing: -0.01em;
        }}
        
        .container {{ max-width: 1300px; margin: 0 auto; }}
        
        header {{ 
            margin-bottom: 2.5rem; 
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}
        
        h1 {{ 
            margin: 0; 
            font-size: 2.25rem; 
            font-weight: 700;
            letter-spacing: -0.03em;
            background: linear-gradient(to right, #ffffff, #9ca3af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        p.subtitle {{ color: var(--text-secondary); margin: 0; font-size: 0.95rem; }}
        
        .controls {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); 
            gap: 1.25rem; 
            background: linear-gradient(145deg, #111827, #131c2e);
            padding: 1.5rem; 
            border-radius: 12px; 
            border: 1px solid var(--border); 
            margin-bottom: 2.5rem; 
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .control-group {{ display: flex; flex-direction: column; gap: 0.5rem; }}
        
        label {{ 
            font-size: 0.75rem; 
            color: var(--text-secondary); 
            text-transform: uppercase; 
            font-weight: 600;
            letter-spacing: 0.05em;
        }}
        
        select, input {{ 
            background-color: var(--bg-input); 
            border: 1px solid var(--border); 
            color: var(--text-main); 
            padding: 0.75rem 1rem; 
            border-radius: 8px; 
            outline: none; 
            font-family: inherit;
            font-size: 0.9rem;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        
        select:focus, input:focus {{
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05);
        }}
        
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); 
            gap: 1.5rem; 
        }}
        
        .card {{ 
            background-color: var(--bg-card); 
            border: 1px solid var(--border); 
            border-radius: 14px; 
            padding: 1.75rem; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .card:hover {{
            transform: translateY(-2px);
            border-color: var(--border-hover);
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        }}
        
        .card-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start; 
            margin-bottom: 1.5rem; 
            gap: 1rem;
        }}
        
        .bike-name {{ 
            font-size: 1.25rem; 
            font-weight: 600; 
            margin: 0; 
            letter-spacing: -0.02em;
            line-height: 1.3;
        }}
        
        .badge {{ 
            font-size: 0.7rem; 
            font-weight: 700; 
            padding: 0.35rem 0.75rem; 
            border-radius: 6px; 
            text-transform: uppercase; 
            letter-spacing: 0.05em;
            white-space: nowrap;
        }}
        
        .badge-dead {{ background-color: rgba(239, 68, 68, 0.12); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }}
        .badge-calm {{ background-color: rgba(59, 130, 246, 0.12); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }}
        .badge-alive {{ background-color: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }}
        .badge-unapologetic {{ background-color: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.2); }}
        .badge-wild {{ background-color: rgba(236, 72, 153, 0.12); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.2); }}
        
        .specs {{ 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 1rem; 
            font-size: 0.9rem; 
            margin-bottom: 1.5rem; 
            border-top: 1px solid var(--border); 
            border-bottom: 1px solid var(--border); 
            padding: 1.25rem 0; 
        }}
        
        .spec-item {{ display: flex; flex-direction: column; gap: 0.25rem; }}
        .spec-label {{ color: var(--text-muted); font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.02em; }}
        .spec-val {{ font-weight: 600; color: #ffffff; font-size: 1.05rem; }}
        
        .profile-footer {{ 
            font-size: 0.8rem; 
            color: var(--text-secondary); 
            font-family: 'JetBrains Mono', monospace; 
            background: rgba(0, 0, 0, 0.25); 
            padding: 0.75rem; 
            border-radius: 6px; 
            border: 1px solid rgba(255, 255, 255, 0.03);
            text-align: left;
            line-height: 1.4;
        }}
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
            grid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 4rem 0; font-size: 0.95rem;">No machines matched the filtering metrics.</p>`;
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
    build_html_dashboard(r'bikes_analyzed.csv', r'index.html')