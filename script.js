// ... existing code ...

document.getElementById('flashcardForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const category = document.getElementById('flashcard-category').value;
    const subject = document.getElementById('flashcard-subject').value;
    const text = document.getElementById('flashcard-text').value;

    fetch('/add_flashcard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ category, subject, text })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        // Optionally, update the UI or notify the user
    })
    .catch(error => console.error('Error:', error));
});

function displayScoreboard() {
    const scoreList = document.getElementById('scoreList');
    students.forEach(student => {
        const listItem = document.createElement('li');
        listItem.textContent = `${student.name}: ${student.quizPoints} points`;
        scoreList.appendChild(listItem);
    });
}

document.addEventListener('DOMContentLoaded', displayScoreboard);