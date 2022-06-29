/* global Chart, coreui */

/**
 * --------------------------------------------------------------------------
 * CoreUI Boostrap Admin Template (v4.1.1): main.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */
// Disable the on-canvas tooltip
Chart.defaults.pointHitDetectionRadius = 1;
Chart.defaults.plugins.tooltip.enabled = false;
Chart.defaults.plugins.tooltip.mode = 'index';
Chart.defaults.plugins.tooltip.position = 'nearest';
Chart.defaults.plugins.tooltip.external = coreui.ChartJS.customTooltips;
Chart.defaults.defaultFontColor = '#646470';

const random = (min, max) => // eslint-disable-next-line no-mixed-operators
Math.floor(Math.random() * (max - min + 1) + min); // eslint-disable-next-line no-unused-vars



const mainChart = new Chart(document.getElementById('main-chart'), {
  type: 'line',
  data: {
    labels: ["Bandwidth","Bandwidth","Bandwidth","Bandwidth","Bandwidth","Bandwidth","Bandwidth","Bandwidth"],
    datasets: [{
      label: 'Tx',
      backgroundColor: coreui.Utils.hexToRgba(coreui.Utils.getStyle('--cui-info'), 10),
      borderColor: coreui.Utils.getStyle('--cui-info'),
      pointHoverBackgroundColor: '#fff',
      borderWidth: 2,
      data: [330,2243,545,2322,5454,2323,5646,6876],
      fill: true
    }, {
      label: 'Rx',
      borderColor: coreui.Utils.getStyle('--cui-success'),
      pointHoverBackgroundColor: '#fff',
      borderWidth: 2,
      data:  [80,22,54,232,545,232,5,687]
    }]
  },
  options: {
    tension:0.4,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    
    elements: {
      line: {
        tension: 0.4
      },
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
        hoverBorderWidth: 3
      }
    }
  }
});
