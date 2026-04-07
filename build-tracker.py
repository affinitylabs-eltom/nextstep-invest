import json, base64, os

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, 'investors_data.json'), 'r', encoding='utf-8') as f:
    investors = json.load(f)

b64 = base64.b64encode(json.dumps(investors, ensure_ascii=False).encode('utf-8')).decode('ascii')

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NextStep Outreach Tracker</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0f1117;color:#e1e4e8}
.hdr{padding:24px 32px;border-bottom:1px solid #21262d;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
.hdr h1{font-size:20px;font-weight:600}
.stats{display:flex;gap:12px;font-size:13px;color:#8b949e}
.stat{background:#161b22;padding:6px 12px;border-radius:6px}
.stat strong{color:#e1e4e8}
.fbar{padding:16px 32px;border-bottom:1px solid #21262d;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.fb{padding:6px 14px;border-radius:20px;border:1px solid #30363d;background:transparent;color:#8b949e;cursor:pointer;font-size:13px}
.fb:hover{border-color:#58a6ff;color:#58a6ff}
.fb.on{background:#58a6ff;color:#fff;border-color:#58a6ff}
.sch{padding:6px 14px;border-radius:20px;border:1px solid #30363d;background:#0d1117;color:#e1e4e8;font-size:13px;width:220px;outline:none}
.sch:focus{border-color:#58a6ff}
.sch::placeholder{color:#484f58}
.wrap{padding:24px 32px}
.card{background:#161b22;border:1px solid #21262d;border-radius:8px;margin-bottom:10px}
.card.dim{opacity:0.45}
.card:hover{border-color:#30363d}
.ch{padding:14px 20px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;user-select:none}
.cl{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.cn{font-weight:600;font-size:15px}
.bg{padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}
.bg-a{background:#1f3a2a;color:#3fb950}
.bg-j{background:#2a1f3a;color:#a371f7}
.bg-t{background:#1f2a3a;color:#58a6ff}
.lk{font-size:12px;color:#58a6ff;text-decoration:none}
.lk:hover{text-decoration:underline}
.nt{font-size:11px;color:#d29922}
.dots{display:flex;gap:4px;align-items:center}
.dot{width:10px;height:10px;border-radius:50%;border:2px solid #30363d;cursor:pointer}
.dot.done{background:#3fb950;border-color:#3fb950}
.dot.cur{border-color:#58a6ff;box-shadow:0 0 0 2px rgba(88,166,255,0.3)}
.chv{color:#484f58;transition:transform 0.2s}
.chv.open{transform:rotate(90deg)}
.cb{display:none;border-top:1px solid #21262d}
.cb.open{display:block}
.stp{padding:16px 20px;border-bottom:1px solid #21262d}
.stp:last-child{border-bottom:none}
.sh{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:8px}
.st{font-size:12px;font-weight:600;color:#8b949e;text-transform:uppercase;letter-spacing:0.5px}
.sa{display:flex;gap:6px}
.cpb{padding:4px 12px;border-radius:6px;border:1px solid #30363d;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:12px}
.cpb:hover{background:#30363d;border-color:#58a6ff;color:#58a6ff}
.cpb.ok{background:#1f3a2a;border-color:#3fb950;color:#3fb950}
.db{padding:4px 10px;border-radius:6px;border:1px solid #30363d;background:transparent;color:#484f58;cursor:pointer;font-size:12px}
.db:hover{border-color:#3fb950;color:#3fb950}
.db.y{background:#1f3a2a;border-color:#3fb950;color:#3fb950}
.sc{font-size:14px;line-height:1.6;color:#c9d1d9;white-space:pre-wrap;background:#0d1117;padding:12px 16px;border-radius:6px;border:1px solid #21262d;word-break:break-word}
.toast{position:fixed;bottom:24px;right:24px;background:#1f3a2a;color:#3fb950;padding:10px 20px;border-radius:8px;font-size:13px;opacity:0;transition:all 0.2s;pointer-events:none;border:1px solid #238636}
.toast.show{opacity:1}
</style>
</head>
<body>
<div class="hdr">
  <h1>NextStep Outreach Tracker</h1>
  <div class="stats">
    <div class="stat">Total: <strong id="s-t">0</strong></div>
    <div class="stat">Not started: <strong id="s-p">0</strong></div>
    <div class="stat">In progress: <strong id="s-i">0</strong></div>
    <div class="stat">Done: <strong id="s-d">0</strong></div>
  </div>
</div>
<div class="fbar">
  <button class="fb on" data-f="all">All</button>
  <button class="fb" data-f="ana">Ana</button>
  <button class="fb" data-f="jimmy">Jimmy</button>
  <button class="fb" data-f="t1">Tier 1</button>
  <button class="fb" data-f="t2">Tier 2</button>
  <button class="fb" data-f="t3">Tier 3</button>
  <button class="fb" data-f="ns">Not started</button>
  <button class="fb" data-f="ip">In progress</button>
  <button class="fb" data-f="opened">Opened link</button>
  <input class="sch" type="text" placeholder="Search investors..." id="q">
  <button class="fb" id="analytics-btn" style="margin-left:auto;background:#1f2a3a;color:#58a6ff;border-color:#58a6ff">Analytics</button>
</div>
<div id="analytics-panel" style="display:none;padding:24px 32px;border-bottom:1px solid #21262d">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
    <h2 style="font-size:16px">Link Analytics</h2>
    <button class="fb" onclick="loadAnalytics()" style="background:#21262d">Refresh</button>
  </div>
  <div id="analytics-content" style="color:#8b949e;font-size:13px">Click "Analytics" to load tracking data...</div>
</div>
<div class="wrap" id="list"></div>
<div class="toast" id="toast"></div>
<script>
const DATA_B64="PLACEHOLDER_B64";
const D=JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(DATA_B64),c=>c.charCodeAt(0))));

function gp(){try{return JSON.parse(localStorage.getItem("nsp")||"{}")}catch{return {}}}
function sp(p){localStorage.setItem("nsp",JSON.stringify(p))}
let prog=gp(),filt="all",qry="";

function toast(m){const t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),1500)}

function cpToClip(txt,btn,label){
  navigator.clipboard.writeText(txt).then(()=>{
    btn.classList.add("ok");btn.textContent="Copied!";toast("Copied to clipboard");
    setTimeout(()=>{btn.classList.remove("ok");btn.textContent=label||"Copy"},2000)
  })
}

function togStep(name,si){
  let c=prog[name]||0;
  prog[name]=si<c?si:si+1;
  sp(prog);render();
}

// Store copy texts
const copyTexts={};
D.forEach((inv,i)=>{
  inv.steps.forEach((s,si)=>{
    const isEmail=s.title.includes("Email");
    if(isEmail){
      const lines=s.content.split("\\n");
      const subjLine=lines.find(l=>l.startsWith("Subject:"));
      if(subjLine){
        copyTexts[i+"-"+si+"-subj"]=subjLine.replace("Subject: ","");
        copyTexts[i+"-"+si]=lines.filter(l=>!l.startsWith("Subject:")).join("\\n").trim();
      } else {
        copyTexts[i+"-"+si]=s.content;
      }
    } else {
      copyTexts[i+"-"+si]=s.content;
    }
  });
});

function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}

function render(){
  const el=document.getElementById("list");el.innerHTML="";
  let tt=0,pp=0,ip=0,dd=0;
  D.forEach((inv,i)=>{
    const done=prog[inv.name]||0;
    const tot=inv.steps.length;
    const fin=done>=tot;
    const inp=done>0&&!fin;
    tt++;if(fin)dd++;else if(inp)ip++;else pp++;
    const sl=(inv.sender||"").toLowerCase();
    const hasOpened=analyticsData[inv.name]&&analyticsData[inv.name].views>0;
    const mf=filt==="all"||(filt==="ana"&&sl==="ana")||(filt==="jimmy"&&sl==="jimmy")||(filt==="t1"&&inv.tier==="1")||(filt==="t2"&&inv.tier==="2")||(filt==="t3"&&inv.tier==="3")||(filt==="ns"&&done===0)||(filt==="ip"&&inp)||(filt==="opened"&&hasOpened);
    const mq=!qry||inv.name.toLowerCase().includes(qry.toLowerCase());
    if(!mf||!mq)return;

    const dots=inv.steps.map((_,j)=>'<div class="dot'+(j<done?' done':j===done?' cur':'')+'" data-n="'+inv.name+'" data-s="'+j+'"></div>').join("");
    const links=[];
    if(inv.linkedin)links.push('<a class="lk" href="'+inv.linkedin+'" target="_blank">LinkedIn</a>');
    if(inv.email)links.push('<a class="lk" href="mailto:'+inv.email+'">'+inv.email+'</a>');

    let stepsHtml="";
    inv.steps.forEach((s,si)=>{
      const isEmail=s.title.includes("Email");
      const hasSubj=copyTexts[i+"-"+si+"-subj"];
      const subjBtn=hasSubj?'<button class="cpb" data-cp="'+i+"-"+si+'-subj" data-l="Subject">Subject</button>':"";
      const cpLabel=isEmail?"Body":"Copy";
      stepsHtml+='<div class="stp"><div class="sh"><span class="st">'+s.title+'</span><div class="sa">'+subjBtn+'<button class="cpb" data-cp="'+i+"-"+si+'" data-l="'+cpLabel+'">'+cpLabel+'</button><button class="db'+(si<done?" y":"")+'" data-dn="'+inv.name+'" data-ds="'+si+'">'+(si<done?"Done":"Mark done")+'</button></div></div><div class="sc">'+esc(s.content)+'</div></div>';
    });

    const openBadge=hasOpened?'<span class="bg" style="background:#1a2e1a;color:#3fb950">Opened</span>':"";
    const analytics=analyticsData[inv.name];
    const analyticsInfo=analytics?'<span style="font-size:11px;color:#8b949e;margin-left:4px">'+analytics.views+'x'+(analytics.password?' | pw entered':'')+(analytics.maxTime?' | '+formatTime(analytics.maxTime):'')+'</span>':"";
    el.innerHTML+='<div class="card'+(fin?" dim":"")+'"><div class="ch" data-ci="'+i+'"><div class="cl"><div class="dots">'+dots+'</div><span class="cn">'+inv.name+'</span><span class="bg bg-'+sl[0]+'">'+inv.sender+'</span><span class="bg bg-t">Tier '+inv.tier+'</span>'+openBadge+analyticsInfo+(inv.note?'<span class="nt">'+inv.note+'</span>':'')+'</div><div style="display:flex;align-items:center;gap:12px">'+links.join(" &middot; ")+'<span class="chv">&#9654;</span></div></div><div class="cb" id="b'+i+'">'+stepsHtml+'</div></div>';
  });
  document.getElementById("s-t").textContent=tt;
  document.getElementById("s-p").textContent=pp;
  document.getElementById("s-i").textContent=ip;
  document.getElementById("s-d").textContent=dd;
}

document.getElementById("list").addEventListener("click",(e)=>{
  const cpBtn=e.target.closest(".cpb");
  if(cpBtn){e.stopPropagation();const key=cpBtn.dataset.cp;const txt=copyTexts[key];if(txt)cpToClip(txt,cpBtn,cpBtn.dataset.l);return}
  const dnBtn=e.target.closest(".db");
  if(dnBtn){e.stopPropagation();togStep(dnBtn.dataset.dn,parseInt(dnBtn.dataset.ds));return}
  const dot=e.target.closest(".dot");
  if(dot){e.stopPropagation();togStep(dot.dataset.n,parseInt(dot.dataset.s));return}
  const hdr=e.target.closest(".ch");
  if(hdr){const idx=hdr.dataset.ci;const b=document.getElementById("b"+idx);b.classList.toggle("open");hdr.querySelector(".chv").classList.toggle("open")}
});

document.querySelectorAll(".fb").forEach(b=>{
  if(b.id==="analytics-btn")return;
  b.addEventListener("click",()=>{document.querySelectorAll(".fb:not(#analytics-btn)").forEach(x=>x.classList.remove("on"));b.classList.add("on");filt=b.dataset.f;render()})
});
document.getElementById("q").addEventListener("input",e=>{qry=e.target.value;render()});

// Analytics
const SB_URL="https://rqimturydpfiwdzdtpyo.supabase.co";
const SB_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxaW10dXJ5ZHBmaXdkemR0cHlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3MzkyMzMsImV4cCI6MjA3OTMxNTIzM30.3KZfpSOyi_3o9BfsRyTN05HIldpy809_rDTOzxhI_IM";
let analyticsData={};

document.getElementById("analytics-btn").addEventListener("click",()=>{
  const p=document.getElementById("analytics-panel");
  p.style.display=p.style.display==="none"?"block":"none";
  if(p.style.display==="block")loadAnalytics();
});

async function loadAnalytics(){
  const el=document.getElementById("analytics-content");
  el.innerHTML='<span style="color:#58a6ff">Loading...</span>';
  try{
    const res=await fetch(SB_URL+"/rest/v1/visitor_tracking?select=*&order=created_at.desc",{
      headers:{"apikey":SB_KEY,"Authorization":"Bearer "+SB_KEY}
    });
    const rows=await res.json();
    analyticsData={};
    const refToName={};
    D.forEach(inv=>{if(inv.ref)refToName[inv.ref]=inv.name});

    rows.forEach(r=>{
      const name=refToName[r.ref]||r.ref;
      if(!analyticsData[name])analyticsData[name]={views:0,password:false,maxScroll:0,maxTime:0,lastVisit:null,visits:[]};
      const a=analyticsData[name];
      if(r.event==="page_view"){a.views++;if(!a.lastVisit||r.created_at>a.lastVisit)a.lastVisit=r.created_at}
      if(r.event==="password_entered")a.password=true;
      if(r.event==="page_exit"){if(r.scroll_depth>a.maxScroll)a.maxScroll=r.scroll_depth;if(r.time_on_page>a.maxTime)a.maxTime=r.time_on_page}
      a.visits.push(r);
    });

    if(Object.keys(analyticsData).length===0){
      el.innerHTML='<p>No visits tracked yet. Links will start tracking once investors open them.</p>';
      return;
    }

    let html='<table style="width:100%;border-collapse:collapse;font-size:13px"><thead><tr style="border-bottom:1px solid #30363d;text-align:left"><th style="padding:8px;color:#8b949e">Investor</th><th style="padding:8px;color:#8b949e">Views</th><th style="padding:8px;color:#8b949e">Password</th><th style="padding:8px;color:#8b949e">Scroll</th><th style="padding:8px;color:#8b949e">Time</th><th style="padding:8px;color:#8b949e">Last Visit</th></tr></thead><tbody>';
    const sorted=Object.entries(analyticsData).sort((a,b)=>b[1].views-a[1].views);
    sorted.forEach(([name,a])=>{
      const pwBadge=a.password?'<span style="color:#3fb950">Yes</span>':'<span style="color:#484f58">No</span>';
      const scroll=a.maxScroll?a.maxScroll+"%":"-";
      const time=a.maxTime?formatTime(a.maxTime):"-";
      const last=a.lastVisit?new Date(a.lastVisit).toLocaleDateString("en-GB",{day:"numeric",month:"short",hour:"2-digit",minute:"2-digit"}):"-";
      const rowColor=a.password?"color:#3fb950":a.views>0?"color:#e1e4e8":"color:#8b949e";
      html+='<tr style="border-bottom:1px solid #21262d;'+rowColor+'"><td style="padding:8px">'+name+'</td><td style="padding:8px">'+a.views+'</td><td style="padding:8px">'+pwBadge+'</td><td style="padding:8px">'+scroll+'</td><td style="padding:8px">'+time+'</td><td style="padding:8px">'+last+'</td></tr>';
    });
    html+='</tbody></table>';
    el.innerHTML=html;
    render();
  }catch(err){
    el.innerHTML='<span style="color:#ef4444">Error loading analytics: '+err.message+'</span><br><span style="color:#8b949e;font-size:12px">You may need to set the Supabase anon key in the HTML file.</span>';
  }
}

function formatTime(s){
  if(s<60)return s+"s";
  const m=Math.floor(s/60);
  const sec=s%60;
  return m+"m "+sec+"s";
}

render();
</script>
</body>
</html>"""

html = html.replace('PLACEHOLDER_B64', b64)

with open(os.path.join(DIR, 'outreach-tracker.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Built tracker with {len(investors)} investors")
