function submitStudentSelection() {
    const selectedStudentId = document.getElementById('studentSelect').value;
    if (selectedStudentId) {
        window.location.href = `/student/${selectedStudentId}/`; // Adjust URL as necessary
    }
}

function submitTestStudentSelection() {
    const selectedStudentId = document.getElementById('studentSelect').value;
    if (selectedStudentId) {
        window.location.href = `/quiz/${selectedStudentId}/`;
    }
}

function submitUpdateStudentSelection() {
    const selectedStudentId = document.getElementById('studentSelect').value;
    if (selectedStudentId) {
        window.location.href = `/update/${selectedStudentId}/`;
    }
}

function confirmDelete() {
    const studentId = document.getElementById('studentDeleteSelect').value;
    if (confirm('Are you sure you want to delete this student?')) {
        fetch(`/delete/${studentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'id': studentId })
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Failed to delete the student');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}