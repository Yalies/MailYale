let cookie = document.getElementById('cookie'),
    submit = document.getElementById('submit');

cookie.onchange = function() {
    submit.disabled = Boolean(cookie.textContent);
}

submit.onclick = function() {
    if (submit.classList.length == 0) {
        console.log('Trying to start scraper.');
        let payload = {
            'cookie': cookie.value,
        };
        fetch('/scraper', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload),
        }).then(response => {
            if (response.ok) {
                submit.textContent = 'Scraper started!';
                submit.classList.add('success');
            } else {
                submit.textContent = 'Scraper run failed.';
                submit.classList.add('fail');
            }
        });
    } else {
        submit.textContent = 'Run Scraper';
        submit.className = '';
    }
}
