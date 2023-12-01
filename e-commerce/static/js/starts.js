let html_starts = `                                        
<span class="fa fa-star checked"></span>
<span class="fa fa-star checked"></span>
<span class="fa fa-star checked"></span>
<span class="fa fa-star not_checked"></span>
<span class="fa fa-star not_checked"></span>
`

function valoracion(ele){
    elemento_id = ele.dataset.productId;
    console.log(elemento_id);
    
    let starts = '';

    fetch(`http://127.0.0.1:8000/api/producto/${elemento_id}`)
        .then(res => res.json())
        .then(res => {
            console.log(res.rating.rate);
            let entero = Math.floor(res.rating.rate);

            for (let i = 0; i < 5; i++) {
                if(i < entero)
                    starts += `<span class="fa fa-star checked" data-index="${i}"></span>`;
                else if(i == entero && res.rating.rate - entero > 0.5)
                    starts += `<span class="fa fa-star-half-o checked" data-index="${i}"></span>`;
                else
                    starts += `<span class="fa fa-star-o checked" data-index="${i}"></span>`;
            }
            starts += `<span>(${Math.round(res.rating.rate * 10)/10})(${res.rating.count})</span>`;
            ele.innerHTML = starts;

            puntuar(ele)
        })
        .catch(error => {
            alert(`Aquí hay un ${error}`);
        });
}

function puntuar(ele) {
    elemento_id = ele.dataset.productId;
    console.log(elemento_id);

    ele.querySelectorAll('.fa').forEach(star => {
        star.addEventListener('mouseover', (event) => {
            const hoverIndex = parseInt(event.target.dataset.index) + 1;
            fillStars(ele, hoverIndex);
        });

        star.addEventListener('mouseout', () => {
            valoracion(ele);
        });

        star.addEventListener('click', (event) => {
            const puntuacion = parseInt(event.target.dataset.index) + 1;
            console.log(`La valoración ha sido de: ${puntuacion}`);
            
            fetch(`http://127.0.0.1:8000/api/productos_rate/${elemento_id}/${puntuacion}`, {method: 'PUT'})
                .then(response => response.json())
                .then(data => {
                    console.log('Respuesta de la API:', data);
                    valoracion(ele);
                })
                .catch(error => {
                    console.error('Error al realizar la solicitud PUT:', error);
                });

        });
    });
}

function fillStars(ele, index) {
    ele.querySelectorAll('.fa').forEach((star, i) => {
        if (i < index) {
            star.classList.remove('fa-star-o');
            star.classList.remove('fa-star-half-o');
            star.classList.add('fa-star');
        } else {
            star.classList.remove('fa-star');
            star.classList.remove('fa-star-half-o');
            star.classList.add('fa-star-o');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const span_para_estrellas = document.querySelectorAll('span.sp')

    span_para_estrellas.forEach((ele) => {
        valoracion(ele)
    })
});