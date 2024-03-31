const sliderbtn = document.getElementById('sliderbtn');
const nav = document.getElementById('navigation');
const icon = document.getElementById('icon');
const time = document.getElementById('time')
const dt = document.getElementById('dt')
let open = false;

sliderbtn.addEventListener('click', () => {
    console.log(1)
    if (!open) {
        nav.classList.add('open');
        sliderbtn.classList.add('open');
        icon.className = "fas fa-chevron-left";
        open = true;
    }
    else {
        icon.className = "fas fa-chevron-right";
        nav.classList.remove('open');
        sliderbtn.classList.remove('open');
        
        open = false;
    }
   
})

const months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9 : "September",
    10: "October",
    11: "November",
    12 : "December"
}

const timeFunc = () => {
    const newTime = new Date().toTimeString().toString().slice(0,8);
    time.textContent = newTime;
    if (dt) {
    const d = new Date();
    const dime = `${d.getDate()} ${months[d.getMonth() + 1]} ${d.getFullYear()} ${newTime}`;
    dt.value = dime;
    }
}

setInterval(timeFunc,1000)