# Update JS functions
with open(r'C:\Users\lenovo\.openclaw\workspace\admin_v13.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update renderWorkorders to include fault column
old_render = '''document.querySelector('#workorder-table tbody').innerHTML=pageData.map(o=>{
        const ct = new Date(o.createTime);
        return '<tr class="'+(o.status!=='已完成'&&ct<ow?'overdue':'')+'"><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+getStatusHtml(o.status)+'</td><td>'+(o.vendor||'-')+'</td><td>'+ct.toLocaleDateString()+'</td></tr>';
    }).join('');'''

new_render = '''document.querySelector('#workorder-table tbody').innerHTML=pageData.map(o=>{
        const ct = new Date(o.createTime);
        const desc = (o.desc || '').substring(0, 12);
        return '<tr class="'+(o.status!=='已完成'&&ct<ow?'overdue':'')+'"><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+desc+'</td><td>'+getStatusHtml(o.status)+'</td><td>'+(o.vendor||'-')+'</td><td>'+ct.toLocaleDateString()+'</td></tr>';
    }).join('');'''

content = content.replace(old_render, new_render)

# Update showPendingDetail to include time info
old_pending = "document.querySelector('#pending-table tbody').innerHTML=os.map(o=>'<tr><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+o.status+'</td></tr>').join('');"

new_pending = '''const now = new Date();
    document.querySelector('#pending-table tbody').innerHTML = os.map(o => {
        const ct = new Date(o.createTime);
        const duration = now - ct;
        return '<tr><td>'+o.id+'</td><td>'+o.dept+'</td><td>'+o.device+'</td><td>'+ct.toLocaleString()+'</td><td>'+formatDuration(duration)+'</td><td>'+getStatusHtml(o.status)+'</td></tr>';
    }).join('');'''

content = content.replace(old_pending, new_pending)

# Add formatDuration function if not exists
if 'function formatDuration' not in content:
    # Insert after getStatusHtml
    insert_pos = content.find('function getStatusHtml')
    if insert_pos > 0:
        func_end = content.find('}', insert_pos) + 1
        new_func = '''
function formatDuration(ms) {
    if(!ms) return '-';
    const h = Math.floor(ms/3600000);
    const m = Math.floor((ms%3600000)/60000);
    if(h > 24) return Math.floor(h/24) + '天' + (h%24) + 'h';
    return h + 'h' + m + 'm';
}'''
        content = content[:func_end] + new_func + content[func_end:]

with open(r'C:\Users\lenovo\.openclaw\workspace\admin_v13.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
