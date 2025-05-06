document.getElementById('diagnosisForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent default form submission

    const form = e.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/diagnose/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Diagnosis successful:', data);
            alert(data.message); // or update the DOM with the result
        } else {
            console.error('Error:', data.error);
            alert(data.error);
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Something went wrong. Please try again.');
    }
});
