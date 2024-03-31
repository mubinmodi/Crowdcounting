
const add = document.getElementById('addCamera')
const backdrop = document.getElementById('backdrop');
const addForm = document.querySelector('.addForm');
const ipGetter = document.getElementById('ipGetter');
const submit = document.getElementById('submitBtn');



add.addEventListener('click', () => {
    console.log(1)
    backdrop.classList.toggle('closedModal');
    addForm.classList.toggle('FormOpen');
    
})

backdrop.addEventListener('click', () => {
    backdrop.classList.toggle('closedModal');
    addForm.classList.toggle('FormOpen');
})



// ipGetter.addEventListener('keyup', () => {
    
//     console.log(ipGetter.value);
//     submit.setAttribute('href', `/config/${ipGetter.value}`)
//     console.log(`/config/${ipGetter.value}`)
// })

