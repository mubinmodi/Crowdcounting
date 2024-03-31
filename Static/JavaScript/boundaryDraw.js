const X = document.getElementById("X");
const Y = document.getElementById("Y");
const cameraDisplay = document.getElementById('cameraDisplay');
const reset = document.getElementById('reset');
const c1 = document.getElementById('c1');
const c2 = document.getElementById('c2');
const form = document.getElementById('form');
const cord1x = document.getElementById('cord1x');
const cord2x = document.getElementById('cord2x');
const cord1y = document.getElementById('cord1y');
const cord2y = document.getElementById('cord2y');

let TLBR = [[0, 0], [0, 0]];
let click = 2;

const calculate = () => {
    const updatedTLBR = [
        [
            Math.min(TLBR[0][0], TLBR[1][0]),
            Math.min(TLBR[0][1], TLBR[1][1])
        ],
        [
            Math.max(TLBR[0][0], TLBR[1][0]),
            Math.max(TLBR[0][1], TLBR[1][1])
        ]

    ];
    return updatedTLBR;
}

const coordinates = (e) => {
    X.textContent = `X : ${e.offsetX}`;
    Y.textContent = `Y : ${e.offsetY}`;
    
    TLBR[1][0] = e.offsetX;
    TLBR[1][1] = e.offsetY;
    
    if (click == 1) {
        const updatedTLBR = calculate();  
        draw.style.left = updatedTLBR[0][0] + 'px';
        draw.style.top = updatedTLBR[0][1] + 'px';
        draw.style.width = updatedTLBR[1][0] - updatedTLBR[0][0] + 'px';
        draw.style.height = updatedTLBR[1][1] -updatedTLBR[0][1] + 'px';
    }
     
}

const storeCoordinates = (e) => {
    if (click == 2) {
        TLBR[0][0] = e.offsetX;
        TLBR[0][1] = e.offsetY;
        c1.textContent = `1st Coordinate : (${TLBR[0][0]} , ${TLBR[0][1]})`;
        const updatedTLBR = calculate();  
        draw.style.left = updatedTLBR[0][0] + 'px';
        draw.style.top = updatedTLBR[0][1] + 'px';
        draw.style.opacity = 1;
        click--;
        cord1x.value = Math.floor(TLBR[0][0]);
        cord1y.value = Math.floor(TLBR[0][1]);
        
    }
    else if (click == 1) {
        TLBR[1][0] = e.offsetX;
        TLBR[1][1] = e.offsetY;
        c2.textContent = `2nd Coordinate : (${TLBR[1][0]} , ${TLBR[1][1]})`
        const updatedTLBR = calculate();  
        draw.style.width = updatedTLBR[1][0] - updatedTLBR[0][0] + 'px';
        draw.style.height = updatedTLBR[1][1] -updatedTLBR[0][1] + 'px';
        draw.style.opacity = '1';
        
        cord2x.value = Math.floor(TLBR[1][0]);
        cord2y.value = Math.floor(TLBR[1][1])
        click--;
        
    }
    else {
        console.log("no clicks left")
    }
    console.log(TLBR)

}


cameraDisplay.addEventListener('mousemove', coordinates)
cameraDisplay.addEventListener('click', storeCoordinates)
reset.addEventListener('click', () => {
    click = 2;
    TLBR = [[0, 0], [0, 0]]; 
    c1.textContent = `1st Coordinate : (${TLBR[0][0]} , ${TLBR[0][1]})`;
    c2.textContent = `2nd Coordinate : (${TLBR[1][0]} , ${TLBR[1][1]})`;
    cord1x.value = 0;
    cord2x.value = 0;
    cord1y.value = 0;
    cord2y.value = 0;
    
    draw.style.height = 0;
    draw.style.width = 0;
    draw.style.top = 0;
    draw.style.left = 0;
    draw.style.opacity = 0;
})


