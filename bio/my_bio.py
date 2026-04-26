import base64
import os

NICKNAME = "the_fost"
DISCORD_TAG = "the_fost"
TELEGRAM_LINK = "https://t.me"
SONG_NAME = "Серёга Пират - ФП АМ"

# Функция для безопасной загрузки картинок в код
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    return ""

AVATAR_DATA = get_base64("avatar.jpg")
MUSIC_DATA = get_base64("music_cover.jpg")

html_final = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{NICKNAME}</title>
    <style>
        body {{ 
            margin: 0; background: #000; color: white; font-family: 'Segoe UI', sans-serif; 
            overflow: hidden; display: flex; justify-content: center; align-items: center; 
            height: 100vh; cursor: none; perspective: 1200px; 
        }}
        #canvas {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }}
        #cursor {{ 
            width: 8px; height: 8px; background: white; border-radius: 50%; 
            position: fixed; pointer-events: none; z-index: 5000; 
            transform: translate(-50%, -50%); box-shadow: 0 0 10px white;
            transition: transform 0.3s ease; 
        }}
        #entry-screen {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 4000; display: flex; justify-content: center; align-items: center;
            transition: opacity 1.2s ease;
        }}
        #entry-screen h2 {{ letter-spacing: 8px; opacity: 0.5; animation: blink 2s infinite; font-weight: 300; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 0.1; }} 50% {{ opacity: 0.6; }} }}
        
        .tilt-container {{
            position: relative; z-index: 10;
            transition: transform 0.2s cubic-bezier(0.03, 0.98, 0.52, 0.99);
            transform-style: preserve-3d;
            opacity: 0; transform: scale(0.95);
            padding: 150px; 
        }}
        .card {{ text-align: center; width: 450px; pointer-events: auto; }}
        .avatar-main {{ width: 150px; height: 150px; object-fit: cover; border-radius: 20px; margin-bottom: 10px; }}
        h1 {{ font-size: 32px; margin: 10px 0; letter-spacing: 2px; font-weight: 400; }}
        
        .player-bar {{
            margin-top: 40px; display: flex; align-items: center; background: rgba(255,255,255,0.03); 
            padding: 10px 20px; border-radius: 15px; width: 100%; backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.05); gap: 15px; box-sizing: border-box;
        }}
        .player-avatar {{ width: 45px; height: 45px; border-radius: 8px; object-fit: cover; }}
        .player-info {{ flex-grow: 1; text-align: left; }}
        .song-title {{ font-size: 13px; margin-bottom: 5px; opacity: 0.9; letter-spacing: 0.5px; }}
        .progress-container {{ display: flex; align-items: center; gap: 10px; font-size: 10px; opacity: 0.6; }}
        .slider {{ flex-grow: 1; height: 3px; cursor: pointer; accent-color: white; appearance: none; background: rgba(255,255,255,0.1); border-radius: 2px; }}
        .slider::-webkit-slider-thumb {{ appearance: none; width: 8px; height: 8px; background: white; border-radius: 50%; }}
        .player-controls {{ display: flex; align-items: center; gap: 15px; }}
        .ctrl-btn {{ cursor: pointer; font-size: 18px; opacity: 0.8; transition: 0.3s; width: 20px; text-align: center; }}
        
        .links {{ display: flex; gap: 15px; justify-content: center; }}
        .btn {{ text-decoration: none; color: white; background: rgba(255,255,255,0.05); padding: 12px 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); transition: 0.4s; font-size: 13px; }}
        .btn:hover {{ background: rgba(255,255,255,0.1); }}

        #toast {{ position: fixed; top: -60px; left: 50%; transform: translateX(-50%); background: rgba(46, 213, 115, 0.95); padding: 12px 25px; border-radius: 10px; z-index: 6000; transition: 0.5s; opacity: 0; }}
    </style>
</head>
<body id="body-click">
    <div id="toast">Ник скопирован</div>
    <div id="cursor"></div>
    <canvas id="canvas"></canvas>
    <div id="entry-screen"><h2>[ CLICK TO ENTER ]</h2></div>

    <div class="tilt-container" id="main-content">
        <div class="card">
            <img src="{AVATAR_DATA}" class="avatar-main">
            <h1 id="nickname"></h1>
            <div class="links">
                <a href="{TELEGRAM_LINK}" target="_blank" class="btn" onmouseover="exp()" onmouseout="shr()">Telegram</a>
                <a href="#" class="btn" onmouseover="exp()" onmouseout="shr()" onclick="copy(event)">Discord</a>
            </div>
            <div class="player-bar" onmouseover="exp()" onmouseout="shr()">
                <img src="{MUSIC_DATA}" class="player-avatar">
                <div class="player-info">
                    <div class="song-title">🌀 {SONG_NAME}</div>
                    <div class="progress-container">
                        <span id="curT">00:00</span>
                        <input type="range" class="slider" id="progress" value="0">
                        <span id="durT">00:00</span>
                    </div>
                </div>
                <div class="player-controls">
                    <span class="ctrl-btn" id="playPause">⏸</span>
                    <input type="range" id="volume" min="0" max="1" step="0.05" value="0.5" style="width: 50px; accent-color: white;">
                </div>
            </div>
        </div>
    </div>

    <audio id="audio" loop><source src="music.mp3" type="audio/mpeg"></audio>

    <script>
        const audio = document.getElementById('audio');
        const container = document.getElementById('main-content');
        const entry = document.getElementById('entry-screen');
        const playBtn = document.getElementById('playPause');
        let isStarted = false;

        document.getElementById('body-click').onclick = function() {{
            if (!isStarted) {{
                isStarted = true;
                entry.style.opacity = '0';
                setTimeout(() => {{
                    entry.style.display = 'none';
                    container.style.opacity = '1';
                    audio.play();
                    typeName();
                }}, 1000);
            }}
        }};

        playBtn.onclick = function(e) {{
            e.stopPropagation();
            if (audio.paused) {{ audio.play(); playBtn.innerHTML = '⏸'; }} 
            else {{ audio.pause(); playBtn.innerHTML = '▶'; }}
        }};

        document.addEventListener('mousemove', (e) => {{
            const cursor = document.getElementById('cursor');
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;
            const rotateX = (centerY - e.clientY) / 15;
            const rotateY = (e.clientX - centerX) / 15;
            container.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
        }});

        const progress = document.getElementById('progress');
        audio.ontimeupdate = () => {{
            if(!isNaN(audio.duration)) {{
                progress.value = (audio.currentTime / audio.duration) * 100;
                document.getElementById('curT').innerHTML = fmt(audio.currentTime);
                document.getElementById('durT').innerHTML = fmt(audio.duration);
            }}
        }};
        function fmt(s) {{
            let m = Math.floor(s/60); s = Math.floor(s%60);
            return (m<10?'0':'')+m+':'+(s<10?'0':'')+s;
        }}
        progress.oninput = (e) => {{ e.stopPropagation(); audio.currentTime = (progress.value/100) * audio.duration; }};
        document.getElementById('volume').oninput = (e) => {{ e.stopPropagation(); audio.volume = e.target.value; }};

        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let stars = [];
        function init() {{
            canvas.width = window.innerWidth; canvas.height = window.innerHeight;
            stars = [];
            for (let i = 0; i < 180; i++) stars.push({{ x: Math.random()*canvas.width, y: Math.random()*canvas.height, size: Math.random()*1.8, speed: Math.random()*0.6+0.2 }});
        }}
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = 'white';
            stars.forEach(s => {{
                ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, Math.PI*2); ctx.fill();
                s.y -= s.speed; if (s.y < 0) s.y = canvas.height;
            }});
            requestAnimationFrame(draw);
        }}
        init(); draw();
        
        function exp() {{ document.getElementById('cursor').style.transform = 'translate(-50%, -50%) scale(4)'; }}
        function shr() {{ document.getElementById('cursor').style.transform = 'translate(-50%, -50%) scale(1)'; }}

        const nameText = "{NICKNAME}"; let j = 0;
        function typeName() {{
            if (j < nameText.length) {{
                document.getElementById("nickname").innerHTML += nameText.charAt(j);
                j++; setTimeout(typeName, 180);
            }}
        }}
        function copy(e) {{
            e.stopPropagation();
            navigator.clipboard.writeText("{DISCORD_TAG}");
            const t = document.getElementById('toast'); t.style.top = '30px'; t.style.opacity = '1';
            setTimeout(() => {{ t.style.top = '-60px'; t.style.opacity = '0'; }}, 2500);
        }}
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("✅ ФИНАЛ: ТГ рабочий, плеер с обложкой, 3D тилт настроен. Запускай!")



