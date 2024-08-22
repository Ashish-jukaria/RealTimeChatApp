
const groupName=JSON.parse(document.getElementById('group-name').textContent)
console.log(groupName)
var ws=new WebSocket(
    'ws://'
+ window.location.host
+'/ws/sc/'
+groupName
+'/')

console.log(ws)

ws.onopen=()=>{


}

ws.onmessage=(event)=>{
    const data=JSON.parse(event.data)
    document.getElementById('textbox1').value+=(data.msg+'\n')


}

ws.onclose=(event)=>{
    console.error('websocket closed')
}

document.getElementById('submit').onclick=(event)=>{

 data= document.getElementById('textbox2').value
 ws.send(JSON.stringify({
    'msg':data
 }))
 document.getElementById('textbox2').value = '';

}

