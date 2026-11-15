# -*- coding: utf-8 -*-
"""NEC PC-98 Launcher: interfaz + puente para NP2kai/NP21 (Windows) en UN solo archivo.
Doble clic en iniciar_pc98.bat (mismo codigo embebido) o: python pc98_launcher.py
Sin dependencias: solo Python 3.8+. Escucha unicamente en 127.0.0.1.
"""
import json, os, sys, re, io, html, time, shutil, zipfile, hashlib, subprocess, threading, webbrowser, glob, unicodedata
import urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, urlparse, urljoin, urlencode, parse_qs, quote

INDEX_HTML = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>NEC PC-98 Emulador</title>
<style>
:root{color-scheme:dark;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);
--bg:#0a0d10;--bg2:#101519;--panel:#141a1f;--panel2:#1b232a;--line:#28323b;--tx:#e9eff3;--mut:#93a3b0;--ac:#22c55e;--ac2:#4ade80;--ok:#22c55e;--red:#ff4d5e;--ondark:#04220f}
*,*::before,*::after{box-sizing:inherit}
html,body{height:100%;margin:0}
body{background:#050709;color:var(--tx);font:14px/1.35 "Segoe UI",system-ui,-apple-system,Roboto,sans-serif;overflow:hidden}
button,select,input{font:inherit;color:inherit}
button{cursor:pointer}
:focus-visible{outline:2px solid var(--ac2);outline-offset:2px}
select,input{accent-color:var(--ac)}
.app{height:100%;min-height:560px;display:grid;grid-template-rows:40px 34px 1fr;background:linear-gradient(160deg,#0e1418,#06090b 60%);position:relative}
.title{display:flex;align-items:center;gap:10px;padding:0 14px;background:#090d10;border-bottom:1px solid var(--line);user-select:none}
.title .logo{color:var(--ac2);font-size:18px}.title b{font-weight:600}.title span{color:var(--mut)}
.title .sp{flex:1}.wc{display:flex;gap:4px}.wc button{width:36px;height:28px;background:none;border:0;border-radius:6px;font-size:15px}.wc button:hover{background:var(--panel2)}.wc .x:hover{background:#c42b3a}
.menubar{display:flex;gap:2px;padding:0 12px;align-items:center;border-bottom:1px solid #1c2530;position:relative}
.mi{position:relative}.mi>button{background:none;border:0;padding:6px 10px;border-radius:6px}.mi>button:hover,.mi.open>button{background:var(--panel2)}
.dd{display:none;position:absolute;top:100%;left:0;min-width:190px;background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:4px;z-index:50;box-shadow:0 10px 30px #000a}
.mi.open .dd{display:block}.dd button{display:block;width:100%;text-align:left;background:none;border:0;padding:7px 10px;border-radius:5px}.dd button:hover{background:var(--panel2)}
.body{display:grid;grid-template-columns:230px 1fr 360px;gap:0;min-height:0}
.side{padding:14px 14px 0;display:flex;flex-direction:column;min-height:0;background:linear-gradient(180deg,transparent 60%,#0b1114);position:relative}
.brand{padding:6px 4px 16px;font-weight:800;font-size:38px;line-height:.9;letter-spacing:-1px;display:flex;align-items:flex-end;gap:6px}
.brand i{display:block;width:70px;height:46px;background:linear-gradient(120deg,transparent 30%,var(--ac) 30% 45%,transparent 45% 55%,var(--ac2) 55% 70%,transparent 70%);margin-left:auto;transform:skewX(-10deg)}
.nav button{display:flex;align-items:center;gap:14px;width:100%;padding:11px 14px;background:none;border:0;border-radius:8px;color:#c6d3da;font-size:15.5px;text-align:left;margin-bottom:3px}
.nav button:hover{background:var(--panel2)}.nav button.on{background:var(--ac);color:var(--ondark);font-weight:600;box-shadow:0 0 0 1px #4ade8044,0 0 18px #22c55e33}
.nav .ic{width:22px;text-align:center;font-size:18px}.hr{height:1px;background:var(--line);margin:12px 6px}
.pc{margin-top:auto;font-size:80px;text-align:center;opacity:.55;padding-bottom:6px}
.main{padding:12px 14px;display:flex;flex-direction:column;gap:12px;min-width:0;min-height:0;overflow:auto}
.bar{display:flex;gap:10px}
.search{flex:1;display:flex;align-items:center;gap:10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:0 14px;height:46px}
.search input{flex:1;background:none;border:0;outline:0;height:100%}
.bar .sel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:0 12px;height:46px;min-width:170px}
.tg{display:flex;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:3px}.tg button{width:50px;border:0;border-radius:6px;background:none;font-size:20px;color:var(--mut)}.tg .on{background:var(--ac);color:var(--ondark);box-shadow:0 0 0 1px #4ade8044,0 0 14px #22c55e33}
.lib{background:#0f1418;border:1px solid var(--line);border-radius:12px;padding:12px;flex:1;min-height:200px;overflow:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:10px}
.card{background:var(--panel);border:2px solid transparent;border-radius:8px;overflow:hidden;cursor:pointer;text-align:left;padding:0;display:flex;flex-direction:column;position:relative}
.card:hover{border-color:#3a4a55}.card.sel{border-color:var(--ac2);box-shadow:0 0 0 1px #22c55e66,0 0 18px #22c55e55}.card.sel .cap{background:#102a1b}
.cv{position:relative;aspect-ratio:3/3.2;display:flex;align-items:center;justify-content:center;text-align:center;padding:8px;font-weight:800;font-size:clamp(12px,1.1vw,17px);line-height:1.22;text-shadow:0 2px 6px #000,0 0 14px #000a;overflow-wrap:anywhere}
.cap{padding:7px 9px;font-size:13px;color:#dbe6ec;background:#101820;min-height:38px}.cap small{display:block;color:var(--mut);font-size:12px}
a.card{color:inherit;text-decoration:none}.heart{position:absolute;top:6px;right:6px;font-size:16px;color:var(--red);text-shadow:0 0 6px #000}
.cbtn{position:absolute;left:6px;bottom:6px;width:27px;height:27px;display:flex;align-items:center;justify-content:center;border-radius:6px;border:1px solid #ffffff40;background:#0b1216e6;color:#dbe6ec;font-size:14px;line-height:1;padding:0;z-index:2;opacity:.72;box-shadow:0 2px 8px #000a;transition:opacity .15s,border-color .15s,background .15s,color .15s}
.card:hover .cbtn,.card:focus-within .cbtn,.cbtn:focus-visible{opacity:1;border-color:var(--ac2)}
.cbtn:hover{border-color:var(--ac2);background:#102a1b;color:#7ef2a2}
.card.nocover .cbtn{opacity:.9;border-color:#67e8a355;background:#0b1216ee}
.card.nocover .cbtn:hover{background:#102a1b}
.cvprev{width:150px;aspect-ratio:3/4;border-radius:8px;background:#000 center/cover no-repeat;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--mut);font-size:12.5px;text-align:center;padding:8px}
.grid.list{grid-template-columns:1fr}.grid.list .card{flex-direction:row;align-items:center}.grid.list .cv{width:70px;aspect-ratio:1;font-size:13px;flex:none}.grid.list .cap{flex:1;min-height:0;display:flex;gap:20px;align-items:center}
.row3{display:grid;grid-template-columns:1.15fr 1fr .85fr;gap:12px;align-items:start}
.box{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.box h3{margin:0 0 10px;font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px}.box h3 a{margin-left:auto;color:var(--ac2);font-size:13px;font-weight:400;cursor:pointer;text-decoration:underline}
.rec{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.rc{display:flex;background:var(--panel2);border:0;border-radius:6px;overflow:hidden;text-align:left;padding:0;height:78px}.rc:hover{outline:1px solid var(--ac2)}
.rc .th{width:78px;flex:none;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;text-align:center}.rc .tx{padding:8px 10px;font-size:13px}.rc .tx small{display:block;color:var(--mut);margin-top:4px}
.q{display:grid;grid-template-columns:auto minmax(70px,1fr);gap:8px 10px;align-items:center;font-size:12.5px}.q select{background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:6px 8px;width:100%;min-width:0}
.mon{display:flex;flex-direction:column;gap:9px;font-size:13px}.mon .r{display:flex;align-items:center;gap:12px}.meter{width:44px;height:14px;background:#0e2a1a;border-radius:2px;overflow:hidden;flex:none}.meter i{display:block;height:100%;background:var(--ok);transition:width .4s}.mon .v{color:var(--ok)}
.mst{font-size:12px;color:var(--mut);border-bottom:1px solid var(--line);padding-bottom:7px;word-break:break-all}
.spark{width:100%;height:34px}
.det{padding:12px 14px 12px 0;display:flex;flex-direction:column;gap:12px;min-height:0;overflow:auto}
.dp{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;gap:12px;padding-bottom:12px}
.dp .cv{aspect-ratio:16/8.4;font-size:clamp(18px,2vw,34px);border-radius:0;line-height:1.2}
.dp h2{margin:0;text-align:center;font-size:18px;font-weight:500}
.meta{padding:0 16px;display:grid;grid-template-columns:28px 90px 1fr;gap:9px 4px;align-items:center;font-size:14px}.meta span:nth-child(3n+2){color:#c8d3da}
.dp p{margin:0;padding:0 16px;color:#c2cdd4;font-size:14.5px;line-height:1.45}
.btns{padding:0 14px;display:flex;flex-direction:column;gap:8px}
.btn{height:42px;border-radius:6px;border:1px solid var(--line);background:var(--panel2);display:flex;align-items:center;justify-content:center;gap:10px}.btn:hover{border-color:var(--ac2)}
.btn.pri{background:var(--ac);border-color:var(--ac);color:var(--ondark);font-weight:700;font-size:16px;height:46px}.btn.pri:hover{background:var(--ac2)}
.view{padding:6px 4px}.view h2{margin:0 0 12px}.view .cardsx{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.view .box button{margin-top:8px}
.tbl{width:100%;border-collapse:collapse}.tbl td{padding:8px;border-bottom:1px solid var(--line)}.tbl kbd{background:var(--panel2);border:1px solid var(--line);border-radius:5px;padding:2px 8px}
.ov{position:absolute;inset:0;background:#000c;display:none;align-items:center;justify-content:center;z-index:100;flex-direction:column;gap:14px;text-align:center}.ov.on{display:flex}
.screen{width:min(640px,86%);aspect-ratio:16/10;background:#000;border:3px solid #333;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:8px;font-family:ui-monospace,Consolas,monospace;color:#7dffa0;box-shadow:0 0 40px #22c55e55}
.modal{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 24px;max-width:460px;width:86%;text-align:left}.modal h2{margin-top:0}
.modal .mv{display:flex;gap:8px;margin-top:14px}
.frm{display:grid;grid-template-columns:104px 1fr;gap:8px 10px;align-items:center}
.frm label{color:var(--mut);font-size:13.5px;text-align:right}
.frm input,.frm textarea{background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:8px 10px;width:100%;font:inherit;color:var(--tx)}
.frm input:focus,.frm textarea:focus{border-color:var(--ac2);outline:none}
.frm textarea{resize:vertical;min-height:82px}
.frm .hint{grid-column:2;color:var(--mut);font-size:12.5px}
.dl{display:grid;grid-template-columns:88px 1fr;gap:6px 10px;font-size:14px}
.dl span:nth-child(odd){color:var(--mut)}
.dl b{font-weight:500;word-break:break-all}
.toast{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);background:var(--ac);color:var(--ondark);font-weight:600;padding:10px 18px;border-radius:8px;opacity:0;pointer-events:none;transition:.25s;z-index:200}.toast.on{opacity:1}
@media(max-width:1150px){.body{grid-template-columns:200px 1fr}.det{display:none}.grid{grid-template-columns:repeat(3,1fr)}.row3{grid-template-columns:1fr}}
@media(max-width:700px){.body{grid-template-columns:1fr;grid-template-rows:auto 1fr}.side{flex-direction:row;overflow-x:auto;padding:6px}.brand,.pc,.hr{display:none}.nav{display:flex}.nav button{white-space:nowrap;width:auto}.grid{grid-template-columns:repeat(2,1fr)}.bar{flex-wrap:wrap}.rec{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="app" id="app">
  <div class="title"><span class="logo">🎮</span><b>NEC PC-98 Emulador</b><span>v1.0.0</span><span>—</span><b>Jugar</b><span>•</span><b>Explorar</b><span>•</span><b>Disfrutar</b><div class="sp"></div>
    <div class="wc"><button data-w="min">—</button><button data-w="max">☐</button><button class="x" data-w="close">✕</button></div></div>
  <div class="menubar" id="menubar"></div>
  <div class="body">
    <aside class="side">
      <div class="brand">NEC<br>PC-98<i></i></div>
      <nav class="nav" id="nav"></nav>
      <div class="pc">🖥️</div>
    </aside>
    <main class="main" id="main"></main>
    <aside class="det" id="det"></aside>
  </div>
  <div class="ov" id="ov"></div>
  <div class="toast" id="toast"></div>
</div>
<script>
const DEMO=[
{id:1,n:"Doukyuusei 2",t:"同級生2",g:"Novela Visual",m:"PC-9821",s:5.3,p:12,fav:1,c:"linear-gradient(160deg,#5b3bd6,#a6b9ff 55%,#f3c9d6)",d:"Una conmovedora historia de amor ambientada en el instituto, con múltiples finales y personajes inolvidables."},
{id:2,n:"Tokimeki Memorial",t:"ときめきメモリアル",g:"Simulación",m:"PC-9821",s:7.1,p:8,fav:0,c:"linear-gradient(160deg,#c0583a,#f3b86b 50%,#e86fa8)",d:"Simulador de vida escolar: estudia, practica deportes y conquista a la chica de tus sueños antes de la graduación."},
{id:3,n:"Star Blazers",t:"STAR BLAZERS",g:"Shooter",m:"PC-9801",s:2.4,p:3,fav:0,c:"linear-gradient(160deg,#050816,#1a2a66 60%,#d4481a)",d:"Shooter espacial de acción frenética a bordo de una gran nave de guerra."},
{id:4,n:"Sotsugyou",t:"卒業",g:"Simulación",m:"PC-9801",s:3.8,p:5,fav:0,c:"linear-gradient(160deg,#3ca35a,#b7e08a 60%,#7ab7ff)",d:"Guía a cinco estudiantes hasta su graduación en este clásico simulador de crianza."},
{id:5,n:"1941 Counter Attack",t:"1941",g:"Shooter",m:"PC-9801",s:1.2,p:2,fav:0,c:"linear-gradient(160deg,#2f6fd0,#e0a73a 60%,#c0412a)",d:"Arcade de aviones de la Segunda Guerra Mundial con jefes enormes y mucha potencia de fuego."},
{id:6,n:"Rance Quest",t:"Rance Quest",g:"RPG",m:"PC-9821",s:9.6,p:6,fav:0,c:"linear-gradient(160deg,#4e8b4a,#f2cf6b 50%,#46a7d8)",d:"Aventura de rol con el infame Rance, combates por turnos y un humor muy particular."},
{id:7,n:"Muv-Luv",t:"マブラヴ",g:"Novela Visual",m:"PC-9821",s:12.4,p:4,fav:0,c:"linear-gradient(160deg,#1c1860,#5a4be0 55%,#8a9bff)",d:"Drama romántico que da un giro inesperado hacia la ciencia ficción y los mechas."},
{id:8,n:"風の伝説ザナドゥ Xanadu",t:"風の伝説ザナドゥ",g:"RPG",m:"PC-9801",s:4.9,p:7,fav:0,c:"linear-gradient(160deg,#1b3a7a,#6ea0e0 50%,#c8b27a)",d:"Segunda entrega de la saga Xanadu, con ciudades vivas y exploración libre."},
{id:9,n:"プリンセスメーカー Princess Maker",t:"プリンセスメーカー",g:"Simulación",m:"PC-9821",s:6.2,p:9,fav:0,c:"linear-gradient(160deg,#f2a58a,#ffe0cc 55%,#f08aa6)",d:"Cría a una niña durante ocho años y decide si será princesa, guerrera o algo más."},
{id:10,n:"ザナドゥ Xanadu",t:"ザナドゥ",g:"RPG",m:"PC-9801",s:2.9,p:10,fav:0,c:"linear-gradient(160deg,#1a1408,#6b4a18 55%,#d9a441)",d:"El RPG de acción que lo empezó todo, con mazmorras laberínticas y progresión por niveles."}];
let G=DEMO,API=false,FOLDER="";
const cs=g=>g.img?`background:#000 url('${g.img}') center/cover`:`background:${g.c}`;
let recents=[2,1,3],sel=1,view="Biblioteca",mode="grid",q="",gen="",mod="";
const $=s=>document.querySelector(s),gm=i=>G.find(x=>x.id===i);
const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const NAV=[["🏠","Biblioteca"],["♥","Favoritos"],["🕒","Recientes"],["☰","Listas"],["🧭","Explorar"],["🛍","Tienda / Extras"],"-",["⚙","Configuración"],["🎮","Controles"],["ℹ","Acerca de"]];
$("#nav").innerHTML=NAV.map(n=>n==="-"?'<div class="hr"></div>':`<button data-v="${n[1]}"><span class="ic">${n[0]}</span>${n[1]}</button>`).join("");
const MENUS={Archivo:["Abrir imagen de disco…","Añadir carpeta de juegos","Salir"],Juego:["Iniciar juego","Añadir a favoritos","Carátula…","Editar datos","Ver detalles"],"Configuración":["Preferencias","Controles"],Ayuda:["Acerca de","Atajos de teclado"]};
$("#menubar").innerHTML=Object.entries(MENUS).map(([k,v])=>`<div class="mi"><button>${k}</button><div class="dd">${v.map(x=>`<button data-m="${x}">${x}</button>`).join("")}</div></div>`).join("");
function toast(t){const e=$("#toast");e.textContent=t;e.classList.add("on");clearTimeout(toast.h);toast.h=setTimeout(()=>e.classList.remove("on"),1800)}
function card(g){return`<div class="card ${g.id===sel?"sel":""}${g.img?"":" nocover"}" data-id="${g.id}" role="button" tabindex="0" aria-label="${esc(g.n)}"><div class="cv" style="${cs(g)}">${g.img?"":g.t}<button class="cbtn" data-cover="${g.id}" title="Poner o cambiar la carátula" aria-label="Poner o cambiar la carátula">🖼</button></div><div class="cap">${g.n}${mode==="list"?`<small>${g.g}</small><small>${g.m}</small><small>${g.s} MB</small>`:""}</div>${g.fav?'<span class="heart">♥</span>':""}</div>`}
function filtered(){return G.filter(g=>(!q||g.n.toLowerCase().includes(q)||g.t.includes(q))&&(!gen||g.g===gen)&&(!mod||g.m===mod))}
const CFG={res:["Auto (Nativo)"],fil:["Ninguno","Scanlines"],fs:["Automático","Desactivado","1","2","3"]};
const sl=(a,v)=>a.map(x=>`<option${x===v?" selected":""}>${x}</option>`).join("");
const S={res:CFG.res[0],fil:CFG.fil[0],aud:true,fs:CFG.fs[0]};
function recHTML(){return recents.filter(gm).slice(0,3).map(i=>{const g=gm(i),w=["3 h atrás","1 día atrás","2 días atrás"][recents.indexOf(i)]||"hace poco";return`<button class="rc" data-id="${i}"><div class="th" style="${cs(g)}">${g.img?"":g.t.slice(0,6)}</div><div class="tx">${g.n}<small>(${w})</small></div></button>`}).join("")}
function renderMain(){
 const m=$("#main");
 if(view==="Biblioteca"||view==="Favoritos"){
  let list=filtered();if(view==="Favoritos")list=list.filter(g=>g.fav);
  const gens=[...new Set(G.map(g=>g.g))],mods=[...new Set(G.map(g=>g.m))];
  m.innerHTML=`<div class="bar"><label class="search">🔍<input id="q" placeholder="Buscar juegos..." value="${q}"></label>
  <select class="sel" id="gen"><option value="">Todos los géneros</option>${gens.map(x=>`<option${x===gen?" selected":""}>${x}</option>`).join("")}</select>
  <select class="sel" id="mod"><option value="">Todos los modelos</option>${mods.map(x=>`<option${x===mod?" selected":""}>${x}</option>`).join("")}</select>
  <div class="tg"><button data-mode="grid" class="${mode==="grid"?"on":""}" title="Cuadrícula">▦</button><button data-mode="list" class="${mode==="list"?"on":""}" title="Lista">☰</button></div></div>
  <div class="lib"><div class="grid ${mode}">${list.map(card).join("")||'<p style="color:var(--mut)">No hay discos en '+(FOLDER||"la carpeta de juegos")+'. Abre <b>⚙ Configuración → Elegir carpeta…</b>.</p>'}</div></div>${bottom()}`;
  const i=$("#q");i.oninput=()=>{q=i.value.toLowerCase();const p=i.selectionStart;renderMain();const n=$("#q");n.focus();n.setSelectionRange(p,p)};
  $("#gen").onchange=e=>{gen=e.target.value;renderMain()};$("#mod").onchange=e=>{mod=e.target.value;renderMain()};
 } else if(view==="Recientes"){
  m.innerHTML=`<div class="view"><h2>🕒 Recientes</h2><div class="cardsx">${recents.filter(gm).map(i=>card(gm(i))).join("")}</div></div>${bottom()}`;
 } else if(view==="Listas"){
  const gs=[...new Set(G.map(g=>g.g))];
  m.innerHTML=`<div class="view"><h2>☰ Listas</h2><div class="cardsx">${gs.map(x=>`<div class="box"><h3>${x}</h3>${G.filter(g=>g.g===x).map(g=>`<div>• ${g.n}</div>`).join("")}<button class="btn" data-lgen="${x}" style="width:100%">Ver en biblioteca</button></div>`).join("")}</div></div>`;
 } else if(view==="Explorar"){
  m.innerHTML=`<div class="view"><h2>🧭 Explorar</h2><div class="bar" style="margin-bottom:10px"><div class="tg">${[["myabandonware","MyAbandonware"],["romsfun","ROMsFun"]].map(s=>`<button data-site="${s[0]}" class="${site===s[0]?"on":""}" style="width:auto;padding:0 16px;font-size:14px">${s[1]}</button>`).join("")}</div><button class="btn" id="opensite" style="padding:0 16px">↗ Abrir sitio</button><button class="btn" id="imp" style="padding:0 16px">⬆ Importar disco o .zip</button><input type="file" id="impf" hidden multiple accept=".zip,.hdi,.nhd,.thd,.fdi,.d88,.88d,.hdm,.nfd,.xdf,.dup,.tfd,.d98,.98d,.hdd,.fdd"></div><div class="box" id="dz" style="margin-bottom:10px;color:var(--mut)">Haz clic en una portada para abrir la página del juego. Descarga allí lo que quieras y arrastra aquí el archivo (.zip o disco): se guarda en tu carpeta de juegos. Si lo descargas en tu carpeta de Descargas, se importa solo y le busca la carátula.</div><div class="grid" id="cat"><p style="color:var(--mut)">Cargando…</p></div></div>`;
  document.querySelectorAll("[data-site]").forEach(b=>b.onclick=()=>{site=b.dataset.site;renderMain()});
  $("#opensite").onclick=()=>window.open(SITEURL[site],"_blank","noopener");
  $("#imp").onclick=()=>API?$("#impf").click():toast("Requiere el puente");$("#impf").onchange=e=>importFiles(e.target.files);
  const dz=$("#dz");dz.ondragover=e=>e.preventDefault();dz.ondrop=e=>{e.preventDefault();API?importFiles(e.dataTransfer.files):toast("Requiere el puente")};
  loadCat();
 } else if(view==="Tienda / Extras"){
  const X=[["Pack de parches de traducción","Parches fan en español","Instalar"],["Fuentes japonesas JIS","Mejora la lectura de texto","Instalar"],["Filtro CRT Retro","Shader de tubo catódico","Instalar"],["BIOS alternativa","Compatibilidad extra","Instalar"]];
  m.innerHTML=`<div class="view"><h2>🛍 Tienda / Extras</h2><div class="cardsx">${X.map(x=>`<div class="box"><h3>${x[0]}</h3><div style="color:var(--mut)">${x[1]}</div><button class="btn" data-ex="${x[0]}" style="width:100%">${x[2]}</button></div>`).join("")}</div></div>`;
 } else if(view==="Configuración"){
  m.innerHTML=`<div class="view"><h2>⚙ Configuración</h2><div class="box"><h3>📁 Carpeta de juegos</h3><div id="fold" style="color:var(--mut);margin-bottom:8px;word-break:break-all">${FOLDER||"(sin definir)"}</div><div style="display:flex;gap:8px"><button class="btn" id="fsel" style="flex:1">📂 Elegir carpeta…</button><button class="btn" id="fopen" style="flex:0 0 auto;padding:0 14px">Abrir</button></div><div style="display:flex;gap:8px;margin-top:8px"><input id="fpath" placeholder="D:\\Juegos\\PC98" style="flex:1;background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:8px"><button class="btn" id="fuse" style="flex:0 0 auto;padding:0 14px">Usar</button></div><div style="color:var(--mut);font-size:12.5px;margin-top:8px">Los discos (.hdi, .fdi, .d88…) de esa carpeta y sus subcarpetas salen en la biblioteca.</div></div><div class="box" style="margin-top:12px"><h3>🎛 Emulador</h3><div class="q" style="font-size:14px">${qc()}</div><div style="color:var(--mut);font-size:12.5px;margin-top:8px">Al lanzar se escriben en np21.ini: SampleHz, SkpFrame/DispSync y skipline. Este NP21/W no admite resolución ni filtros xBRZ por configuración.</div></div><div class="box" style="margin-top:12px"><h3>🎯 Perfil por juego</h3><div style="color:var(--mut);margin-bottom:8px">Los ajustes de arriba valen para todos. Guarda una excepción para el juego seleccionado.</div><div style="display:flex;gap:8px"><button class="btn" id="psave" style="flex:1">Guardar para este juego</button><button class="btn" id="pclear" style="flex:0 0 auto;padding:0 14px">Quitar</button></div><div id="pst" style="color:var(--mut);font-size:12.5px;margin-top:8px"></div></div><div class="box" style="margin-top:12px"><h3>🖼 Carátulas</h3><div id="cvst" style="color:var(--mut);margin-bottom:8px">Busca carátulas en internet para los juegos que no tengan una.</div><button class="btn" id="cvall" style="padding:0 18px">Buscar carátulas de todos</button></div></div>`;bindQ();$("#cvall").onclick=coverAll;pollCover();
  $("#fsel").onclick=()=>{toast("Espera al selector de carpetas…");jpost("/api/folder",{}).then(r=>{if(!r.ok)return toast(r.error||"Cancelado");FOLDER=r.carpeta;toast("Carpeta lista: "+r.juegos+" juego(s)");renderMain();reload()})};
  $("#fopen").onclick=()=>jpost("/api/openfolder",{}).then(r=>{if(!r.ok)toast(r.error)});
  $("#fuse").onclick=()=>{const p=$("#fpath").value.trim();if(!p)return toast("Escribe una ruta");jpost("/api/folder",{path:p}).then(r=>{toast(r.ok?"Carpeta lista: "+r.juegos+" juego(s)":r.error);if(r.ok){FOLDER=r.carpeta;renderMain();reload()}})};
  $("#psave").onclick=()=>{const g=gm(sel);if(!g)return toast("Selecciona un juego");jpost("/api/perfil",{id:g.id,cfg:S}).then(()=>{const e=$("#pst");if(e)e.textContent="Perfil guardado para «"+g.n+"»";toast("Perfil del juego guardado")})};
  $("#pclear").onclick=()=>{const g=gm(sel);if(!g)return toast("Selecciona un juego");jpost("/api/perfil",{id:g.id,cfg:null}).then(()=>{const e=$("#pst");if(e)e.textContent="«"+g.n+"» usa el perfil general";toast("Perfil del juego quitado")})};
 } else if(view==="Controles"){
  const K=[["Mover","↑ ↓ ← →"],["Aceptar / Disparo","Z"],["Cancelar","X"],["Menú","Esc"],["Pausa","P"],["Pantalla completa","F11"],["Captura","F12"]];
  m.innerHTML=`<div class="view"><h2>🎮 Controles</h2><div class="box"><table class="tbl">${K.map(k=>`<tr><td>${k[0]}</td><td><kbd>${k[1]}</kbd></td></tr>`).join("")}</table></div></div>`;
 } else {
  m.innerHTML=`<div class="view"><h2>ℹ Acerca de</h2><div class="box"><b>NEC PC-98 Emulador</b> v1.0.0<br><span style="color:var(--mut)">Prototipo de interfaz. Jugar • Explorar • Disfrutar.</span></div></div>`;
 }
 document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("on",b.dataset.v===view));
 const mon=$("#mon");if(mon)monTick()
}
const qc=()=>`<label for="s1">Resolución:</label><select id="s1" data-k="res">${sl(CFG.res,S.res)}</select><label for="s2">Filtro:</label><select id="s2" data-k="fil">${sl(CFG.fil,S.fil)}</select><label>Audio:</label><label><input type="checkbox" data-k="aud" ${S.aud?"checked":""}> Alta Calidad</label><label for="s4">Frameskip:</label><select id="s4" data-k="fs">${sl(CFG.fs,S.fs)}</select>`;
function bindQ(){document.querySelectorAll("[data-k]").forEach(e=>e.onchange=()=>{S[e.dataset.k]=e.type==="checkbox"?e.checked:e.value;toast("Configuración guardada");if(API)fetch("/api/config",{method:"POST",body:JSON.stringify({ajustes:S})})})}
function bottom(){return`<div class="row3"><div class="box"><h3>🕒 Juegos Recientes <a data-v2="Recientes">Ver todos →</a></h3><div class="rec">${recHTML()||'<p style="color:var(--mut);font-size:13px;margin:0">Todavía no has jugado a nada.</p>'}</div></div><div class="box"><h3>⚙ Configuración Rápida</h3><div class="q">${qc()}</div></div><div class="box mon" id="mon"><div class="mst" id="mst">NP21 detenido</div><div class="r" title="NP21 no expone los FPS a otros programas"><span class="meter"><i id="mf"></i></span><span>FPS: <span class="v" id="vf">—</span></span></div><div class="r"><span class="meter"><i id="mc"></i></span><span>CPU: <span class="v" id="vc">—</span></span></div><div class="r"><span class="meter"><i id="mr"></i></span><span>RAM: <span class="v" id="vr">—</span></span></div><svg class="spark" viewBox="0 0 100 30" preserveAspectRatio="none"><polyline id="sp" fill="none" stroke="#2fd25a" stroke-width="1.5" points=""/></svg></div></div>`}
function renderDet(){
 const g=gm(sel);if(!g){$("#det").innerHTML='<div class="dp"><p style="padding-top:16px">Sin juegos. Copia tus discos (.hdi, .fdi, .d88…) a la carpeta de juegos.</p></div>';return}
 $("#det").innerHTML=`<div class="dp"><div class="cv" style="${cs(g)}">${g.img?"":g.t}</div><h2>${g.n}</h2>
 <div class="meta"><span>🎮</span><span>Género:</span><span>${g.g}</span><span>🖥</span><span>Modelo:</span><span>${g.m}</span><span>💾</span><span>Tamaño:</span><span>${g.s} MB</span><span>★</span><span>Jugado:</span><span>${g.p} veces</span><span style="color:var(--red)">♥</span><span>Favorito:</span><span style="color:${g.fav?"var(--red)":"var(--ac2)"}">${g.fav?"♥":"♡"}</span></div>
 <p>${g.d}</p>
 <div class="btns"><button class="btn pri" id="play">▶ Iniciar Juego</button><button class="btn" id="fav">${g.fav?"♥ Quitar de Favoritos":"♥ Añadir a Favoritos"}</button><button class="btn" id="edit">✎ Editar datos</button><button class="btn" id="info">ⓘ Ver Detalles</button><div style="display:flex;gap:8px"><button class="btn" id="cvs" style="flex:1">🖼 Carátula…</button><button class="btn" id="cvm" style="flex:1">📁 Subir imagen</button></div><input type="file" id="cvf" accept="image/*" hidden></div></div>`;
 $("#play").onclick=play;$("#fav").onclick=()=>{g.fav=g.fav?0:1;if(API)fetch("/api/fav",{method:"POST",body:JSON.stringify({id:g.id,fav:g.fav})});toast(g.fav?"Añadido a favoritos":"Quitado de favoritos");renderAll()};$("#info").onclick=details;$("#edit").onclick=editData;$("#cvs").onclick=()=>coverMenu(g.id);$("#cvm").onclick=()=>API?$("#cvf").click():toast("Requiere el puente");$("#cvf").onchange=coverUpload;
}
function renderAll(){renderMain();renderDet()}
function play(){const g=gm(sel);if(!g)return;g.p++;if(API){recents=[g.id,...recents.filter(x=>x!==g.id)].slice(0,12);fetch("/api/play",{method:"POST",body:JSON.stringify({id:g.id})}).then(r=>r.json()).then(j=>{if(!j.ok)return toast(j.error);toast(j.nota?j.nota:"Lanzando "+g.n+" en NP21…")}).catch(()=>toast("Puente no disponible"));renderAll();return}recents=[g.id,...recents.filter(x=>x!==g.id)].slice(0,3);
 const o=$("#ov");o.innerHTML=`<div class="screen"><div style="font-size:22px">${g.t}</div><div>${g.n}</div><div>[ ${S.res} • ${S.fil} ]</div><div>Cargando disco... ▮</div></div><button class="btn" id="stop" style="padding:0 24px">■ Detener emulación</button>`;o.classList.add("on");
 $("#stop").onclick=()=>{o.classList.remove("on");renderAll()}}
function details(){const g=gm(sel);if(!g)return;const o=$("#ov");
 const fecha=g.mtime?new Date(g.mtime*1000).toLocaleString("es-ES",{dateStyle:"medium",timeStyle:"short"}):"—";
 const mb=g.bytes?(g.bytes/1048576).toFixed(1):g.s;
 o.innerHTML=`<div class="modal" style="max-width:580px"><h2>${esc(g.n)}</h2>
 <div class="dl"><span>Archivo</span><b>${esc(g.file||"—")}</b><span>Carpeta</span><b>${esc(g.dir||"—")}</b><span>Tamaño</span><b>${mb} MB</b><span>Fecha</span><b>${esc(fecha)}</b><span>Jugado</span><b>${g.p} ${g.p===1?"vez":"veces"}</b><span>Datos</span><b>${g.custom?"personalizados":"por defecto, sin editar"}</b></div>
 <p style="color:var(--mut);line-height:1.45">${esc(g.d)}</p>
 <div class="mv"><button class="btn" id="dedit" style="flex:1">✎ Editar datos</button><button class="btn" id="drev" style="flex:1">📂 Abrir carpeta</button></div>
 <button class="btn" id="cl" style="width:100%;margin-top:8px">Cerrar</button></div>`;
 o.classList.add("on");$("#cl").onclick=()=>o.classList.remove("on");
 $("#dedit").onclick=()=>{o.classList.remove("on");editData()};
 $("#drev").onclick=()=>jpost("/api/reveal",{id:g.id}).then(r=>{if(!r.ok)toast(r.error)})}
function editData(){const g=gm(sel);if(!g)return;
 if(!API)return toast("Requiere el puente");
 const gens=[...new Set([...G.map(x=>x.g),"RPG","Novela Visual","Shooter","Simulación","Aventura","Puzzle","Estrategia","Acción"].filter(Boolean))];
 const mods=[...new Set([...G.map(x=>x.m),"PC-8801","PC-9801","PC-9801VX","PC-9801VM","PC-9821","PC-9821Xa"].filter(Boolean))];
 const limpio=v=>v&&!v.startsWith("Disco:")?v:"";
 const o=$("#ov");
 o.innerHTML=`<div class="modal" style="max-width:640px"><h2>✎ Datos de «${esc(g.n)}»</h2>
 <div class="frm">
  <label for="dn">Nombre</label><input id="dn" maxlength="120" value="${esc(g.n)}" placeholder="Nombre en la lista">
  <label for="dt">Título original</label><input id="dt" maxlength="120" value="${esc(g.t===g.n?"":g.t)}" placeholder="日本語 o nombre alternativo">
  <label for="dg">Género</label><input id="dg" list="lgen" maxlength="60" value="${esc(g.g==="Sin clasificar"?"":g.g)}" placeholder="RPG, Shooter, Novela Visual…">
  <datalist id="lgen">${gens.map(x=>`<option value="${esc(x)}">`).join("")}</datalist>
  <label for="dm">Modelo</label><input id="dm" list="lmod" maxlength="60" value="${esc(g.m==="PC-98"?"":g.m)}" placeholder="PC-9801VX, PC-9821…">
  <datalist id="lmod">${mods.map(x=>`<option value="${esc(x)}">`).join("")}</datalist>
  <label for="dd">Descripción</label><textarea id="dd" rows="4" maxlength="600" placeholder="Sinopsis, idioma, notas…">${esc(limpio(g.d))}</textarea>
  <div class="hint">Si dejas un campo vacío vuelve al valor por defecto. Se guarda en datos.json; el disco no se modifica.</div>
 </div>
 <div class="mv"><button class="btn pri" id="dsave" style="flex:1">Guardar</button><button class="btn" id="dreset" style="flex:0 0 auto;padding:0 16px">Restablecer</button><button class="btn" id="dclose" style="flex:0 0 auto;padding:0 16px">Cancelar</button></div></div>`;
 o.classList.add("on");
 const val=id=>{const e=$(id);return e?e.value.trim():""};
 $("#dclose").onclick=()=>o.classList.remove("on");
 $("#dreset").onclick=()=>jpost("/api/meta",{id:g.id,data:null}).then(r=>{if(!r.ok)return toast(r.error);o.classList.remove("on");toast("Datos restablecidos");return reload()}).then(()=>renderAll());
 $("#dsave").onclick=()=>jpost("/api/meta",{id:g.id,data:{n:val("#dn"),t:val("#dt"),g:val("#dg"),m:val("#dm"),d:val("#dd")}}).then(r=>{
  if(!r.ok)return toast(r.error||"No se pudo guardar");
  o.classList.remove("on");toast("Datos guardados");return reload()}).then(()=>renderAll());
 $("#dn").focus()}
function pick(id){sel=id;renderAll()}
document.addEventListener("click",e=>{
 const t=e.target;
 const mi=t.closest(".mi");document.querySelectorAll(".mi").forEach(x=>{if(x!==mi)x.classList.remove("open")});
 if(mi&&t.closest(":scope>button,.mi>button")&&!t.dataset.m){mi.classList.toggle("open");return}
 const mb=t.closest("[data-m]");if(mb){mi&&mi.classList.remove("open");const a=mb.dataset.m;
  if(a==="Iniciar juego")play();else if(a==="Añadir a favoritos")$("#fav").click();else if(a==="Carátula…")coverMenu(sel);else if(a==="Editar datos")editData();else if(a==="Ver detalles")details();else if(a==="Preferencias"){view="Configuración";renderMain()}else if(a==="Controles"){view="Controles";renderMain()}else if(a==="Acerca de"){view="Acerca de";renderMain()}else if(a==="Añadir carpeta de juegos"){view="Configuración";renderMain();setTimeout(()=>{const b=$("#fsel");b&&b.click()},60)}else if(a==="Salir")toast("Cierra la pestaña para salir");else toast(a)
  return}
 const w=t.closest("[data-w]");if(w){const app=$("#app");if(w.dataset.w==="max")document.documentElement.requestFullscreen?.().catch(()=>toast("Pantalla completa no disponible"));else toast(w.dataset.w==="min"?"Minimizar (demo)":"Cerrar (demo)");return}
 const nv=t.closest("[data-v]");if(nv){view=nv.dataset.v;renderMain();return}
 const v2=t.closest("[data-v2]");if(v2){view=v2.dataset.v2;renderMain();return}
 const md=t.closest("[data-mode]");if(md){mode=md.dataset.mode;renderMain();return}
 const lg=t.closest("[data-lgen]");if(lg){gen=lg.dataset.lgen;view="Biblioteca";renderMain();return}
 const ex=t.closest("[data-ex]");if(ex){toast("Instalado: "+ex.dataset.ex);ex.textContent="✓ Instalado";return}
 const cvb=t.closest("[data-cover]");if(cvb){e.preventDefault();coverMenu(cvb.dataset.cover);return}
 const c=t.closest("[data-id]");if(c){pick(c.dataset.id)}
});
document.addEventListener("keydown",e=>{
 if((e.key==="Enter"||e.key===" ")&&e.target.classList&&e.target.classList.contains("card")){e.preventDefault();pick(e.target.dataset.id)}
});
document.addEventListener("dblclick",e=>{if(e.target.closest("[data-cover]"))return;if(e.target.closest(".card"))play()});
const HIST=[];
function monTick(){
 if(!$("#mon"))return;
 const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
 const bar=(id,pct)=>{const e=document.getElementById(id);if(e)e.style.width=Math.max(0,Math.min(100,pct))+"%"};
 const st=document.getElementById("mst");
 if(!API){set("vf","—");set("vc","—");set("vr","—");bar("mf",0);bar("mc",0);bar("mr",0);if(st)st.textContent="Requiere el puente";return}
 fetch("/api/proc").then(r=>r.json()).then(p=>{
  set("vf","—");bar("mf",0);
  if(p.running){
   set("vc",p.cpu==null?"—":p.cpu.toFixed(0)+"%");
   set("vr",p.ram==null?"—":Math.round(p.ram)+" MB");
   bar("mc",p.cpu||0);bar("mr",Math.min(100,(p.ram||0)/8));
   if(st)st.innerHTML='<b style="color:var(--ok)">● En ejecución</b> · '+esc((p.names||[]).join(", "))+(p.pid?" · PID "+p.pid:"");
   HIST.push(p.cpu||0);if(HIST.length>40)HIST.shift();
  }else{
   set("vc","—");set("vr","—");bar("mc",0);bar("mr",0);
   if(st)st.textContent="NP21 detenido";
   HIST.length=0;
  }
  const sp=document.getElementById("sp");
  if(sp)sp.setAttribute("points",HIST.map((v,i)=>`${i*100/39},${30-Math.min(30,v*0.28)}`).join(" "));
 }).catch(()=>{if(st)st.textContent="Sin datos"});
}
setInterval(monTick,1000);
let site="myabandonware",pt=null,lastFound=-1,lastImp=-1;
const SITEURL={myabandonware:"https://www.myabandonware.com/browse/platform/pc98/?pl%5B0%5D=pc98",romsfun:"https://romsfun.com/roms/nec-pc-9801/"};
const jpost=(u,b)=>fetch(u,{method:"POST",body:JSON.stringify(b||{})}).then(r=>r.json());
function reload(){return fetch("/api/games").then(r=>r.json()).then(j=>{G=j.games;recents=j.recents;FOLDER=j.carpeta||FOLDER;if(!gm(sel))sel=(G[0]||{}).id;renderAll()})}
function loadCat(){const c=$("#cat");if(!c)return;if(!API){c.innerHTML='<p style="color:var(--mut)">Requiere el puente (pc98_launcher.py).</p>';return}
 fetch("/api/catalog?site="+site).then(r=>r.json()).then(j=>{const e=$("#cat");if(!e)return;e.innerHTML=j.items.length?j.items.map(x=>`<a class="card" href="${x.u}" target="_blank" rel="noopener noreferrer"><div class="cv" style="background:#000 url('${x.i}') center/cover"></div><div class="cap">${x.t}</div></a>`).join(""):`<p style="color:var(--mut)">${j.error||"Sin resultados."} Usa «Abrir sitio».</p>`}).catch(()=>{const e=$("#cat");e&&(e.innerHTML="<p>Error de red</p>")})}
function importFiles(fs){[...fs].forEach(f=>fetch("/api/import?name="+encodeURIComponent(f.name),{method:"POST",body:f}).then(r=>r.json()).then(r=>{toast(r.ok?"Importado: "+r.added.join(", "):r.error);reload();pollCover()}))}
let cvFor=null;
function coverMenu(id){
 if(!API)return toast("Requiere el puente");
 const g=gm(id||sel);if(!g)return;
 cvFor=g.id;pick(g.id);
 const base=(g.file||g.n).replace(/\.[^.]+$/,"");
 const prev=g.img?`<div class="cvprev" style="${cs(g)}"></div>`:`<div class="cvprev">Sin carátula</div>`;
 const nota=g.img?`Carátula actual guardada junto al disco.`:`Ahora se muestra el degradado con el título.`;
 const o=$("#ov");
 o.innerHTML=`<div class="modal" style="max-width:560px"><h2>🖼 Carátula de «${esc(g.n)}»</h2>
 <div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap">
  <div style="flex:0 0 auto">${prev}</div>
  <div style="flex:1;min-width:200px;display:flex;flex-direction:column;gap:8px">
   <button class="btn pri" id="cvpick">📁 Elegir imagen…</button>
   <button class="btn" id="cvfind">🔍 Buscar en internet</button>
   ${g.img?'<button class="btn" id="cvdel">🗑 Quitar carátula</button>':""}
   <button class="btn" id="cvclose">Cerrar</button>
  </div>
 </div>
 <p style="color:var(--mut);font-size:12.5px;line-height:1.45;margin:12px 0 0">${nota} PNG, JPG o WebP hasta 8 MB. Se guarda como <b>${esc(base)}.png/.jpg</b> en la carpeta del juego; el disco no se modifica.</p>
 <input type="file" id="cvin" accept="image/png,image/jpeg,image/webp" hidden></div>`;
 o.classList.add("on");
 const close=()=>o.classList.remove("on");
 $("#cvclose").onclick=close;
 $("#cvpick").onclick=()=>$("#cvin").click();
 $("#cvin").onchange=e=>{const f=e.target.files[0];if(!f)return;
  if(f.size>8000000)return toast("Imagen demasiado grande (máximo 8 MB)");
  toast("Guardando carátula…");
  fetch("/api/cover/upload?id="+cvFor,{method:"POST",body:f}).then(r=>r.json()).then(r=>{
   toast(r.ok?"Carátula guardada":r.error||"No se pudo guardar");if(r.ok)close();reload()}).catch(()=>toast("Error de red"))};
 $("#cvfind").onclick=()=>{close();coverSearch(cvFor)};
 if(g.img)$("#cvdel").onclick=()=>{
  if(!confirm("¿Quitar la carátula de «"+g.n+"»? Se borra solo la imagen; el juego no se toca."))return;
  jpost("/api/cover/remove",{id:g.id}).then(r=>{toast(r.ok?"Carátula quitada":r.error);if(r.ok)close();reload()})};
}
function coverSearch(gid){if(!API)return toast("Requiere el puente");const g=gm(gid||sel),o=$("#ov");if(!g)return;
 o.innerHTML=`<div class="modal" style="max-width:720px"><h2>Carátula: ${esc(g.n)}</h2><div id="cl2" style="color:var(--mut)">Buscando…</div><button class="btn" id="cl" style="width:100%;margin-top:12px">Cerrar</button></div>`;o.classList.add("on");$("#cl").onclick=()=>o.classList.remove("on");
 fetch("/api/cover/search?id="+g.id).then(r=>r.json()).then(j=>{const c=$("#cl2");if(!j.items.length){c.innerHTML='Sin resultados. Usa <b>📁 Elegir imagen…</b> para poner una tuya.';return}
  c.innerHTML=`<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px">${j.items.map((x,i)=>`<button class="card" data-ci="${i}"><img src="${esc(x.u)}" referrerpolicy="no-referrer" style="width:100%;aspect-ratio:3/4;object-fit:cover" alt=""><div class="cap">${esc(x.s)}<small>${esc(x.t)}</small></div></button>`).join("")}</div>`;
  c.querySelectorAll("[data-ci]").forEach(b=>b.onclick=()=>jpost("/api/cover/set",{id:g.id,url:j.items[+b.dataset.ci].u}).then(r=>{toast(r.ok?"Carátula guardada":r.error);o.classList.remove("on");reload()}))}).catch(()=>{$("#cl2").textContent="Error de red"})}
function coverUpload(e){const f=e.target.files[0];if(!f)return;fetch("/api/cover/upload?id="+sel,{method:"POST",body:f}).then(r=>r.json()).then(r=>{toast(r.ok?"Carátula guardada":r.error);reload()})}
function coverAll(){jpost("/api/cover/all").then(()=>{toast("Buscando carátulas…");pollCover()})}
function pollCover(){clearTimeout(pt);if(!API)return;fetch("/api/cover/progress").then(r=>r.json()).then(p=>{const e=$("#cvst");if(e&&(p.running||p.total))e.textContent=(p.running?"Buscando… ":"Listo: ")+p.done+"/"+p.total+" · encontradas "+p.found;if(p.found!==lastFound||p.imp!==lastImp){if(lastImp>=0&&p.imp>lastImp)toast("Nuevo juego importado: "+p.last);lastFound=p.found;lastImp=p.imp;reload()}if(p.running)pt=setTimeout(pollCover,2500)}).catch(()=>{})}
fetch("/api/games").then(r=>r.ok?r.json():Promise.reject()).then(j=>{API=true;pollCover();setInterval(pollCover,5000);G=j.games;recents=j.recents;FOLDER=j.carpeta||"";Object.assign(S,j.ajustes||{});if(!CFG.res.includes(S.res))S.res=CFG.res[0];if(!CFG.fil.includes(S.fil))S.fil=CFG.fil[0];if(!CFG.fs.includes(S.fs))S.fs=CFG.fs[0];sel=(G[0]||{}).id;renderAll();if(!G.length)toast("Carpeta de juegos vacía")}).catch(()=>renderAll());
</script>
</body>
</html>
'''

BASE = os.path.dirname(os.path.abspath(__file__))
CFG_PATH = os.path.join(BASE, "config.json")
DB_PATH = os.path.join(BASE, "datos.json")
EXT = {".hdi", ".nhd", ".thd", ".fdi", ".d88", ".88d", ".hdm", ".nfd", ".xdf",
       ".dup", ".tfd", ".d98", ".98d", ".hdd", ".fdd"}
IMG = (".png", ".jpg", ".jpeg", ".webp")
HDD_EXT = (".hdi", ".nhd", ".thd")   # imagenes de disco duro (IDE)
CD_EXT = (".iso", ".cue", ".ccd", ".mds", ".nrg", ".cdm")
LOCK = threading.Lock()


def _ini_del_emulador(exe):
    """Ruta del .ini que lee el emulador: junto al exe, con el nombre base del exe."""
    nombre = os.path.splitext(os.path.basename(exe))[0] + ".ini"
    return os.path.join(os.path.dirname(exe), nombre)


def _ini_fijar_claves(ruta_ini, claves):
    """Actualiza claves de la seccion [NekoProject21] conservando el resto del archivo.

    El emulador usa la primera aparicion de cada clave, asi que editamos el
    primer bloque de la seccion. Se trabaja a nivel de bytes para no alterar
    la codificacion original (ANSI) del resto del archivo.
    """
    data = b""
    if os.path.isfile(ruta_ini):
        with open(ruta_ini, "rb") as f:
            data = f.read()
    i = data.find(b"[NekoProject21]")
    if i < 0:
        if data and not data.endswith((b"\r", b"\n")):
            data += b"\r\n"
        data += b"[NekoProject21]\r\n"
        i = data.find(b"[NekoProject21]")
    j = data.find(b"\n[", i + 15)
    fin = len(data) if j < 0 else j + 1
    bloque = data[i:fin]
    for k, v in claves:
        linea = k.encode("ascii") + b"=" + v.encode("mbcs")
        m = re.search(rb"(?m)^" + re.escape(k.encode("ascii")) + rb"[ \t]*=.*$", bloque)
        if m:
            cr = b"\r" if m.group(0).endswith(b"\r") else b""
            bloque = bloque[:m.start()] + linea + cr + bloque[m.end():]
        else:
            nl = bloque.find(b"\n")
            bloque = bloque[:nl + 1] + linea + b"\r\n" + bloque[nl + 1:]
    data = data[:i] + bloque + data[fin:]
    with open(ruta_ini, "wb") as f:
        f.write(data)


def _preparar_hdd(exe, ruta_disco):
    """Configura el juego como HDD IDE 0 en el ini del emulador y limpia FDD."""
    ruta_ini = _ini_del_emulador(exe)
    if not os.path.isfile(ruta_ini):
        viejo = os.path.join(os.path.dirname(exe), "np21.ini")
        if os.path.isfile(viejo):
            shutil.copyfile(viejo, ruta_ini)   # migracion unica de ajustes
    bak = ruta_ini + ".bak"
    if os.path.isfile(ruta_ini) and not os.path.isfile(bak):
        shutil.copyfile(ruta_ini, bak)
    claves = [("HDD1FILE", ruta_disco), ("IDE1TYPE", "1")]
    for n in range(1, 5):                      # el HDD arranca solo si no hay disquete
        claves.append(("FDD%dFILE" % n, ""))
    _ini_fijar_claves(ruta_ini, claves)
    return ruta_ini


def _preparar_cd(exe, ruta_disco):
    """Configura el juego como CD-ROM IDE (unidad IDE2) en el ini del emulador."""
    ruta_ini = _ini_del_emulador(exe)
    if not os.path.isfile(ruta_ini):
        viejo = os.path.join(os.path.dirname(exe), "np21.ini")
        if os.path.isfile(viejo):
            shutil.copyfile(viejo, ruta_ini)
    bak = ruta_ini + ".bak"
    if os.path.isfile(ruta_ini) and not os.path.isfile(bak):
        shutil.copyfile(ruta_ini, bak)
    claves = [("IDE2TYPE", "2"), ("CD2_FILE", ruta_disco)]
    _ini_fijar_claves(ruta_ini, claves)
    return ruta_ini
COVERS = {}


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_emulator():
    for pat in ("np2kai*.exe", "np21kai*.exe", "np2*.exe", "np21*.exe",
                "*/np2kai*.exe", "*/np21kai*.exe", "*/np2*.exe", "*/np21*.exe"):
        for p in glob.glob(os.path.join(BASE, pat)):
            if "puente" not in os.path.basename(p).lower():
                return p
    return ""


def config():
    c = load(CFG_PATH, None)
    if c is None:
        c = {"emulador": find_emulator(), "carpeta_juegos": "juegos", "puerto": 8098}
        save(CFG_PATH, c)
    return c


def games_dir(c):
    d = c.get("carpeta_juegos", "juegos")
    return d if os.path.isabs(d) else os.path.join(BASE, d)


def scan():
    c, db = config(), load(DB_PATH, {})
    root = games_dir(c)
    os.makedirs(root, exist_ok=True)
    favs, played, meta = set(db.get("fav", [])), db.get("jugado", {}), db.get("meta", {})
    out = []
    COVERS.clear()
    for dp, _, files in os.walk(root):
        for fn in sorted(files):
            stem, ext = os.path.splitext(fn)
            if ext.lower() not in EXT:
                continue
            full = os.path.join(dp, fn)
            gid = hashlib.md5(os.path.relpath(full, root).lower().encode()).hexdigest()[:10]
            h = int(gid, 16) % 360
            m = meta.get(gid) or meta.get(fn, {})
            g = {"id": gid, "n": m.get("n") or stem, "t": m.get("t") or stem,
                 "g": m.get("g") or "Sin clasificar", "m": m.get("m") or "PC-98",
                 "s": round(os.path.getsize(full) / 1048576, 1),
                 "p": played.get(gid, 0), "fav": 1 if gid in favs else 0,
                 "c": f"linear-gradient(160deg,hsl({h},55%,30%),hsl({(h + 50) % 360},60%,60%))",
                 "d": m.get("d") or f"Disco: {fn}", "path": full,
                 "custom": 1 if gid in meta else 0}
            for e in IMG:
                cp = os.path.join(dp, stem + e)
                if os.path.exists(cp):
                    COVERS[gid] = cp
                    g["img"] = f"/covers/{gid}"
                    break
            out.append(g)
    return out


def api_games():
    gs = scan()
    ids = {g["id"] for g in gs}
    db = load(DB_PATH, {})
    rec = [i for i in db.get("recientes", []) if i in ids]
    out = []
    for g in gs:
        item = {k: v for k, v in g.items() if k != "path"}
        item["file"] = os.path.basename(g["path"])
        item["dir"] = os.path.dirname(g["path"])
        item["bytes"] = os.path.getsize(g["path"])
        item["mtime"] = int(os.path.getmtime(g["path"]))
        out.append(item)
    return {"games": out, "recents": rec, "ajustes": db.get("ajustes", {}),
            "carpeta": games_dir(config())}


def api_play(gid):
    c = config()
    exe = c.get("emulador", "")
    if not exe or not os.path.isfile(exe):
        return {"ok": False, "error": "Falta la ruta de np2kai.exe en config.json"}
    g = next((x for x in scan() if x["id"] == gid), None)
    if not g:
        return {"ok": False, "error": "Juego no encontrado"}
    db0 = load(DB_PATH, {})
    perfil = db0.get("perfiles", {}).get(gid) or db0.get("ajustes", {})
    _, ign = aplicar_perfil(perfil)
    ext = os.path.splitext(g["path"])[1].lower()
    try:
        if ext in HDD_EXT:
            _preparar_hdd(exe, g["path"])          # .hdi/.nhd/.thd -> HDD IDE 0
        elif ext in CD_EXT:
            _preparar_cd(exe, g["path"])           # .iso/.cue/... -> CD-ROM IDE
        subprocess.Popen([exe], cwd=os.path.dirname(exe))
    except Exception as e:
        return {"ok": False, "error": f"No se pudo abrir el emulador: {e}"}
    with LOCK:
        db = load(DB_PATH, {})
        db.setdefault("jugado", {})[gid] = db.get("jugado", {}).get(gid, 0) + 1
        db["recientes"] = [gid] + [i for i in db.get("recientes", []) if i != gid][:11]
        save(DB_PATH, db)
    r = {"ok": True}
    if ign:
        r["nota"] = "NP21/W no admite " + ", ".join(ign)
    return r


def api_fav(gid, fav):
    with LOCK:
        db = load(DB_PATH, {})
        s = set(db.get("fav", []))
        (s.add if fav else s.discard)(gid)
        db["fav"] = sorted(s)
        save(DB_PATH, db)
    return {"ok": True}


CAMPOS = {"n": 120, "t": 120, "g": 60, "m": 60, "d": 600}


def limpiar(v, n):
    """Quita saltos y caracteres de control; recorta al largo permitido."""
    return re.sub(r"[\x00-\x1f]", " ", str(v or "")).strip()[:n]


def api_meta(gid, data):
    """Guarda los datos editables de un juego. Los campos vacios vuelven al valor por defecto."""
    g = next((x for x in scan() if x["id"] == gid), None)
    if not g:
        return {"ok": False, "error": "Juego no encontrado"}
    data = data or {}
    campos = {k: limpiar(data.get(k), n) for k, n in CAMPOS.items()}
    with LOCK:
        db = load(DB_PATH, {})
        meta = db.setdefault("meta", {})
        meta.pop(os.path.basename(g["path"]), None)  # entrada vieja por nombre de archivo
        if any(campos.values()):
            meta[gid] = {k: v for k, v in campos.items() if v}
        else:
            meta.pop(gid, None)
        save(DB_PATH, db)
    return {"ok": True, "datos": campos, "personalizado": 1 if any(campos.values()) else 0}


def api_reveal(gid):
    """Abre el Explorador con el disco seleccionado."""
    g = next((x for x in scan() if x["id"] == gid), None)
    if not g:
        return {"ok": False, "error": "Juego no encontrado"}
    try:
        subprocess.Popen(f'explorer /select,"{os.path.normpath(g["path"])}"')
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


_NPROC = {"prev": {}}
INVALID_HANDLE = (1 << 64) - 1
# np21nt_x64.exe, np2kai.exe, np21w.exe… pero no np2debug-mcp-server.exe
PROC_RE = re.compile(r"^np2[0-9a-z_]*(?:\.exe)?$", re.I)


def _win_procs(extra=()):
    """Lista (pid, nombre) de los procesos que son el emulador NP2/NP21."""
    import ctypes
    from ctypes import wintypes as wt

    class PE(ctypes.Structure):
        _fields_ = [("dwSize", wt.DWORD), ("cntUsage", wt.DWORD), ("th32ProcessID", wt.DWORD),
                    ("th32DefaultHeapID", ctypes.c_size_t), ("th32ModuleID", wt.DWORD),
                    ("cntThreads", wt.DWORD), ("th32ParentProcessID", wt.DWORD),
                    ("pcPriClassBase", ctypes.c_long), ("dwFlags", wt.DWORD),
                    ("szExeFile", ctypes.c_char * 260)]

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.CreateToolhelp32Snapshot.restype = wt.HANDLE
    k32.CreateToolhelp32Snapshot.argtypes = [wt.DWORD, wt.DWORD]
    k32.Process32First.argtypes = [wt.HANDLE, ctypes.POINTER(PE)]
    k32.Process32Next.argtypes = [wt.HANDLE, ctypes.POINTER(PE)]
    snap = k32.CreateToolhelp32Snapshot(0x2, 0)  # TH32CS_SNAPPROCESS
    if not snap or snap == INVALID_HANDLE:
        return []
    out = []
    extra = {x.lower() for x in extra if x}
    try:
        e = PE()
        e.dwSize = ctypes.sizeof(e)
        ok = k32.Process32First(snap, ctypes.byref(e))
        while ok:
            nm = e.szExeFile.decode("mbcs", "ignore")
            if PROC_RE.match(nm) or nm.lower() in extra:
                out.append((int(e.th32ProcessID), nm))
            ok = k32.Process32Next(snap, ctypes.byref(e))
    finally:
        k32.CloseHandle(snap)
    return out


def _proc_stats(pid):
    """Tiempo de CPU acumulado (s) y memoria residente (MB) de un proceso."""
    import ctypes
    from ctypes import wintypes as wt

    class PMC(ctypes.Structure):
        _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    h = 0
    for acc in (0x1000, 0x400):  # QUERY_LIMITED_INFORMATION, QUERY_INFORMATION
        h = k32.OpenProcess(acc, False, pid)
        if h:
            break
    if not h:
        return None
    try:
        c, ex, k, u = (wt.FILETIME() for _ in range(4))
        if not k32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(ex), ctypes.byref(k), ctypes.byref(u)):
            return None
        ft = lambda f: (f.dwHighDateTime << 32) | f.dwLowDateTime
        cpu = (ft(k) + ft(u)) / 1e7
        pmc = PMC()
        pmc.cb = ctypes.sizeof(pmc)
        ram = None
        if psapi.GetProcessMemoryInfo(h, ctypes.byref(pmc), pmc.cb):
            ram = pmc.WorkingSetSize / 1048576
        return {"cpu": cpu, "ram": ram}
    finally:
        k32.CloseHandle(h)


def api_proc():
    """CPU y RAM reales del emulador. El FPS no se puede leer desde fuera."""
    if os.name != "nt":
        return {"running": False, "error": "solo Windows"}
    try:
        procs = _win_procs([os.path.basename(config().get("emulador", ""))])
    except Exception as e:
        return {"running": False, "error": str(e)}
    if not procs:
        _NPROC["prev"] = {}
        return {"running": False, "cpu": None, "ram": None, "names": [], "pid": None}
    ahora = time.time()
    prev, nuevo = _NPROC["prev"], {}
    cpus, rams, nombres, medido = 0.0, 0.0, [], True
    for pid, nm in procs:
        st = _proc_stats(pid)
        if not st:
            continue
        nombres.append(nm)
        if st["ram"] is not None:
            rams += st["ram"]
        p = prev.get(pid)
        if p and ahora - p[0] < 0.2:  # demasiado pronto: reutiliza la última medición
            nuevo[pid] = p
            if p[2] is None:
                medido = False
            else:
                cpus += p[2]
            continue
        pct = None
        if p:
            pct = max(0.0, (st["cpu"] - p[1]) / (ahora - p[0]) / max(1, os.cpu_count() or 1) * 100)
            cpus += pct
        else:
            medido = False
        nuevo[pid] = (ahora, st["cpu"], pct)
    _NPROC["prev"] = nuevo
    return {"running": bool(nombres), "cpu": round(cpus, 1) if nombres and medido else None,
            "ram": round(rams, 1) if rams else None, "names": nombres,
            "pid": procs[0][0] if len(procs) == 1 else None}


def api_cfg(aj):
    with LOCK:
        db = load(DB_PATH, {})
        db["ajustes"] = aj
        save(DB_PATH, db)
    return {"ok": True}


INI = "np21.ini"


def ini_file():
    exe = config().get("emulador", "")
    return os.path.join(os.path.dirname(exe) if exe else BASE, INI)


def ini_load():
    p = ini_file()
    if not os.path.isfile(p):
        return None, ""
    with open(p, "rb") as f:
        raw = f.read()
    txt = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8", "ignore")
    return p, txt


def ini_set(txt, pares):
    """Cambia clave=valor sin tocar el resto del ini (orden, secciones y comentarios)."""
    lineas = txt.replace("\r\n", "\n").split("\n")
    for k, v in pares.items():
        kl, hecho = k.lower(), False
        for i, l in enumerate(lineas):
            if "=" in l and l.split("=", 1)[0].strip().lower() == kl:
                lineas[i] = l.split("=", 1)[0].strip() + "=" + str(v)
                hecho = True
        if not hecho:
            for i, l in enumerate(lineas):
                if l.strip().lower() == "[nekoproject21]":
                    lineas.insert(i + 1, k + "=" + str(v))
                    break
    return "\n".join(lineas)


def aplicar_perfil(p):
    """Escribe en np21.ini solo lo que NP21/W admite. Devuelve (aplicado, ignorado)."""
    ruta, txt = ini_load()
    if not ruta:
        return [], ["no encuentro np21.ini junto al emulador"]
    pares = {}
    pares["SampleHz"] = "44100" if p.get("aud", True) else "22050"
    fs = str(p.get("fs", "Automático"))
    if fs in ("Automático", "Desactivado"):
        pares["DispSync"], pares["SkpFrame"] = "true", "0"
    else:
        pares["DispSync"], pares["SkpFrame"] = "false", fs
    fil = p.get("fil", "Ninguno")
    pares["skipline"] = "true" if fil == "Scanlines" else "false"
    if fil == "Scanlines":
        pares["skplight"] = "64"
    ign = []
    if fil not in ("Ninguno", "Scanlines"):
        ign.append("filtro " + fil)
    res = str(p.get("res", "Auto (Nativo)"))
    if res != "Auto (Nativo)":
        ign.append("resolución " + res)
    try:
        if not os.path.exists(ruta + ".bak"):
            shutil.copy2(ruta, ruta + ".bak")
        with open(ruta, "wb") as f:
            f.write(b"\xff\xfe" + ini_set(txt, pares).replace("\n", "\r\n").encode("utf-16-le"))
    except Exception as e:
        return [], [str(e)]
    return sorted(pares), ign


def api_perfil(gid, cfg):
    with LOCK:
        db = load(DB_PATH, {})
        pf = db.setdefault("perfiles", {})
        if cfg:
            pf[gid] = cfg
        else:
            pf.pop(gid, None)
        save(DB_PATH, db)
    return {"ok": True}


def pick_folder():
    """Abre el selector nativo de carpetas de Windows y devuelve la ruta elegida."""
    ps = ("Add-Type -AssemblyName System.Windows.Forms;"
          "$d=New-Object System.Windows.Forms.FolderBrowserDialog;"
          "$d.Description='Elige la carpeta con tus discos PC-98 (.hdi, .fdi, .d88...)';"
          "if($d.ShowDialog() -eq 'OK'){[Console]::Out.Write($d.SelectedPath)}")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-STA", "-Command", ps],
                           capture_output=True, text=True, timeout=600,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return r.stdout.strip()
    except Exception:
        return ""


def api_folder(path=""):
    """Cambia la carpeta de juegos: con ruta o abriendo el selector del sistema."""
    path = (path or "").strip().strip('"')
    if not path:
        path = pick_folder()
        if not path:
            return {"ok": False, "error": "No se eligio ninguna carpeta"}
    path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
    if not os.path.isdir(path):
        return {"ok": False, "error": "Esa carpeta no existe: " + path}
    with LOCK:
        c = load(CFG_PATH, {})
        c["carpeta_juegos"] = path
        save(CFG_PATH, c)
    return {"ok": True, "carpeta": path, "juegos": len(scan())}


def api_open_folder():
    d = games_dir(config())
    try:
        os.startfile(d)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


UA = "Mozilla/5.0 (X11; PC98Launcher) AppleWebKit/537.36"
SITES = {"myabandonware": ("https://www.myabandonware.com/browse/platform/pc98/?pl%5B0%5D=pc98", "/game/"),
         "romsfun": ("https://romsfun.com/roms/nec-pc-9801/", "nec-pc-9801")}
CAT = {}
JOB = {"running": False, "done": 0, "total": 0, "found": 0, "imp": 0, "last": ""}
PORT = 8098


def http(url, timeout=12):
    rq = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,ja;q=0.8"})
    with urllib.request.urlopen(rq, timeout=timeout) as r:
        return r.read(12_000_000)


def parse_cards(page, base, key, limit=60):
    """Extrae (titulo, enlace, imagen) de cualquier <a href> que contenga <img>."""
    out, seen = [], set()
    for m in re.finditer(r'<a\b[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', page, re.S | re.I):
        href = urljoin(base, html.unescape(m.group(1)))
        im = re.search(r"<img\b[^>]*>", m.group(2), re.I)
        if key not in href or not im or href in seen or href.rstrip("/") == base.rstrip("/"):
            continue
        tag = im.group(0)
        s = re.search(r'data-(?:lazy-)?src="([^"]+)"', tag) or re.search(r'\ssrc="([^"]+)"', tag)
        if not s or s.group(1).startswith("data:"):
            continue
        a = re.search(r'alt="([^"]*)"', tag)
        t = html.unescape(a.group(1)).strip() if a and a.group(1).strip() else re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
        seen.add(href)
        out.append({"t": t or href.rstrip("/").rsplit("/", 1)[-1], "u": href,
                    "i": urljoin(base, html.unescape(s.group(1))).replace("'", "%27")})
        if len(out) >= limit:
            break
    return out


def api_catalog(site):
    if site not in SITES:
        return {"items": [], "error": "Sitio desconocido."}
    hit = CAT.get(site)
    if hit and time.time() - hit[0] < 600:
        return {"items": hit[1]}
    url, key = SITES[site]
    try:
        page = http(url).decode("utf-8", "ignore")
        items = parse_cards(page, url, key)
    except Exception as e:
        return {"items": [], "error": f"No se pudo leer el sitio ({e})."}
    items = [{"t": html.escape(x["t"]), "u": html.escape(x["u"], quote=True), "i": x["i"]} for x in items]
    if items:
        CAT[site] = (time.time(), items)
    return {"items": items, "error": "" if items else "No se encontraron juegos (el sitio puede bloquear lectores automáticos)."}


RUIDO = {"complete", "pack", "collection", "translated", "translation", "traduccion",
         "espanol", "español", "spanish", "castellano", "english", "ingles", "japanese",
         "japones", "jap", "jpn", "jp", "eng", "esp", "es", "usa", "japan", "fan", "patch",
         "parche", "rip", "iso", "bin", "cue", "zip", "disk", "disco", "version", "pc",
         "pc98", "98", "9801", "9821", "hdi", "fdi", "d88", "nhd", "thd", "hdm"}


CJK = "\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f"


def clean(n):
    """Quita etiquetas de edición del nombre del archivo para buscar el título real."""
    n = unicodedata.normalize("NFKC", n or "")          # ３ -> 3, （） -> ( )
    n = re.sub(r"[\[\(【〔《].*?[\]\)】〕》]", " ", n)
    n = re.sub(r"[_.\-]+", " ", n)
    toks = [t for t in n.split() if t]
    keep = [t for t in toks if t.lower() not in RUIDO]
    return " ".join(keep or toks).strip()


def tokens(s):
    """Palabras latinas y sílabas japonesas (bigramas) para poder comparar títulos en japonés."""
    s = unicodedata.normalize("NFKC", s or "").lower()
    out = set(re.findall(r"[a-z0-9]+", s))
    for run in re.findall("[" + CJK + "]+", s):
        if len(run) == 1:
            out.add(run)
        else:
            out.update(run[i:i + 2] for i in range(len(run) - 1))
    return out


def sim(a, b):
    A = tokens(clean(a))
    B = tokens(b)
    return len(A & B) / len(A) if A else 0


def parecido(a, b):
    """Cuánto del nombre buscado aparece en el título. Con una sola palabra exige que el título sea corto."""
    A = tokens(clean(a))
    B = tokens(b)
    if not A or not B:
        return 0.0
    inter = len(A & B)
    cob = inter / len(A)
    if len(A) == 1:
        return min(cob, inter / len(B))
    return cob


def score(nombre, it):
    """Probabilidad de que el resultado sea el juego buscado (usa la consulta que lo encontró)."""
    return max(parecido(nombre, it["t"]), parecido(it["q"], it["t"]) if it.get("q") else 0.0)


def orden(nombre, it):
    """Mejor primero: el arte de caja de LaunchBox manda, luego el parecido del título."""
    return (1 if it.get("s") == "LaunchBox" else 0, score(nombre, it))


TAIL = {"for", "windows", "win", "version", "ver", "edition", "download", "free", "plus", "cd"}
ROMANOS = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def romanizar(t):
    """Variantes latinas de un título ajeno: '…Lakers 3' -> ['…Lakers III', '…Lakers 3']."""
    t = re.sub(r"[\[\(【〔《].*?[\]\)】〕》]", " ", unicodedata.normalize("NFKC", t or ""))
    ws = [w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'&!+\-]*", t) if w.lower() not in RUIDO]
    while ws and ws[-1].lower() in TAIL:
        ws.pop()
    if not ws or not re.search(r"[A-Za-z]{3}", " ".join(ws)):
        return []
    q = " ".join(ws)
    out = [q]
    if len(ws) >= 3 and ws[-1].isdigit() and 1 <= int(ws[-1]) <= 10:
        out.insert(0, " ".join(ws[:-1] + [ROMANOS[int(ws[-1])]]))
    return out


LBCACHE = {}


def lb_box(h):
    """Arte de caja frontal más grande del payload Nuxt del detalle de LaunchBox."""
    i = h.find("__NUXT_DATA__")
    if i < 0:
        return ""
    j = h.find(">", i) + 1
    k = h.find("</script>", j)
    if k < j:
        return ""
    data = html.unescape(h[j:k])
    best, area = "", 0
    for m in re.finditer(r'"Box - Front"', data):
        frag = data[m.end():m.end() + 400]
        f = re.search(r'"([0-9a-f\-]{36}\.(?:jpg|jpeg|png))"', frag)
        if not f:
            continue
        nums = re.findall(r"\b(\d+)\b", frag[f.end():f.end() + 40])
        a = int(nums[1]) * int(nums[2]) if len(nums) >= 3 else 0
        if a >= area:
            best, area = f.group(1), a
    return "https://images.launchbox-app.com//" + best if best else ""


def launchbox(q, paginas=2):
    """Carátulas de caja reales de LaunchBox Games Database (solo entiende títulos latinos)."""
    hit = LBCACHE.get(q)
    if hit and time.time() - hit[0] < 3600:
        return list(hit[1])
    url = "https://gamesdb.launchbox-app.com/games/results/" + quote(q) + "?searchText=" + quote(q)
    page = http(url).decode("utf-8", "ignore")
    ids, vistos = [], set()
    for i, s in re.findall(r'/games/details/([0-9]+)-([a-z0-9\-]+)', page):
        if i not in vistos:
            vistos.add(i)
            ids.append(i + "-" + s)
        if len(ids) >= paginas:
            break
    out = []
    for aid in ids:
        try:
            h = http("https://gamesdb.launchbox-app.com/games/details/" + aid).decode("utf-8", "ignore")
        except Exception:
            continue
        t = re.search(r"<title>([^<]+)</title>", h)
        t = html.unescape(t.group(1)).replace(" - LaunchBox Games Database", "").strip() if t else ""
        box = lb_box(h)
        if box:
            out.append({"u": box, "s": "LaunchBox", "t": t or aid})
    LBCACHE[q] = (time.time(), out)
    return list(out)


def wiki(lang, q):
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrsearch": q, "gsrlimit": 5,
        "prop": "pageimages", "piprop": "thumbnail", "pithumbsize": 500})
    pages = json.loads(http(url)).get("query", {}).get("pages", {}).values()
    return [{"u": p["thumbnail"]["source"], "s": "Wikipedia " + lang, "t": p["title"]}
            for p in sorted(pages, key=lambda p: p.get("index", 99)) if "thumbnail" in p]


def mabw(q):
    base = "https://www.myabandonware.com/"
    page = http(base + "search/q/" + quote(q)).decode("utf-8", "ignore")
    return [{"u": c["i"], "s": "MyAbandonware", "t": c["t"]} for c in parse_cards(page, base, "/game/", 5)]


def archive(q):
    url = "https://archive.org/advancedsearch.php?" + urlencode({
        "q": f"title:({q}) AND mediatype:(software OR texts OR image)", "fl[]": ["identifier", "title"],
        "rows": 5, "output": "json"}, doseq=True)
    docs = json.loads(http(url)).get("response", {}).get("docs", [])
    return [{"u": "https://archive.org/services/img/" + d["identifier"], "s": "Internet Archive",
             "t": d["title"][0] if isinstance(d.get("title"), list) else d.get("title", "")} for d in docs]


def search_covers(g):
    """Busca por el nombre limpio y, si no hay nada bueno, por sus primeras palabras."""
    base = clean(g["n"])
    toks = base.split()
    variantes = [base]
    if len(toks) > 3:
        variantes.append(" ".join(toks[:3]))
    if len(toks) > 2:
        variantes.append(" ".join(toks[:2]))
    out, vistos = [], set()

    def push(items):
        for it in items:
            if it["u"] not in vistos:
                vistos.add(it["u"])
                out.append(it)

    for q in variantes:
        if not q:
            continue
        for fn, a in ((wiki, ("en", q + " PC-98")), (wiki, ("ja", q)), (mabw, (q,)), (archive, (q,))):
            try:
                items = fn(*a)
            except Exception:
                items = []
            push(items)
        if any(parecido(base, x["t"]) >= 0.6 for x in out):
            break

    # LaunchBox solo entiende títulos latinos: se prueba el nombre propio y, si el
    # nombre es japonés, uno romanizado sacado de los títulos que aparecieron arriba.
    consultas = [base] if re.search(r"[A-Za-z]{3}", base) else []
    for it in out:
        for q in romanizar(it["t"]):
            if q not in consultas:
                consultas.append(q)
    for q in consultas[:3]:
        try:
            items = launchbox(q)
        except Exception:
            items = []
        for it in items:
            it["q"] = q
        push(items)
        if any(score(base, x) >= 0.6 for x in items):
            break
    return sorted(out, key=lambda x: orden(base, x), reverse=True)


MARCAS = {"8680bb925ed3e9766ba1fe08f676ae17"}  # logo genérico que devuelve Internet Archive


def save_cover(g, data):
    if len(data) > 8_000_000:
        raise ValueError("Imagen demasiado grande")
    ext = (".png" if data[:4] == b"\x89PNG" else ".jpg" if data[:2] == b"\xff\xd8"
           else ".webp" if data[:4] == b"RIFF" and data[8:12] == b"WEBP" else None)
    if not ext:
        raise ValueError("Formato de imagen no valido (usa png, jpg o webp)")
    if hashlib.md5(data).hexdigest() in MARCAS:
        raise ValueError("Esa web no tiene carátula para el juego (devolvió su logo)")
    stem = os.path.splitext(g["path"])[0]
    for e in IMG:
        if os.path.exists(stem + e):
            os.remove(stem + e)
    with open(stem + ext, "wb") as f:
        f.write(data)


def find(gid):
    return next((x for x in scan() if x["id"] == gid), None)


def api_cover_search(gid):
    g = find(gid)
    return {"items": search_covers(g)[:16] if g else []}


def api_cover_set(gid, url):
    g = find(gid)
    if not g or not url.startswith(("http://", "https://")):
        return {"ok": False, "error": "Solicitud no valida"}
    try:
        save_cover(g, http(url))
    except Exception as e:
        return {"ok": False, "error": str(e)}
    con_caratula(gid)
    return {"ok": True}


def api_cover_upload(gid, raw):
    g = find(gid)
    if not g:
        return {"ok": False, "error": "Juego no encontrado"}
    try:
        save_cover(g, raw)
    except Exception as e:
        return {"ok": False, "error": str(e)}
    con_caratula(gid)
    return {"ok": True}


def con_caratula(gid):
    """Un juego con carátula deja de estar en la lista de pendientes."""
    with LOCK:
        db = load(DB_PATH, {})
        s = db.get("sin_caratula", [])
        if gid in s:
            db["sin_caratula"] = [x for x in s if x != gid]
            save(DB_PATH, db)


def api_cover_remove(gid):
    """Borra el archivo de carátula (no el juego) y evita que la búsqueda automática lo reponga."""
    g = find(gid)
    if not g:
        return {"ok": False, "error": "Juego no encontrado"}
    stem = os.path.splitext(g["path"])[0]
    quitados = []
    for e in IMG:
        p = stem + e
        if os.path.exists(p):
            try:
                os.remove(p)
                quitados.append(os.path.basename(p))
            except Exception as ex:
                return {"ok": False, "error": "No se pudo borrar: " + str(ex)}
    COVERS.pop(gid, None)
    with LOCK:
        db = load(DB_PATH, {})
        s = set(db.get("sin_caratula", []))
        s.add(gid)
        db["sin_caratula"] = sorted(s)
        save(DB_PATH, db)
    return {"ok": True, "quitados": quitados}


def cover_job(force):
    if JOB["running"]:
        return
    JOB["running"] = True

    def run():
        db = load(DB_PATH, {})
        skip = set() if force else set(db.get("sin_caratula", []))
        gs = [g for g in scan() if "img" not in g and g["id"] not in skip]
        JOB.update(done=0, total=len(gs), found=0)
        miss = set(db.get("sin_caratula", [])) if not force else set()
        for g in gs:
            try:
                cands = [x for x in search_covers(g) if score(g["n"], x) >= 0.6]
                best = max(cands, key=lambda x: orden(g["n"], x)) if cands else None
                if best:
                    save_cover(g, http(best["u"]))
                    JOB["found"] += 1
                    miss.discard(g["id"])
                else:
                    miss.add(g["id"])
            except Exception:
                miss.add(g["id"])
            JOB["done"] += 1
        with LOCK:
            db = load(DB_PATH, {})
            db["sin_caratula"] = sorted(miss)
            save(DB_PATH, db)
        JOB["running"] = False

    threading.Thread(target=run, daemon=True).start()


def api_import(name, data):
    root = games_dir(config())
    os.makedirs(root, exist_ok=True)
    name = os.path.basename(name)
    ext, added = os.path.splitext(name)[1].lower(), []
    if ext in EXT:
        with open(os.path.join(root, name), "wb") as f:
            f.write(data)
        return {"ok": True, "added": [name]}
    if ext != ".zip":
        return {"ok": False, "error": "Solo .zip o discos (.hdi, .fdi, .d88...). Si es .7z/.lzh, extraelo antes."}
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except Exception:
        return {"ok": False, "error": "Zip danado o no valido"}
    if sum(i.file_size for i in z.infolist()) > 600_000_000:
        return {"ok": False, "error": "Zip demasiado grande"}
    sub = os.path.join(root, os.path.splitext(name)[0])
    for i in z.infolist():
        fn, e = os.path.basename(i.filename), os.path.splitext(i.filename)[1].lower()
        if i.is_dir() or not fn or (e not in EXT and e not in IMG):
            continue
        os.makedirs(sub, exist_ok=True)
        with z.open(i) as s, open(os.path.join(sub, fn), "wb") as d:
            shutil.copyfileobj(s, d)
        if e in EXT:
            added.append(fn)
    if not added:
        return {"ok": False, "error": "El zip no contiene discos reconocidos (.hdi, .fdi, .d88...)."}
    return {"ok": True, "added": added}


TMP_EXT = (".crdownload", ".part", ".tmp", ".download", ".opdownload")


def watch(c, t0):
    """Vigila la carpeta de Descargas: importa solos los .zip / discos que termines de bajar."""
    d = c.get("carpeta_descargas") or os.path.join(os.path.expanduser("~"), "Downloads")
    seen, pend = {}, False
    done = set(load(DB_PATH, {}).get("importados", []))
    while True:
        time.sleep(2)
        try:
            names = os.listdir(d)
        except Exception:
            continue
        for fn in names:
            try:
                ext = os.path.splitext(fn)[1].lower()
                full = os.path.join(d, fn)
                if (ext not in EXT and ext != ".zip") or not os.path.isfile(full):
                    continue
                st = os.stat(full)
                sig = f"{fn}|{st.st_size}|{int(st.st_mtime)}"
                if st.st_mtime < t0 or sig in done or st.st_size > 700_000_000:
                    continue
                prev = seen.get(full)
                if not prev or prev[0] != st.st_size:
                    seen[full] = (st.st_size, time.time())
                    continue
                if time.time() - prev[1] < 3:
                    continue
                with open(full, "rb") as f:
                    r = api_import(fn, f.read())
                done.add(sig)
                with LOCK:
                    db = load(DB_PATH, {})
                    db["importados"] = sorted(done)[-500:]
                    save(DB_PATH, db)
                if r.get("ok"):
                    JOB["last"] = ", ".join(r["added"][:2])
                    JOB["imp"] += 1
                    pend = True
            except Exception:
                pass
        if pend and not JOB["running"]:
            cover_job(False)
            pend = False


def page():
    """Si hay un index.html junto al script lo usa (para cambiar de diseño); si no, la interfaz incluida."""
    ext = os.path.join(BASE, "index.html")
    if os.path.isfile(ext):
        with open(ext, "rb") as f:
            return f.read()
    return INDEX_HTML.encode("utf-8")


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="application/json; charset=utf-8"):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def safe(self):
        ok = (f"127.0.0.1:{PORT}", f"localhost:{PORT}")
        o = self.headers.get("Origin")
        return self.headers.get("Host") in ok and (not o or o in ("http://" + h for h in ok))

    def do_GET(self):
        if not self.safe():
            return self.send(403, {"error": "origen no permitido"})
        u = urlparse(self.path)
        p, q = unquote(u.path), parse_qs(u.query)
        if p in ("/", "/index.html"):
            return self.send(200, page(), "text/html; charset=utf-8")
        if p == "/api/games":
            return self.send(200, api_games())
        if p == "/api/proc":
            return self.send(200, api_proc())
        if p == "/api/catalog":
            return self.send(200, api_catalog(q.get("site", [""])[0]))
        if p == "/api/cover/search":
            return self.send(200, api_cover_search(q.get("id", [""])[0]))
        if p == "/api/cover/progress":
            return self.send(200, dict(JOB))
        if p.startswith("/covers/"):
            cp = COVERS.get(p[8:])
            if cp and os.path.exists(cp):
                ct = "image/" + ("jpeg" if cp.lower().endswith((".jpg", ".jpeg")) else cp.rsplit(".", 1)[1].lower())
                with open(cp, "rb") as f:
                    return self.send(200, f.read(), ct)
        self.send(404, {"error": "no encontrado"})

    def do_POST(self):
        if not self.safe():
            return self.send(403, {"ok": False, "error": "origen no permitido"})
        try:
            u = urlparse(self.path)
            p, q = u.path, parse_qs(u.query)
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            if p == "/api/import":
                return self.send(200, api_import(q.get("name", [""])[0], raw))
            if p == "/api/cover/upload":
                return self.send(200, api_cover_upload(q.get("id", [""])[0], raw))
            d = json.loads(raw or b"{}")
            if p == "/api/play":
                return self.send(200, api_play(d.get("id", "")))
            if p == "/api/fav":
                return self.send(200, api_fav(d.get("id", ""), d.get("fav")))
            if p == "/api/config":
                return self.send(200, api_cfg(d.get("ajustes", {})))
            if p == "/api/folder":
                return self.send(200, api_folder(d.get("path", "")))
            if p == "/api/perfil":
                return self.send(200, api_perfil(d.get("id", ""), d.get("cfg")))
            if p == "/api/meta":
                return self.send(200, api_meta(d.get("id", ""), d.get("data")))
            if p == "/api/reveal":
                return self.send(200, api_reveal(d.get("id", "")))
            if p == "/api/cover/remove":
                return self.send(200, api_cover_remove(d.get("id", "")))
            if p == "/api/openfolder":
                return self.send(200, api_open_folder())
            if p == "/api/cover/set":
                return self.send(200, api_cover_set(d.get("id", ""), d.get("url", "")))
            if p == "/api/cover/all":
                cover_job(True)
                return self.send(200, {"ok": True})
        except Exception as e:
            return self.send(500, {"ok": False, "error": str(e)})
        self.send(404, {"error": "no encontrado"})


if __name__ == "__main__":
    c = config()
    PORT = int(os.environ.get("PC98_PORT") or c.get("puerto", 8098))
    print("Emulador :", c.get("emulador") or "(NO configurado: edita config.json)")
    print("Juegos   :", games_dir(c))
    print(f"Interfaz : http://127.0.0.1:{PORT}  (Ctrl+C para cerrar)")
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    if c.get("caratulas_automaticas", True):
        cover_job(False)
    if c.get("vigilar_descargas", True):
        threading.Thread(target=watch, args=(c, time.time()), daemon=True).start()
        print("Vigilando:", c.get("carpeta_descargas") or os.path.join(os.path.expanduser("~"), "Downloads"))
    threading.Timer(0.8, lambda: webbrowser.open(f"http://127.0.0.1:{PORT}")).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
