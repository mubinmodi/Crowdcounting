const main = document.querySelector('.chart-section')
const xhr = new XMLHttpRequest();
const url = `/cameras-data`;
xhr.open("GET", url);
xhr.responseType = 'json'
xhr.send();
// const loading = document.createElement('div');

// let innerHtmlForReport = `<div class="loader">Loading...</div>`


// xhr.onprogress = event => {

  
//   loading.innerHTML = innerHtmlForReport
//   main.appendChild(loading)
// }

xhr.onload = event => {
  console.log(`Received ${event.loaded} of ${event.total}`)
  const camerasData = JSON.parse(xhr.response);
  console.log(camerasData)
  camerasData.push({
    _id: "total-16-may",
    ip: "_ _ _._ _ _._ _._ _",
    CameraName : "Total-Count-Graph"
  })
 
  const max_size = 8;
  const totalCountArray = new Array(length).fill(0);

  const sum = () => {
    let s = totalCountArray.reduce((a, c) => a + c, 0);
    return s;
  };

  console.log("later",camerasData)

  camerasData.forEach((cameraData, index) => {

  const chartSection = document.createElement('div');
    chartSection.setAttribute('class', 'Chart');
  
    const videoFeedUrl = `video_feed/${cameraData._id}`
    
    const dataToBeAdded = [

      `<div class = "totalWindow">
        <h4>Total Count</h4>
        <p>No Live Footage Available for this window</p>
      </div>`
      ,
      `<div class="TotalCount">
      <p>Total Count</p>
      <h3 id="${cameraData._id}-totalCount">0</h3>
    </div>`
      
    ];

    if (index !== camerasData.length - 1) {
      dataToBeAdded[0] = ` <img 
          src= ${videoFeedUrl}
         alt="" class="image" />`;
    }
  
   innerHtmlForReport = `
   
    
      <div class="titleAndSelector">
        <div class="title">
          <h2>Report - ${cameraData.CameraName}</h2>
          <div class="line-breaker"></div>
        </div>
        <div class="selector">
          <div class="optionChoose">
            <ul>
              <li class="option-${cameraData._id} option " data-option="${cameraData._id}-week">Week</li>
              <li class="option-${cameraData._id} option" data-option="${cameraData._id}-day">Day</li>
              <li class="option-${cameraData._id} option" data-option="${cameraData._id}-live">Live</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="camAndGraph">
        <div class="liveCamera">
          <div class="Live">
            <h2 >${cameraData.CameraName}</h2>
            <div class="icon_live"></div>
            <p style="color: aliceblue">( Live Footage )</p>
          </div>

          <p id="ip">${cameraData.ip}</p>
          ${dataToBeAdded[0]}
        </div>
        <div class="graph">
          <div class="canvas"><canvas id="${cameraData._id}-graph"></canvas></div>
        </div>
      </div>
      <div class="ListCount">
        <div class="CurrCount">
          <p>${index !== camerasData.length - 1 ? 'Current Count' : 'Total Count'}</p>
          <h3 id= "${cameraData._id}-currCount">0</h3>
        </div>
        <div class="AverageCount">
          <p>Average Count</p>
          <h3 id= "${cameraData._id}-averageCount">0</h3>
        </div>
        <div class="MaxCount">
          <p>Max Count</p>
          <h3 id= "${cameraData._id}-maxCount">0</h3>
        </div>
        ${index !== camerasData.length - 1 ? dataToBeAdded[1] : ''}
      </div>
    `;

    
  
    chartSection.innerHTML = innerHtmlForReport;
    
    // loading.replaceWith(chartSection);
  
   main.appendChild(chartSection);

    const currentGraph = document.getElementById(`${cameraData._id}-graph`).getContext("2d");
    const TotalCount = document.getElementById(`${cameraData._id}-totalCount`);
    const AverageCount = document.getElementById(`${cameraData._id}-averageCount`);
    const MaxCount = document.getElementById(`${cameraData._id}-maxCount`);
    const CurrentCount = document.getElementById(`${cameraData._id}-currCount`);
  

  const gradient = currentGraph.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, 'rgba(0,125,252,0.4)');   
  gradient.addColorStop(0.5, 'rgba(0,125,252,0.1)');
  gradient.addColorStop(1, 'rgba(18,18,18,0)');

  let prevTime = new Date(new Date().getTime() + 10 * 1000)
        .toTimeString()
        .toString()
      .slice(0, 8);
    
    const dummyGraphData = {
    graphWeek: [
      {
        Day: "Monday",
        Count : 42
      },
       {
        Day: "Tuesday",
        Count : 30
      },
       {
        Day: "Wednesday",
        Count : 44
      },
       {
        Day: "Thursday",
        Count : 70
      },
       {
        Day: "Friday",
        Count : 50
      },
       {
        Day: "Saturday",
        Count : 80
      },{
        Day: "Sunday",
        Count : 100
      }
    ],
    graphDay: [
      {
        Time: '06:00',
        Count : 13
      }
      ,
      {
        Time: '12:00',
        Count : 30
      },
      {
        Time: '18:00',
        Count : 48
      },
      {
        Time: '21:00',
        Count : 70
      },
      {
        Time: '23:00',
        Count : 45
      },
    ]
  }

  const config = {  
        type: "line",
        data: {
            labels: [],
            datasets: [
            {
                    label: "Count",
                    font: {
                    color : "#3c98ff",
                },
                data: [],
                fill: true,
                borderColor: ["rgba(0, 125, 252, 1)"],
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.1,
                spanGaps: true,
                showLine: true,
                line: {
                    pointRadius : 0
                }
            },
            ],
        },
        options: {
        animation: true,
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    color: "#3c98ff",
                    font: 20,
                    padding: 20,
                },
                min: 0,
                suggestedMax : 10,
                title: {
                    text: "Count",
                    display: true,
                    font: {
                        size : 16
                    },
                    color :  "#3c98ff"
                },
                grid: {
                drawBorder: true,
                color: "#84beff",
                drawOnChartArea: false,
                tickWidth: 2,
                borderColor: "#3c98ff",
                borderWidth : 2
            }
          },
            x: {
                beginAtZero: true,
                ticks: {
                    color: "#3c98ff",
                    font: 20,
                    padding: 20,
                },
                min: 0,
                suggestedMax : 100,
                title: {
                    text: "Time",
                    display: true,
                    font: {
                        size : 16
                    },
                    color :  "#3c98ff"
                },
                grid: {
                drawBorder: true,
                color: "#84beff",
                drawOnChartArea: false,
                tickWidth: 2,
                borderColor: "#3c98ff",
                borderWidth : 2
            }
            }
        },
        layout: {
          padding: 20,
        },
        plugins: {
            legend: {
                labels: {
                    font:{
                        size: 14,
                    },
                color:  "white",
            },
          },
        },
      },
    };
     let live = false;
      let current = 0;
      let max = 0;
    let average = 0;
    const updatedData = []
      const updatedLabels = []
  
  const GRAPH = new Chart(currentGraph, config);
    if (index !== camerasData.length - 1) {
      const countSource = new EventSource(`/count_stream/${cameraData._id}`);
      const graphSource = new EventSource(`/graph/${cameraData._id}`);

      
     
    
      countSource.onmessage = event => {
        const data = JSON.parse(event.data);
        totalCountArray[index] = data.count;
        CurrentCount.textContent = data.count
        current = data.count;
        TotalCount.textContent = sum();
      };

      graphSource.onmessage = event => {
        const data = JSON.parse(event.data);
        const currTime = new Date().toTimeString().toString().slice(0, 8);
        updatedLabels.push(currTime)
        updatedData.push(data.value)
        if (updatedData.length > max_size + 1) {
          updatedLabels.shift();
          updatedData.shift();
        }
      };
    }
    else {
      setInterval(() => {
         const currTime = new Date().toTimeString().toString().slice(0, 8);
        updatedLabels.push(currTime)
      updatedData.push(sum())
        current = sum();
        CurrentCount.textContent = current
        if (updatedData.length > max_size + 1) {
          console.log(updatedData.length)
          updatedLabels.shift();
          updatedData.shift();
      }
      },1000)
     
      
    }
    
    const display = () => {
        average += current;
        const currTime = new Date().toTimeString().toString().slice(0, 8);
        if (prevTime == currTime) {
            average /= 10;
            AverageCount.textContent = average.toFixed(0);
            average = 0
            prevTime = new Date(new Date().getTime() + 10 * 1000).toTimeString().toString().slice(0, 8);
        }
       
        if (current > max) {
            max = current;
        }
        MaxCount.textContent = max.toFixed(0);
      if (live) {
          
            config.data.labels = updatedLabels
            config.data.datasets[0].data =updatedData
            GRAPH.update();
        }
    };
  
  const graphSwitch = document.querySelectorAll(`.option-${cameraData._id}`);
    
  setInterval(display, 1000)

  graphSwitch.forEach(ele => {
      ele.addEventListener('click', e => {
        const target = e.target.dataset.option
        if (e.target.dataset.option === `${cameraData._id}-week`) {
          
          live = false
          config.data.datasets[0].data = []
          config.data.labels = []
          config.data.datasets[0].data = dummyGraphData.graphWeek.map(val => val.Count);
          config.data.labels = dummyGraphData.graphWeek.map(val =>  val.Day);
          GRAPH.update();
        }
        else if (e.target.dataset.option === `${cameraData._id}-live`) {
          
         live = true
        }
        else if (e.target.dataset.option === `${cameraData._id}-day`) {
          
          live = false
          config.data.datasets[0].data = []
          config.data.labels = []
          config.data.datasets[0].data = dummyGraphData.graphDay.map(val => val.Count);
          config.data.labels = dummyGraphData.graphDay.map(val => val.Time);
          GRAPH.update();

        }

        graphSwitch.forEach(p => {
          
          if (p.getAttribute('data-option') !== target) {
                p.style.color = "ALICEBLUE";
            }
        })
        ele.style.color = "rgb(49 189 255)";
      })
    })
  })

}


