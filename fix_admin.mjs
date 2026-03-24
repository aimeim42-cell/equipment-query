import { readFileSync, writeFileSync } from 'fs';

const GITHUB_TOKEN = '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';

const filePath = 'C:/Users/lenovo/.openclaw/workspace/admin_v17.html';
const content = readFileSync(filePath, 'utf8');

const pendingStart = content.indexOf('function showPendingDetail');
const incompletePending = content.slice(pendingStart);

const beforePending = content.slice(0, pendingStart);

const completeShowPending = `function showPendingDetail(t){
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
`;

const missingFunctions = `

function renderVendors(){
    const tbody=document.querySelector('#vendor-table tbody');
    tbody.innerHTML=vendors.map(v=>'<tr><td>'+v.type+'</td><td>'+v.vendor+'</td><td>'+v.contact+'</td><td>'+v.phone+'</td></tr>').join('');
}

function renderDashboard(){
    const now=new Date();
    const ms=new Date(now.getFullYear(),now.getMonth(),1);
    const wa=new Date(now.getTime()-7*86400000);
    const monthOrders=workorders.filter(o=>new Date(o.createTime)>=ms);
    const weekOrders=workorders.filter(o=>new Date(o.createTime)>=wa);
    document.getElementById('month-total').textContent=monthOrders.length;
    document.getElementById('month-done').textContent=monthOrders.filter(o=>o.status==='已完成').length;
    document.getElementById('month-pending').textContent=monthOrders.filter(o=>o.status!=='已完成').length;
    document.getElementById('week-total').textContent=weekOrders.length;
    document.getElementById('week-done').textContent=weekOrders.filter(o=>o.status==='已完成').length;
    document.getElementById('week-pending').textContent=weekOrders.filter(o=>o.status!=='已完成').length;
    const completed=workorders.filter(o=>o.status==='已完成'&&o.completeTime);
    if(completed.length>0){
        const total=completed.reduce((sum,o)=>{
            return sum+(new Date(o.completeTime).getTime()-new Date(o.createTime).getTime());
        },0);
        document.getElementById('avg-response').textContent=formatDuration(Math.round(total/completed.length));
    }else{
        document.getElementById('avg-response').textContent='0h';
    }
    const vendorMap={};
    workorders.forEach(o=>{const v=o.vendor||'未知';vendorMap[v]=(vendorMap[v]||0)+1;});
    const vendorLabels=Object.keys(vendorMap);
    const vendorData=Object.values(vendorMap);
    if(window.chartVendor)window.chartVendor.destroy();
    const ctxV=document.getElementById('chart-vendor').getContext('2d');
    window.chartVendor=new Chart(ctxV,{
        type:'bar',
        data:{labels:vendorLabels,datasets:[{label:'工单数',data:vendorData,backgroundColor:'#1976d2'}]},
        options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{stepSize:1}}}}
    });
    const respMap={};
    workorders.filter(o=>o.status==='已完成'&&o.completeTime).forEach(o=>{
        const v=o.vendor||'未知';
        const hours=(new Date(o.completeTime).getTime()-new Date(o.createTime).getTime())/3600000;
        if(!respMap[v])respMap[v]=[];
        respMap[v].push(hours);
    });
    const respLabels=Object.keys(respMap);
    const respAvg=respLabels.map(v=>{const arr=respMap[v];return Math.round(arr.reduce((a,b)=>a+b,0)/arr.length*10)/10;});
    if(window.chartResponse)window.chartResponse.destroy();
    const ctxR=document.getElementById('chart-response').getContext('2d');
    window.chartResponse=new Chart(ctxR,{
        type:'bar',
        data:{labels:respLabels,datasets:[{label:'平均响应时长(h)',data:respAvg,backgroundColor:'#28a745'}]},
        options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}
    });
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
    else if(page==='settings'){
        const user=getCurrentUser();
        if(user)document.getElementById('setting-username').value=user.username||'';
        showAccountList();
    }else if(page==='generate'){
        const sel=document.getElementById('edit-vendor');
        if(sel)sel.innerHTML=vendors.map(v=>'<option value="'+v.vendor+'">'+v.vendor+'</option>').join('');
    }
}

async function uploadToCloud(){
    const gistId=getGistId();
    if(!gistId){alert('请先在设置中填写Gist ID');return;}
    const data=JSON.stringify({workorders,vendors,version:new Date().toISOString()});
    try{
        const res=await fetch('https://api.github.com/gists/'+gistId,{
            method:'PATCH',
            headers:{'Authorization':'token '+GITHUB_TOKEN,'Content-Type':'application/json'},
            body:JSON.stringify({description:'Workorders backup',files:{'workorders.json':{content:data}}})
        });
        if(res.ok){alert('上传成功');syncFromCloud();}
        else{const err=await res.json();alert('上传失败: '+(err.message||res.status));}
    }catch(e){alert('上传失败: '+e.message);}
}

async function syncFromCloud(){
    const gistId=getGistId();
    if(!gistId)return;
    try{
        const res=await fetch('https://api.github.com/gists/'+gistId,{headers:{'Authorization':'token '+GITHUB_TOKEN}});
        if(!res.ok)return;
        const data=await res.json();
        const file=data.files&&data.files['workorders.json'];
        if(file){
            const parsed=JSON.parse(file.content);
            if(parsed.workorders){
                workorders=parsed.workorders;
                saveWorkorders();
                alert('同步成功，共 '+workorders.length+' 条工单');
            }
        }
    }catch(e){console.error('Sync error:',e);}
}

const editVendorSel=document.getElementById('edit-vendor');
if(editVendorSel){editVendorSel.innerHTML=vendors.map(v=>'<option value="'+v.vendor+'">'+v.vendor+'</option>').join('');}

checkLogin();
`;

const fixedContent = beforePending + completeShowPending + missingFunctions;
writeFileSync('C:/Users/lenovo/.openclaw/workspace/admin_new.html', fixedContent, 'utf8');
console.log('admin_new.html written, length:', fixedContent.length);

// Also apply HTML fix: combine search/date/button into one row
// Find the current search card structure and fix it
let fixedHtml = fixedContent;

// Find and fix: the separate query button row should be merged into one row
const searchCardOld = `<div class="d-flex gap-1 mb-1">
                        <input class="form-control form-control-sm" id="search-order" placeholder="🔍 \u641c\u7d22\u673a\u6784...">
                        <input type="date" class="form-control form-control-sm" id="search-date-start">
                        <input type="date" class="form-control form-control-sm" id="search-date-end">
                    </div>
                    <div class="d-flex gap-1">
                        <button class="btn btn-primary btn-sm flex-fill" onclick="renderWorkorders()">\u67e5\u8be2</button>
                    </div>`;

const searchCardNew = `<div class="d-flex gap-1 mb-2">
                        <input class="form-control form-control-sm" id="search-order" placeholder="🔍 \u641c\u7d22\u673a\u6784..." style="max-width:160px">
                        <input type="date" class="form-control form-control-sm" id="search-date-start">
                        <input type="date" class="form-control form-control-sm" id="search-date-end">
                        <button class="btn btn-primary btn-sm" onclick="renderWorkorders()">\u67e5\u8be2</button>
                    </div>`;

if (fixedHtml.includes(searchCardOld)) {
    fixedHtml = fixedHtml.replace(searchCardOld, searchCardNew);
    console.log('HTML fix applied: search card merged');
} else {
    console.log('WARNING: search card pattern not found exactly, trying partial match');
    // Try to find the pattern differently
    const idx1 = fixedHtml.indexOf('id="search-order"');
    if (idx1 > 0) {
        const start = fixedHtml.lastIndexOf('<div', idx1);
        const end = fixedHtml.indexOf('</div>', fixedHtml.indexOf('btn btn-primary btn-sm flex-fill', idx1));
        console.log('Found search card at', start, 'to', end+6);
    }
}

writeFileSync('C:/Users/lenovo/.openclaw/workspace/admin_new.html', fixedHtml, 'utf8');
console.log('Final admin_new.html written, length:', fixedHtml.length);
