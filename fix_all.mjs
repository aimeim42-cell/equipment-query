import { readFileSync, writeFileSync } from 'fs';

const src = 'C:/Users/lenovo/.openclaw/workspace/admin_new.html';
let c = readFileSync(src, 'utf8');

console.log('File length:', c.length);

// ============================================================
// 1. Fix duplicate placeholder in search-order input
// ============================================================
// The search-order input has duplicate placeholder attributes from the build script
const dupPlaceholder = 'placeholder="搜索机构..." style="max-width:150px" placeholder="&#x641c;&#x7d22;&#x673a;&#x6784;..."';
const fixedPlaceholder = 'placeholder="搜索机构..." style="max-width:150px"';
c = c.replace(dupPlaceholder, fixedPlaceholder);
console.log('1. Duplicate placeholder fixed:', !c.includes(dupPlaceholder));

// ============================================================
// 2. Add device type change listener
// ============================================================
const oldDeviceType = 'class="form-control" id="edit-device-type"';
const newDeviceType = 'class="form-control" id="edit-device-type" onchange="handleDeviceTypeChange(this.value)"';
c = c.replace(oldDeviceType, newDeviceType);
console.log('2. Device type onchange added:', c.includes('handleDeviceTypeChange'));

// ============================================================
// 3. Fix chart canvases - add explicit width/height attributes
// ============================================================
c = c.replace('<canvas id="chart-vendor"', '<canvas id="chart-vendor" width="400" height="220"');
c = c.replace('<canvas id="chart-response"', '<canvas id="chart-response" width="400" height="220"');
console.log('3. Chart canvases fixed');

// ============================================================
// 4. Fix analyzeWorkorder - set vendor=username for vendor role
// ============================================================
// Change: o.vendor=vName; o.status='待分配';
// To:     o.vendor=(u && u.role==='vendor')?u.username:vName||'待分配';
//         o.status=(u && u.role==='vendor' && device==='其他')?'其他':'待分配';
const oldAnalyzeStatus = "o.vendor=vName; o.status='待分配'; } else {";
const newAnalyzeStatus = "o.vendor=(u&&u.role==='vendor')?u.username:(vName||'待分配'); o.status=(u&&u.role==='vendor'&&device==='其他')?'其他':'待分配'; } else {";
c = c.replace(oldAnalyzeStatus, newAnalyzeStatus);
console.log('4. analyzeWorkorder vendor/status logic fixed:', c.includes("o.vendor=(u&&u.role==='vendor')"));

// ============================================================
// 5. Fix nav for vendor role
// ============================================================
const oldNavWorkorders = "document.getElementById('nav-workorders').style.display='none';";
const newNavWorkorders = "var _u=getCurrentUser();document.getElementById('nav-workorders').style.display=(!_u||_u.role==='admin')?'':'none';document.getElementById('nav-generate').style.display=(!_u||_u.role==='admin')?'':'none';";
c = c.replace(oldNavWorkorders, newNavWorkorders);
console.log('5. Desktop nav access control added:', c.includes("_u.role==='admin'"));

const oldMobileNav = "document.getElementById('mnav-workorders').style.display='none';";
const newMobileNav = "var _mu=getCurrentUser();document.getElementById('mnav-workorders').style.display=(!_mu||_mu.role==='admin')?'':'none';document.getElementById('mnav-generate').style.display=(!_mu||_mu.role==='admin')?'':'none';";
c = c.replace(oldMobileNav, newMobileNav);
console.log('6. Mobile nav access control added:', c.includes("_mu.role==='admin'"));

// ============================================================
// 6. Inject all new functions before last </script>
// ============================================================
const lastScriptEnd = c.lastIndexOf('</script>');
const newFunctions = `

// 运维商"其他"设备类型：切换设备类型时自动更新状态选项
function handleDeviceTypeChange(deviceType) {
    var statusSelect = document.getElementById('edit-status');
    if (!statusSelect) return;
    var u = getCurrentUser();
    var isVendorOther = (u && u.role === 'vendor' && deviceType === '其他');
    var opts = statusSelect.options;
    for (var i = 0; i < opts.length; i++) {
        if (isVendorOther && opts[i].value === '待分配') {
            opts[i].text = '其他';
            opts[i].value = '其他';
            if (statusSelect.value === '待分配') statusSelect.value = '其他';
        } else if (opts[i].value === '其他') {
            opts[i].text = '待分配';
            opts[i].value = '待分配';
        }
    }
}

// 增强generateWorkorder：运维商"其他"类型时自动设置vendor为当前用户
var _origGenerateWorkorder = generateWorkorder;
generateWorkorder = function() {
    var u = getCurrentUser();
    var vendor = document.getElementById('edit-vendor').value;
    var device = document.getElementById('edit-device-type').value;
    var dept = document.getElementById('edit-dept').value;
    var desc = document.getElementById('edit-desc').value;
    var status = document.getElementById('edit-status').value;
    if (u && u.role === 'vendor' && device === '其他') { vendor = u.username; }
    if (!dept || !device) { alert('请填写完整信息'); return; }
    var now = new Date();
    var id = 'WO' + now.getFullYear() + String(now.getMonth()+1).padStart(2,'0') + String(now.getDate()).padStart(2,'0') + String(Math.random()).slice(2,6);
    var o = {
        id: id, createTime: now.toISOString(), createBy: u ? u.username : 'admin',
        dept: dept, device: device, vendor: vendor, desc: desc,
        status: (u && u.role === 'vendor' && device === '其他') ? '其他' : status,
        responseTime: null, completeTime: null
    };
    workorders.push(o);
    saveWorkorders();
    renderWorkorders();
    bootstrap.Modal.getInstance(document.getElementById('generateModal')).hide();
    alert('工单 ' + id + ' 已生成');
    document.getElementById('edit-desc').value = '';
};

// showPage增强：进入生成页面时自动分析工单
var _origShowPage = showPage;
showPage = function(page) {
    _origShowPage(page);
    if (page === 'generate') {
        setTimeout(function() { analyzeWorkorder(); }, 100);
    }
};

// renderWorkorders增强：供应商角色只看自己的工单
var _origRenderWorkorders = renderWorkorders;
renderWorkorders = function() {
    var u = getCurrentUser();
    var kw = (document.getElementById('search-order') || {value:''}).value.trim().toLowerCase();
    var ds = (document.getElementById('search-date-start') || {value:''}).value;
    var de = (document.getElementById('search-date-end') || {value:''}).value;
    var list = workorders.filter(function(o) {
        if (u && u.role === 'vendor' && o.createBy !== u.username) return false;
        if (kw && o.id.toLowerCase().indexOf(kw) < 0 && (o.dept||'').toLowerCase().indexOf(kw) < 0 && (o.vendor||'').toLowerCase().indexOf(kw) < 0) return false;
        if (ds && o.createTime < ds) return false;
        if (de && o.createTime > de + 'T23:59:59') return false;
        return true;
    });
    list.sort(function(a,b){ return new Date(b.createTime) - new Date(a.createTime); });
    var html = '<table class="table table-sm table-hover mb-0"><thead><tr><th>工单号</th><th>创建时间</th><th>机构</th><th>设备类型</th><th>供应商</th><th>状态</th><th>操作</th></tr></thead><tbody>';
    if (list.length === 0) {
        html += '<tr><td colspan="7" class="text-center text-muted py-4">暂无数据</td></tr>';
    } else {
        list.forEach(function(o) {
            html += '<tr>';
            html += '<td><span class="text-primary fw-bold" style="cursor:pointer" onclick="showOrderDetail(\\''+o.id+'\\')">'+o.id+'</span></td>';
            html += '<td>'+new Date(o.createTime).toLocaleString('zh-CN',{hour12:false})+'</td>';
            html += '<td>'+o.dept+'</td>';
            html += '<td>'+o.device+'</td>';
            html += '<td>'+(o.vendor||'')+'</td>';
            html += '<td>'+getStatusHtml(o.status)+'</td>';
            html += '<td>';
            var u2 = getCurrentUser();
            if ((!u2 || u2.role === 'admin') && o.status !== '已完成') {
                html += '<button class="btn btn-xs btn-outline-primary me-1" onclick="showChangeStatus(\\''+o.id+'\\')">改状态</button>';
            }
            html += '<button class="btn btn-xs btn-outline-secondary" onclick="showOrderDetail(\\''+o.id+'\\')">详情</button>';
            html += '</td></tr>';
        });
    }
    html += '</tbody></table>';
    document.getElementById('workorder-list').innerHTML = html;
};

// renderDashboard增强：供应商角色只看自己的数据
var _origRenderDashboard = renderDashboard;
renderDashboard = function() {
    var u = getCurrentUser();
    var filtered = (u && u.role === 'vendor') ? workorders.filter(function(o){ return o.createBy === u.username; }) : workorders;
    var now = new Date();
    var ms = new Date(now.getFullYear(),now.getMonth(),1);
    var wa = new Date(now.getTime()-7*86400000);
    var mo = filtered.filter(function(o){ return new Date(o.createTime) >= ms; });
    var wo = filtered.filter(function(o){ return new Date(o.createTime) >= wa; });
    document.getElementById('month-total').textContent = mo.length;
    document.getElementById('month-done').textContent = mo.filter(function(o){ return o.status==='已完成'; }).length;
    document.getElementById('month-pending').textContent = mo.filter(function(o){ return o.status!=='已完成'; }).length;
    document.getElementById('week-total').textContent = wo.length;
    document.getElementById('week-done').textContent = wo.filter(function(o){ return o.status==='已完成'; }).length;
    document.getElementById('week-pending').textContent = wo.filter(function(o){ return o.status!=='已完成'; }).length;
    var done = filtered.filter(function(o){ return o.status==='已完成'&&o.completeTime; });
    if (done.length > 0) {
        var tot = done.reduce(function(s,o){ return s+(new Date(o.completeTime).getTime()-new Date(o.createTime).getTime()); }, 0);
        document.getElementById('avg-response').textContent = formatDuration(Math.round(tot/done.length));
    } else {
        document.getElementById('avg-response').textContent = '0h';
    }
    var vm = {};
    filtered.forEach(function(o){ var v=o.vendor||'未知'; vm[v]=(vm[v]||0)+1; });
    var vK = Object.keys(vm), vV = Object.values(vm);
    if (window.chartVendor) { try { window.chartVendor.destroy(); } catch(e){} window.chartVendor = null; }
    if (window.chartResponse) { try { window.chartResponse.destroy(); } catch(e){} window.chartResponse = null; }
    var cv = document.getElementById('chart-vendor');
    var cr = document.getElementById('chart-response');
    if (cv && cv.parentElement) {
        cv.parentElement.style.minHeight = '220px';
        window.chartVendor = new Chart(cv.getContext('2d'),{
            type:'bar',
            data:{labels:vK,datasets:[{label:'工单数',data:vV,backgroundColor:'#1976d2'}]},
            options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{stepSize:1}}}}
        });
    }
    var rm = {};
    filtered.filter(function(o){ return o.status==='已完成'&&o.completeTime; }).forEach(function(o){
        var v=o.vendor||'未知';
        var h=(new Date(o.completeTime).getTime()-new Date(o.createTime).getTime())/3600000;
        if(!rm[v])rm[v]=[];rm[v].push(h);
    });
    var rK = Object.keys(rm);
    var rV = rK.map(function(v){ var a=rm[v]; return Math.round(a.reduce(function(x,y){return x+y;},0)/a.length*10)/10; });
    if (cr && cr.parentElement) {
        cr.parentElement.style.minHeight = '220px';
        window.chartResponse = new Chart(cr.getContext('2d'),{
            type:'bar',
            data:{labels:rK,datasets:[{label:'平均响应时长(h)',data:rV,backgroundColor:'#28a745'}]},
            options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}
        });
    }
};
`;

c = c.slice(0, lastScriptEnd) + newFunctions + '\n' + c.slice(lastScriptEnd);
console.log('7. All new functions injected');

// ============================================================
// 7. Set default page to dashboard for better UX
// ============================================================
// This is already handled by checkLogin showing dashboard

writeFileSync('C:/Users/lenovo/.openclaw/workspace/admin_v18.html', c, 'utf8');
console.log('\nDone! admin_v18.html written');
console.log('Length:', c.length);

// Verification
const checks = [
  ['Duplicate placeholder gone', !c.includes('style="max-width:150px" placeholder')],
  ['handleDeviceTypeChange added', c.includes('function handleDeviceTypeChange')],
  ['Chart width/height added', c.includes('width="400" height="220"')],
  ['analyzeWorkorder fixed', c.includes("u.role==='vendor'")],
  ['Nav access control', c.includes("_u.role==='admin'")],
  ['Mobile nav access control', c.includes("_mu.role==='admin'")],
  ['generateWorkorder wrapped', c.includes('_origGenerateWorkorder')],
  ['showPage wrapped', c.includes('_origShowPage')],
  ['renderWorkorders wrapped', c.includes('_origRenderWorkorders')],
  ['renderDashboard wrapped', c.includes('_origRenderDashboard')],
  ['Vendor filter in renderWorkorders', c.includes("u.role === 'vendor' && o.createBy !== u.username")],
];
checks.forEach(([name, ok]) => console.log((ok ? '✅' : '❌'), name));
