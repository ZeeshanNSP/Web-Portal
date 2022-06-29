/* global Chart, coreui */

/**
 * --------------------------------------------------------------------------
 * CoreUI Boostrap Admin Template (v4.1.1): main.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */
// Disable the on-canvas tooltip


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
const  getData =  ()=>{
   $.get("./getBandwidth",(res)=>{
    return {tx:res["tx"],rx:res["rx"]}
  })
  return {tx:Math.abs(Math.random()*1024)+100,rx:Math.abs(Math.random()*512)+10}
  
}
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
            bd =  getData()
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

const myLineChart = new Chart(document.getElementById("main-chart"),config);



