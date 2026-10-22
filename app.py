<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Neon Blaster — Game bắn súng 2D</title>
<style>
  *{box-sizing:border-box} body{margin:0;background:#070b18;color:#eef4ff;font-family:system-ui,Segoe UI,Arial,sans-serif;display:grid;place-items:center;min-height:100vh}
  .wrap{width:min(960px,96vw)} header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin:12px 0}
  h1{font-size:clamp(20px,4vw,30px);margin:0;letter-spacing:1px;color:#71f6ff}.stats{display:flex;gap:10px;flex-wrap:wrap}
  .pill{background:#111a31;border:1px solid #26385f;padding:8px 12px;border-radius:12px;font-weight:700}
  canvas{display:block;width:100%;height:auto;border:1px solid #293c68;border-radius:16px;background:#080e22;box-shadow:0 0 35px #00d9ff17;touch-action:none}
  .help{color:#aab8d8;font-size:14px;line-height:1.6;margin:10px 2px}.btn{border:0;border-radius:10px;padding:9px 14px;background:#68efff;color:#06101e;font-weight:800;cursor:pointer}
</style>
</head>
<body>
<div class="wrap">
<header><h1>⚡ NEON BLASTER</h1><div class="stats"><div class="pill">Điểm: <span id="score">0</span></div><div class="pill">Máu: <span id="hp">100</span> ❤️</div><button class="btn" id="restart">Chơi lại</button></div></header>
<canvas id="game" width="900" height="560" aria-label="Game bắn súng 2D"></canvas>
<div class="help"><b>Điều khiển:</b> WASD hoặc phím mũi tên để di chuyển · Di chuột để ngắm · Giữ chuột trái hoặc phím Space để bắn. Trên điện thoại: chạm bên trái để di chuyển, chạm bên phải để ngắm và bắn. Sống sót càng lâu, điểm càng cao!</div>
</div>
<script>
(() => {
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
const scoreEl=document.getElementById('score'),hpEl=document.getElementById('hp');
const W=canvas.width,H=canvas.height;
let keys={},mouse={x:W/2,y:H/2,down:false},player,bullets,enemies,particles,score,hp,spawnTimer,lastTime,gameOver;
function reset(){player={x:W/2,y:H/2,r:14,speed:250,angle:0,cooldown:0};bullets=[];enemies=[];particles=[];score=0;hp=100;spawnTimer=0;lastTime=0;gameOver=false;scoreEl.textContent=score;hpEl.textContent=hp;}
function pointer(e){const r=canvas.getBoundingClientRect();return{x:(e.clientX-r.left)*W/r.width,y:(e.clientY-r.top)*H/r.height};}
canvas.addEventListener('pointermove',e=>{const p=pointer(e);mouse.x=p.x;mouse.y=p.y;});
canvas.addEventListener('pointerdown',e=>{const p=pointer(e);mouse.x=p.x;mouse.y=p.y;mouse.down=true;canvas.setPointerCapture?.(e.pointerId);});
canvas.addEventListener('pointerup',()=>mouse.down=false);canvas.addEventListener('pointercancel',()=>mouse.down=false);
window.addEventListener('keydown',e=>{keys[e.code]=true;if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();if(gameOver&&e.code==='Enter')reset();});
window.addEventListener('keyup',e=>keys[e.code]=false);document.getElementById('restart').onclick=reset;
function burst(x,y,color,n=10){for(let i=0;i<n;i++){const a=Math.random()*Math.PI*2,s=40+Math.random()*180;particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:.25+Math.random()*.5,color});}}
function spawn(){let x,y;const side=Math.floor(Math.random()*4);if(side===0){x=Math.random()*W;y=-20}else if(side===1){x=W+20;y=Math.random()*H}else if(side===2){x=Math.random()*W;y=H+20}else{x=-20;y=Math.random()*H}
const tough=Math.random()<Math.min(.35,score/800);enemies.push({x,y,r:tough?17:11,speed:(tough?65:85)+Math.random()*45+Math.min(score/15,70),hp:tough?3:1,maxHp:tough?3:1,color:tough?'#ff4fd8':'#ff6b73'});}
function update(dt){
 if(gameOver)return;
 let dx=(keys.KeyD||keys.ArrowRight?1:0)-(keys.KeyA||keys.ArrowLeft?1:0),dy=(keys.KeyS||keys.ArrowDown?1:0)-(keys.KeyW||keys.ArrowUp?1:0);
 if(dx||dy){const l=Math.hypot(dx,dy);player.x+=dx/l*player.speed*dt;player.y+=dy/l*player.speed*dt;}
 player.x=Math.max(player.r,Math.min(W-player.r,player.x));player.y=Math.max(player.r,Math.min(H-player.r,player.y));
 player.angle=Math.atan2(mouse.y-player.y,mouse.x-player.x);player.cooldown-=dt;
 if((mouse.down||keys.Space)&&player.cooldown<=0){bullets.push({x:player.x+Math.cos(player.angle)*20,y:player.y+Math.sin(player.angle)*20,vx:Math.cos(player.angle)*560,vy:Math.sin(player.angle)*560,life:1.2});player.cooldown=.16;burst(player.x+Math.cos(player.angle)*18,player.y+Math.sin(player.angle)*18,'#72f7ff',3);}
 spawnTimer-=dt;if(spawnTimer<=0){spawn();spawnTimer=Math.max(.28,1.05-score/900);}
 for(const b of bullets){b.x+=b.vx*dt;b.y+=b.vy*dt;b.life-=dt;}
 bullets=bullets.filter(b=>b.life>0&&b.x>-10&&b.x<W+10&&b.y>-10&&b.y<H+10);
 for(const en of enemies){const a=Math.atan2(player.y-en.y,player.x-en.x);en.x+=Math.cos(a)*en.speed*dt;en.y+=Math.sin(a)*en.speed*dt;
  if(Math.hypot(player.x-en.x,player.y-en.y)<player.r+en.r){en.dead=true;hp-=en.maxHp===3?12:8;burst(en.x,en.y,en.color,14);hpEl.textContent=Math.max(0,hp);if(hp<=0){hp=0;gameOver=true;}}
  for(const b of bullets){if(!b.dead&&Math.hypot(b.x-en.x,b.y-en.y)<en.r+4){b.dead=true;en.hp--;burst(b.x,b.y,'#ffe58a',4);if(en.hp<=0){en.dead=true;score+=en.maxHp===3?30:10;scoreEl.textContent=score;burst(en.x,en.y,en.color,15);}}}
 }
 enemies=enemies.filter(e=>!e.dead);bullets=bullets.filter(b=>!b.dead);
 for(const p of particles){p.x+=p.vx*dt;p.y+=p.vy*dt;p.vx*=.97;p.vy*=.97;p.life-=dt;}particles=particles.filter(p=>p.life>0);
}
function draw(){
 ctx.clearRect(0,0,W,H);ctx.fillStyle='#080e22';ctx.fillRect(0,0,W,H);
 // star grid
 ctx.strokeStyle='#172449';ctx.lineWidth=1;for(let x=20;x<W;x+=40){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}for(let y=20;y<H;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}
 for(let i=0;i<55;i++){const x=(i*157+31)%W,y=(i*97+17)%H;ctx.fillStyle='#49618e';ctx.fillRect(x,y,2,2);}
 for(const b of bullets){ctx.shadowBlur=14;ctx.shadowColor='#72f7ff';ctx.fillStyle='#bafcff';ctx.beginPath();ctx.arc(b.x,b.y,4,0,Math.PI*2);ctx.fill();}ctx.shadowBlur=0;
 for(const e of enemies){ctx.shadowBlur=16;ctx.shadowColor=e.color;ctx.fillStyle=e.color;ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(e.x-e.r*.25,e.y-e.r*.25,3,0,Math.PI*2);ctx.fill();if(e.maxHp>1){ctx.fillStyle='#351a42';ctx.fillRect(e.x-17,e.y-e.r-9,34,4);ctx.fillStyle='#ff9dec';ctx.fillRect(e.x-17,e.y-e.r-9,34*e.hp/e.maxHp,4);}}
 for(const p of particles){ctx.globalAlpha=Math.max(0,p.life*2);ctx.fillStyle=p.color;ctx.fillRect(p.x,p.y,3,3);}ctx.globalAlpha=1;
 // player
 ctx.save();ctx.translate(player.x,player.y);ctx.rotate(player.angle);ctx.shadowBlur=20;ctx.shadowColor='#54f5ff';ctx.fillStyle='#53eaff';ctx.beginPath();ctx.moveTo(19,0);ctx.lineTo(-11,-11);ctx.lineTo(-6,0);ctx.lineTo(-11,11);ctx.closePath();ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#eaffff';ctx.beginPath();ctx.arc(0,0,5,0,Math.PI*2);ctx.fill();ctx.restore();
 if(gameOver){ctx.fillStyle='#050916cc';ctx.fillRect(0,0,W,H);ctx.textAlign='center';ctx.fillStyle='#ff7a91';ctx.font='bold 48px system-ui';ctx.fillText('GAME OVER',W/2,H/2-25);ctx.fillStyle='#fff';ctx.font='bold 22px system-ui';ctx.fillText('Điểm của bạn: '+score,W/2,H/2+18);ctx.font='16px system-ui';ctx.fillStyle='#aab8d8';ctx.fillText('Nhấn “Chơi lại” hoặc Enter để thử lại',W/2,H/2+55);}
}
function loop(t){const dt=Math.min(.033,(t-(lastTime||t))/1000);lastTime=t;update(dt);draw();requestAnimationFrame(loop);}
reset();requestAnimationFrame(loop);
})();
</script>
</body>
</html>
