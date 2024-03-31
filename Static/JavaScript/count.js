window.addEventListener('DOMContentLoaded', () => {

const errorContainer = document.getElementById('error-container');

fetch('/cameras-data', {
    method: "GET",
    headers: {
        'Content-Type' : 'application/json'
    }
}).
    then(response => {
        return response.json()
    }).
    then(result => {
        const cameras = JSON.parse(result);
        

        cameras.forEach(cameraData => {
            let prevCount = -1;
            let data;
            let added = false;
            const threshold = cameraData.threshold;
            

            const removingChild = (target) => {
                target.classList.add('remove');
                setTimeout(() => {
                    errorContainer.removeChild(target)
                },500)
                data = null;
                added = false;
            }

            const trigger = (data) => {
                data.onclick = (event) => {
                    if (event.target.tagName === 'I') {
                        removingChild(event.target.parentElement);
                    }
                }
            }
            const addDivison = (message) => {
                if (!added) {
                    const divError = document.createElement('div');
                    divError.setAttribute('class', `warning-msg`);
                    divError.innerHTML = `
                        <i class="fas fa-exclamation-triangle"></i>&nbsp;&nbsp;&nbsp;
                        ${message}
                        <i class="far fa-times last close"></i>
                    `;
                    errorContainer.appendChild(divError);
                    added = true;
                    return divError;
                }
                return false; 
            }

            const countSource = new EventSource(`/count_stream/${cameraData._id}`);
            countSource.onmessage = event => {
                const dataCount = JSON.parse(event.data);
                const count = dataCount.count;
                const message = `Count of ${cameraData.CameraName} has exceeded its limitting value`;
                    if (count >= threshold ) {
                        if (!data && !added && prevCount !== count) {
                            data = addDivison(message);
                        }
                    trigger(data);
                }
                    else {
                        if (data && added) {
                            removingChild(data)
                        }
                    
                }
                prevCount = count;
            };
            
        });
        

    })
    .catch(err => console.log(err));
})