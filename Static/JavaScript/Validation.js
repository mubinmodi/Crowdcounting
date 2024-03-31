// password client side validation

const password = document.getElementById('password');
const inputLine = document.getElementById('tooltip')
const email = document.getElementById('email');
const min = 8;
const max = 16;
const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
const emailRegex = /^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$/;

password.addEventListener('keyup', (e) => {
    
    if (regex.test(e.target.value) && e.target.value.length > min && e.target.value.length < max) {
        
        inputLine.style.color = "#54e346";
    }
    else if(e.target.value === '') {
        inputLine.style.color = "#d9d9d9";
    }
    else {
        inputLine.style.color = "#ff4646";
    }
})

const confirmPassword = document.getElementById('confirmPassword');
const iconChange = document.getElementById('iconChange');

confirmPassword.addEventListener('keyup', (e) => {

    if (e.target.value == '') {
        iconChange.className = "fas fa-check-circle";
        iconChange.style.color = "#d9d9d9";
    }
     else if(e.target.value == password.value && e.target.value != '') {
        iconChange.className = "fas fa-check-circle";
        iconChange.style.color = "#54e346"
    }
    else if (e.target.value !== password.value) {
        iconChange.className = "fas fa-times-circle";
        iconChange.style.color = "#ff4646";
    }
   
   
})

// all fields Validation
const submitButton = document.querySelector('.btn');
const allInputs = document.querySelectorAll('.input');



const check = () => {
    
    let count = 0;
    for (let inp of allInputs) {
        if (inp.value !== '') {
            count++;
        }
    }
    if (count === allInputs.length && (password.value === confirmPassword.value) && emailRegex.test(email.value)) {
        submitButton.disabled = false;
        submitButton.style.backgroundColor = "#007DFC";
    }
    else if (count !== allInputs.length || (password.value !== confirmPassword.value) || !emailRegex.test(email.value) ) {
        submitButton.disabled = true;
        submitButton.style.backgroundColor = "#191919";
    }
    setTimeout(check, 10);
}
check();  




// show Password

