$content = [System.IO.File]::ReadAllText("C:\Users\lenovo\.openclaw\workspace\admin_v17.html", [System.Text.Encoding]::UTF8)
$TOKEN = "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"

$pendingStart = $content.IndexOf("function showPendingDetail")
$beforePending = $content.Substring(0, $pendingStart)

$completePending = @"
function showPendingDetail(t){
    const now=new Date();
    const ms=new Date(now.getFullYear(),now.getMonth(),1);
    const wa=new Date(now.getTime()-7*86400000);
    let os=t==='month'?workorders.filter(o=>new Date(o.createTime)>=ms&&o.status!=='已完成'):workorders.filter(o=>new Date(o.createTime)>=wa&&o.status!=='已完成');
    document.getElementById('pendingModalTitle').textContent=(t==='month'?'本月':'本周')+'未完成 ('+os.length+'条)';
    document.querySelector('#pending-table tbody').innerHTML=os.map(o=>{
        const ct=new Date(o.createTime);
        const duration=now-ct;
        return'<tr><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+(o.desc||'').substring(0,10)+'</td><td>'+ct.toLocaleDateString()+'</td><td>'+formatDuration(duration)+'</td><td>'+getStatusHtml(o.status)+'</td></tr>';
    }).join('');
    new bootstrap.Modal(document.getElementById('pendingModal')).show();
}
"@

$extraFuncs = @"
function renderVendors(){
    const tbody=document.querySelector('#vendor-table tbody');
    tbody.innerHTML=vendors.map(v=>'<tr><td>'+v.type+'</td><td>'+v.vendor+'</td><td>'+v.contact+'</td><td>'+v.phone+'</td></tr>').join('');
}
function renderDashboard(){
    const now=new Date();
    const ms=new Date(now.getFullYear(),now.getMonth(),1);
    const wa=new Date(now.getTime()-7*86400000);
    const mo=workorders.filter(o=>new Date(o.createTime)>=ms);
    const wo=workorders.filter(o=>new Date(o.createTime)>=wa);
    document.getElementById('month-total').textContent=mo.length;
    document.getElementById('month-done').textContent=mo.filter(o=>o.status==='已完成').length;
    document.getElementById('month-pending').textContent=mo.filter(o=>o.status!=='已完成').length;
    document.getElementById('week-total').textContent=wo.length;
    document.getElementById('week-done').textContent=wo.filter(o=>o.status==='已完成').length;
    document.getElementById('week-pending').textContent=wo.filter(o=>o.status!=='已完成').length;
    const done=workorders.filter(o=>o.status==='已完成'&&o.completeTime);
    if(done.length>0){
        const tot=done.reduce((s,o)=>s+(new Date(o.completeTime).getTime()-new Date(o.createTime).getTime()),0);
        document.getElementById('avg-response').textContent=formatDuration(Math.round(tot/done.length));
    }else{
        document.getElementById('avg-response').textContent='0h';
    }
    const vm={};
    workorders.forEach(o=>{const v=o.vendor||'未知';vm[v]=(vm[v]||0)+1;});
    const vK=Object.keys(vm),vV=Object.values(vm);
    if(window.chartVendor)window.chartVendor.destroy();
    window.chartVendor=new Chart(document.getElementById('chart-vendor').getContext('2d'),{type:'bar',data:{labels:vK,datasets:[{label:'工单数',data:vV,backgroundColor:'#1976d2'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{stepSize:1}}}}});
    const rm={};
    workorders.filter(o=>o.status==='已完成'&&o.completeTime).forEach(o=>{
        const v=o.vendor||'未知';
        const h=(new Date(o.completeTime).getTime()-new Date(o.createTime).getTime())/3600000;
        if(!rm[v])rm[v]=[];rm[v].push(h);
    });
    const rK=Object.keys(rm);
    const rV=rK.map(v=>{const a=rm[v];return Math.round(a.reduce((x,y)=>x+y,0)/a.length*10)/10;});
    if(window.chartResponse)window.chartResponse.destroy();
    window.chartResponse=new Chart(document.getElementById('chart-response').getContext('2d'),{type:'bar',data:{labels:rK,datasets:[{label:'平均响应时长(h)',data:rV,backgroundColor:'#28a745'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});
}
function showPage(page){
    const pages=['generate','workorders','dashboard','vendors','settings'];
    pages.forEach(p=>{
        document.getElementById('page-'+p).style.display='none';
        document.getElementById('nav-'+p).classList.remove('active');
        const m=document.getElementById('mnav-'+p);
        if(m)m.classList.remove('active');
    });
    document.getElementById('page-'+page).style.display='block';
    const nav=document.getElementById('nav-'+page);
    if(nav)nav.classList.add('active');
    const mnav=document.getElementById('mnav-'+page);
    if(mnav)mnav.classList.add('active');
    if(page==='workorders')renderWorkorders();
    else if(page==='dashboard')renderDashboard();
    else if(page==='vendors')renderVendors();
    else if(page==='settings'){const u=getCurrentUser();if(u)document.getElementById('setting-username').value=u.username||'';showAccountList();}
    else if(page==='generate'){const s=document.getElementById('edit-vendor');if(s)s.innerHTML=vendors.map(v=>'<option value="'+v.vendor+'">'+v.vendor+'</option>').join('');}
}
async function uploadToCloud(){
    const gid=getGistId();
    if(!gid){alert('请先在设置中填写Gist ID');return;}
    try{
        const res=await fetch('https://api.github.com/gists/'+gid,{method:'PATCH',headers:{'Authorization':'token '+TOKEN,'Content-Type':'application/json'},body:JSON.stringify({description:'Workorders backup',files:{'workorders.json':{content:JSON.stringify({workorders,vendors,version:new Date().toISOString()})}}})});
        if(res.ok){alert('上传成功');syncFromCloud();}else{const e=await res.json();alert('上传失败: '+(e.message||res.status));}
    }catch(e){alert('上传失败: '+e.message);}
}
async function syncFromCloud(){
    const gid=getGistId();
    if(!gid)return;
    try{
        const res=await fetch('https://api.github.com/gists/'+gid,{headers:{'Authorization':'token '+TOKEN}});
        if(!res.ok)return;
        const data=await res.json();
        const f=data.files&&data.files['workorders.json'];
        if(f&&f.content){const p=JSON.parse(f.content);if(p.workorders){workorders=p.workorders;saveWorkorders();alert('同步成功，共 '+workorders.length+' 条工单');}}
    }catch(e){console.error(e);}
}
const ev=document.getElementById('edit-vendor');
if(ev)ev.innerHTML=vendors.map(v=>'<option value="'+v.vendor+'">'+v.vendor+'</option>').join('');
checkLogin();
"@

$out = $beforePending + $completePending + $extraFuncs

# Fix HTML: change mb-1 to mb-2 and merge button into same row
$out = $out.Replace('mb-1 mb-1">', 'mb-2">')
$out = $out.Replace('mb-1 mb-1"', 'mb-2"')

# Find the search input row and add style
$searchInputOld = '<input class="form-control form-control-sm" id="search-order" placeholder'
$searchInputNew = '<input class="form-control form-control-sm" id="search-order" placeholder="搜索机构..." style="max-width:150px"'
$out = $out.Replace($searchInputOld, $searchInputNew)

# Remove the separate button row div and merge button into same line
$oldButtonSection = @'
                    </div>
                    <div class="d-flex gap-1">
                        <button class="btn btn-primary btn-sm flex-fill" onclick="renderWorkorders()">查询</button>
                    </div>
'@

$newButtonSection = @'
                        <input type="date" class="form-control form-control-sm" id="search-date-end">
                        <button class="btn btn-primary btn-sm" onclick="renderWorkorders()">查询</button>
                    </div>
'@

$out = $out.Replace($oldButtonSection, $newButtonSection)

[System.IO.File]::WriteAllText("C:\Users\lenovo\.openclaw\workspace\admin_new.html", $out, [System.Text.Encoding]::UTF8)
Write-Host "Done! Length: $($out.Length)"
Write-Host "checkLogin: $($out.Contains('checkLogin'))"
Write-Host "renderDashboard: $($out.Contains('function renderDashboard'))"
Write-Host "showPage: $($out.Contains('function showPage'))"
Write-Host "renderVendors: $($out.Contains('function renderVendors'))"
Write-Host "HTML fix (mb-2): $($out.Contains('mb-2'))"
