import base64
import os

NICKNAME = "the_fost"
DISCORD_TAG = "the_fost"
TELEGRAM_TAG = "fost_official"
DISCORD_ID = "1404770879254167574" 
SONG_NAME = "Серёга Пират - ФП АМ"

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
        body {{ margin: 0; background: #000; color: white; font-family: 'Segoe UI', Tahoma, sans-serif; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; cursor: none; perspective: 1200px; }}
        #canvas {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }}
        #cursor {{ width: 8px; height: 8px; background: white; border-radius: 50%; position: fixed; pointer-events: none; z-index: 9999; transform: translate(-50%, -50%); box-shadow: 0 0 10px white; transition: transform 0.3s ease; }}
        
        .ripple {{ position: fixed; border: 2px solid rgba(255,255,255,0.4); background: rgba(255,255,255,0.05); border-radius: 50%; pointer-events: none; transform: translate(-50%, -50%); animation: ripple-effect 0.6s ease-out forwards; z-index: 9998; }}
        @keyframes ripple-effect {{ from {{ width: 0; height: 0; opacity: 1; }} to {{ width: 120px; height: 120px; opacity: 0; }} }}

        .badge {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.07); padding: 6px 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); font-size: 13px; opacity: 0.9; }}
        #touch-label {{ position: fixed; top: 20px; right: 20px; opacity: 0; transform: translateX(50px); transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 10000; }}
        #touch-label.show {{ opacity: 1; transform: translateX(0); }}
        
        .views-container {{ position: relative; margin-bottom: 50px; cursor: none; }}
        .views-tooltip {{ position: absolute; top: -30px; left: 50%; transform: translateX(-50%); background: #fff; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; opacity: 0; transition: 0.3s; }}
        .views-container:hover .views-tooltip {{ opacity: 1; top: -40px; }}
        
        .avatar-wrapper {{ position: relative; display: inline-block; cursor: pointer; }}
        .avatar-main {{ width: 160px; height: 160px; object-fit: cover; border-radius: 25px; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); animation: pulse 4s infinite ease-in-out; }}
        @keyframes pulse {{ 0%, 100% {{ box-shadow: 0 0 20px rgba(255,255,255,0.05); }} 50% {{ box-shadow: 0 0 40px rgba(255,255,255,0.15); }} }}
        .avatar-main.spring {{ transform: scale(0.8); }}
        
        #nickname {{ font-size: 34px; margin: 10px 0; letter-spacing: 3px; font-weight: 400; min-height: 45px; }}
        .status-box {{ background: rgba(255,255,255,0.03); padding: 8px 15px; border-radius: 12px; margin: 10px auto 25px; font-size: 12px; display: flex; align-items: center; gap: 10px; border: 1px solid rgba(255,255,255,0.05); width: fit-content; }}
        .status-dot {{ width: 10px; height: 10px; border-radius: 50%; background: #43b581; box-shadow: 0 0 10px #43b581; }}
        
        .tilt-container {{ position: relative; z-index: 10; transition: transform 0.1s ease-out, opacity 2s ease; transform-style: preserve-3d; opacity: 0; }}
        .card {{ text-align: center; width: 480px; display: flex; flex-direction: column; align-items: center; }}
        
        .player-bar {{ margin-top: 30px; display: flex; align-items: center; background: rgba(255,255,255,0.03); padding: 10px 20px; border-radius: 18px; width: 100%; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); gap: 15px; box-sizing: border-box; }}
        .player-avatar {{ width: 45px; height: 45px; border-radius: 50%; object-fit: cover; animation: rotate 10s linear infinite; animation-play-state: paused; }}
        .playing .player-avatar {{ animation-play-state: running; }}
        @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
        
        .player-info {{ flex-grow: 1; text-align: left; overflow: hidden; }}
        .progress-container {{ display: flex; align-items: center; gap: 8px; font-size: 10px; opacity: 0.5; margin-top: 5px; }}
        .slider {{ flex-grow: 1; height: 3px; cursor: pointer; accent-color: white; appearance: none; background: rgba(255,255,255,0.1); }}
        
        .links {{ display: flex; gap: 15px; justify-content: center; }}
        .btn {{ text-decoration: none; color: white; background: rgba(255,255,255,0.05); padding: 12px 35px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); transition: 0.4s; font-size: 14px; }}
        
        #toast {{ position: fixed; top: -60px; left: 50%; transform: translateX(-50%); background: rgba(46, 213, 115, 0.95); color: white; padding: 12px 25px; border-radius: 10px; z-index: 9999; transition: 0.5s; opacity: 0; font-weight: bold; font-size: 14px; }}
        #entry-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: transparent; z-index: 8000; display: flex; justify-content: center; align-items: center; transition: 1s; cursor: pointer; }}
        #easter-smile {{ position: fixed; right: -100px; top: 50%; transform: translateY(-50%); font-size: 50px; transition: 0.8s; opacity: 0; color: white; text-shadow: 0 0 20px white; }}
        #easter-smile.active {{ right: 50px; opacity: 1; }}
    </style>
</head>
<body id="body-click">
    <div id="toast"></div><div id="cursor"></div><canvas id="canvas"></canvas>
    <div class="badge" id="touch-label">don't touch me</div>
    <div id="easter-smile">:)</div>
    <div id="entry-screen"><h2>[ CLICK TO ENTER ]</h2></div>

    <div class="tilt-container" id="main-content">
        <div class="card">
            <div class="views-container" onmouseover="playHover()">
                <div class="views-tooltip">VIEWS</div>
                <div class="badge">👁 <span id="visit-count">0</span></div>
            </div>
            <div class="avatar-wrapper" onclick="triggerSpring(event)" onmouseover="playHover()">
                <img src="{AVATAR_DATA}" class="avatar-main" id="main-ava">
            </div>
            <h1 id="nickname" onmouseover="startScramble()" onmouseout="stopScramble()"></h1>
            <div class="status-box"><div class="status-dot"></div><span>ONLINE</span></div>
            <div class="links">
                <a href="#" class="btn" onmouseover="exp()" onmouseout="shr()" onclick="copyTG(event)">Telegram</a>
                <a href="#" class="btn" onmouseover="exp()" onmouseout="shr()" onclick="copyDS(event)">Discord</a>
            </div>
            <div class="player-bar playing" id="playerBar" onmouseover="playHover()">
                <img src="{MUSIC_DATA}" class="player-avatar">
                <div class="player-info">
                    <div style="font-size:12px; opacity:0.8; white-space: nowrap;">{SONG_NAME}</div>
                    <div class="progress-container">
                        <span id="curT">00:00</span>
                        <input type="range" class="slider" id="progress" value="0">
                        <span id="durT">00:00</span>
                    </div>
                </div>
                <div class="player-controls">
                    <span id="playPause" style="cursor:pointer; width:15px;">⏸</span>
                    <input type="range" id="volume" min="0" max="1" step="0.05" value="0.5" style="width: 40px; accent-color: white;">
                </div>
            </div>
        </div>
    </div>

    <audio id="audio" loop src="music.mp3"></audio>
    <audio id="hover-sound" src="hover.mp3"></audio>

    <script>
        const audio = document.getElementById('audio');
        const hSnd = document.getElementById('hover-sound');
        const playBtn = document.getElementById('playPause');
        const nickEl = document.getElementById('nickname');
        const originalName = "{NICKNAME}";
        let mouse = {{ x: 0, y: 0 }}, isStarted = false, trail = [], scrambleInterval;

        window.onblur = () => {{ document.title = "Вернись к fost..."; }};
        window.onfocus = () => {{ document.title = originalName; }};

        function playHover() {{ if(isStarted) {{ hSnd.currentTime = 0; hSnd.volume = 0.2; hSnd.play().catch(()=>{{}}); }} }}

        document.addEventListener('click', (e) => {{
            if (!isStarted) return;
            const ripple = document.createElement('div');
            ripple.className = 'ripple'; ripple.style.left = e.clientX + 'px'; ripple.style.top = e.clientY + 'px';
            document.body.appendChild(ripple); ripple.onanimationend = () => ripple.remove();
        }});

        document.getElementById('body-click').onclick = function() {{
            if (!isStarted) {{
                isStarted = true;
                document.getElementById('entry-screen').style.opacity = '0';
                audio.volume = 0.5; audio.play();
                setTimeout(() => {{
                    document.getElementById('entry-screen').style.display = 'none';
                    document.getElementById('main-content').style.opacity = '1';
                    typeName();
                }}, 1000);
            }}
        }};

        // NICKNAME EFFECTS
        function typeName() {{
            let j = 0; nickEl.innerHTML = "";
            function step() {{ if (j < originalName.length) {{ nickEl.innerHTML += originalName.charAt(j); j++; setTimeout(step, 180); }} }}
            step();
        }}

        const chars = "!@#$%^&*()_+<>?/[]{{}}1234567890";
        function startScramble() {{
            if(nickEl.innerHTML.length < originalName.length) return;
            clearInterval(scrambleInterval);
            scrambleInterval = setInterval(() => {{ nickEl.innerText = originalName.split('').map(() => chars[Math.floor(Math.random()*chars.length)]).join(''); }}, 70);
        }}
        function stopScramble() {{ clearInterval(scrambleInterval); nickEl.innerText = originalName; }}

        // TIMER & PLAYER
        function fmt(s) {{ let m = Math.floor(s/60); s = Math.floor(s%60); return (m<10?'0':'')+m+':'+(s<10?'0':'')+s; }}
        audio.ontimeupdate = () => {{
            if(!isNaN(audio.duration)) {{
                document.getElementById('progress').value = (audio.currentTime / audio.duration)*100;
                document.getElementById('curT').innerText = fmt(audio.currentTime);
                document.getElementById('durT').innerText = fmt(audio.duration);
            }}
        }};
        document.getElementById('progress').oninput = (e) => {{ e.stopPropagation(); audio.currentTime = (e.target.value/100)*audio.duration; }};
        document.getElementById('volume').oninput = (e) => {{ e.stopPropagation(); audio.volume = e.target.value; }};
        playBtn.onclick = (e) => {{
            e.stopPropagation();
            if (audio.paused) {{ audio.play(); playBtn.innerHTML = '⏸'; }} 
            else {{ audio.pause(); playBtn.innerHTML = '▶'; }}
        }};

        // CANVAS ANIMATION
        const canvas = document.getElementById('canvas'); const ctx = canvas.getContext('2d'); let stars = [];
        function init() {{ canvas.width = window.innerWidth; canvas.height = window.innerHeight; stars = []; for (let i = 0; i < 90; i++) stars.push({{ x: Math.random()*canvas.width, y: Math.random()*canvas.height, size: Math.random()*1.8, speed: Math.random()*0.5+0.1, vx: 0, vy: 0 }}); }}
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height); 
            trail.push({{ x: mouse.x, y: mouse.y }}); if (trail.length > 12) trail.shift();
            trail.forEach((t, i) => {{ let opacity = (i / trail.length) * 0.4; let size = (i / trail.length) * 4; ctx.fillStyle = `rgba(255,255,255,${{opacity}})`; ctx.beginPath(); ctx.arc(t.x, t.y, size, 0, Math.PI*2); ctx.fill(); }});
            ctx.fillStyle = 'white';
            stars.forEach((s, idx) => {{
                let dx = s.x - mouse.x; let dy = s.y - mouse.y; let dist = Math.hypot(dx, dy);
                if (dist < 100) {{ let f = (100 - dist) / 100; s.vx += dx/dist*f*2; s.vy += dy/dist*f*2; }}
                s.x += s.vx; s.y += s.vy + s.speed; s.vx *= 0.95; s.vy *= 0.95;
                if (s.y > canvas.height) s.y = 0; if (s.x > canvas.width) s.x = 0; if (s.x < 0) s.x = canvas.width;
                ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, Math.PI*2); ctx.fill();
                for (let j = idx + 1; j < stars.length; j++) {{ let s2 = stars[j]; let d = Math.hypot(s.x - s2.x, s.y - s2.y); if (d < 110) {{ ctx.strokeStyle = `rgba(255,255,255,${{0.2 * (1 - d/110)}})`; ctx.lineWidth = 0.6; ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(s2.x, s2.y); ctx.stroke(); }} }}
            }}); requestAnimationFrame(draw);
        }}
        init(); draw();

        document.addEventListener('mousemove', (e) => {{
            mouse.x = e.clientX; mouse.y = e.clientY;
            document.getElementById('cursor').style.left = e.clientX + 'px'; document.getElementById('cursor').style.top = e.clientY + 'px';
            const rX = (window.innerHeight/2-e.clientY)/25; const rY = (e.clientX-window.innerWidth/2)/25;
            document.getElementById('main-content').style.transform = `rotateX(${{rX}}deg) rotateY(${{rY}}deg)`;
        }});

        function triggerSpring(e) {{ e.stopPropagation(); document.getElementById('main-ava').classList.add('spring'); document.getElementById('touch-label').classList.add('show'); setTimeout(() => {{ document.getElementById('main-ava').classList.remove('spring'); }}, 150); setTimeout(() => {{ document.getElementById('touch-label').classList.remove('show'); }}, 2000); }}
        function showToast(txt) {{ const t = document.getElementById('toast'); t.innerText = txt; t.style.top = '30px'; t.style.opacity = '1'; setTimeout(() => {{ t.style.top = '-60px'; t.style.opacity = '0'; }}, 2500); }}
        function copyTG(e) {{ e.stopPropagation(); navigator.clipboard.writeText("{TELEGRAM_TAG}"); showToast("Ник Telegram скопирован"); }}
        function copyDS(e) {{ e.stopPropagation(); navigator.clipboard.writeText("{DISCORD_TAG}"); showToast("Ник Discord скопирован"); }}
        function exp() {{ playHover(); document.getElementById('cursor').style.transform = 'translate(-50%, -50%) scale(4)'; }}
        function shr() {{ document.getElementById('cursor').style.transform = 'translate(-50%, -50%) scale(1)'; }}
        let keyBuffer = ""; document.addEventListener('keydown', (e) => {{ keyBuffer += e.key.toLowerCase(); if (keyBuffer.length > 4) keyBuffer = keyBuffer.substring(1); if (keyBuffer === "fost") {{ document.getElementById('easter-smile').classList.add('active'); playHover(); setTimeout(() => document.getElementById('easter-smile').classList.remove('active'), 3000); keyBuffer = ""; }} }});
        let count = localStorage.getItem('v_count') || 127; if (!sessionStorage.getItem('v_done')) {{ count++; localStorage.setItem('v_count', count); sessionStorage.setItem('v_done', 't'); }} document.getElementById('visit-count').innerText = count;
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_final)
