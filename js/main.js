/* global Chart, coreui */

/**
 * --------------------------------------------------------------------------
 * CoreUI Boostrap Admin Template (v4.1.1): main.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */
// Disable the on-canvas tooltip

const DEBUG = false;
const random = (min, max) => // eslint-disable-next-line no-mixed-operators
Math.floor(Math.random() * (max - min + 1) + min); // eslint-disable-next-line no-unused-vars



var data = {
  labels: ["Tx","Rx"],
  datasets: [{
    label: "Tx",
    backgroundColor:"rgba(0,225,0,1)",
    strokeColor:"rgba(0,225,0,1)",
    fillColor: "rgba(0,225,0,1)",
    borderColor: "rgba(0, 255, 0, 1)",
    data: []
  },{
    label: "Rx",
    backgroundColor:"rgba(255,0,0,1)",
    fillColor: "rgba(255,0,0,1)",
    strokeColor: "rgba(255,0,0,1)",
    pointHighlightStroke: "rgba(255,0,0,1)",
    borderColor: "rgba(255, 0, 0, 1)",
    data: []
  }  ]
};
var bd = {tx:Math.abs(Math.random()*2000)+100,rx:Math.abs(Math.random()*1000)+10} 

setInterval(function(){
  $.get("./getBandwidth",(res)=>{
    bd =  {tx:res["tx"],rx:res["rx"]}
  })

},500)
var config={
  type:"line",
  data,
  options:{
    tension:0.3,
    scales:{
      x:{
        type:'realtime',
      
        realtime:{
          onRefresh : chart=>{
            tx = {
              x:Date.now(),y:bd["tx"]
            }
            rx = {
              x:Date.now(),y:bd["rx"]
            }
          
            chart.data.datasets[0].data.push(tx)
          chart.data.datasets[1].data.push(rx)
          }
        }
      },
      y:{
        beginAtZero:true
      }
    }
  
  }
}

if(!DEBUG)
  document.addEventListener('contextmenu', event => event.preventDefault());

const myLineChart = new Chart(document.getElementById("main-chart"),config);



const dt = document.getElementById("dt")
setInterval(function(){
  t = new Date().toLocaleString()
  dt.innerText = t
},1000)


