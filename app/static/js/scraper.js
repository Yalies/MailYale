let cookie = document.getElementById('cookie'),
    submit = document.getElementById('submit');

submit.onclick = function() {
    let payload = {
        'cookie': cookie.value,
    };
    fetch('/scraper', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
    })
    /*
        .then(response => {
            response.ok
        )
    */
}
