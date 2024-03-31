const allVideoOptions = document.querySelectorAll('.option');
const videoContainer = document.getElementById('videoContainer')
const source = document.getElementById('src');


allVideoOptions.forEach(preview => {
    preview.addEventListener('click', (e) => {
        console.log(e.target)
        source.setAttribute('src', e.target.dataset.src)
        
        const target = e.target;

        videoContainer.load();
        videoContainer.setAttribute('controls', true)
        
        videoContainer.play();
        
        allVideoOptions.forEach(p => {
            if (p !== target) {
        
                p.style.color = "#232D39";
            }
        })
        preview.style.color = "#007dfc";
        
})
})


