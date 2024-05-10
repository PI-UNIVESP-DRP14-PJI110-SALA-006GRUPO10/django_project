document.addEventListener("DOMContentLoaded", function() {
    const allQuestions = document.querySelectorAll('.quiz-question');
    let currentSetIndex = 0; // This will keep track of which set of questions we're on.

    function showNextSet() {
        // Hide current set of questions
        allQuestions[currentSetIndex].style.display = 'none';
        if (currentSetIndex + 1 < allQuestions.length) {
            allQuestions[currentSetIndex + 1].style.display = 'none';
        }

        // Show next set of questions
        currentSetIndex += 2;
        if (currentSetIndex < allQuestions.length) {
            allQuestions[currentSetIndex].style.display = 'block';
            if (currentSetIndex + 1 < allQuestions.length) {
                allQuestions[currentSetIndex + 1].style.display = 'block';
            }
        } else {
            // No more questions, show the submit button
            document.getElementById('submitBtn').style.display = 'block';
        }
    }

    // Set up event listeners for the answer buttons
    allQuestions.forEach(question => {
        question.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', function() {
                // Handle the selection marking
                const questionId = this.getAttribute('data-question');
                const allButtonsInGroup = document.querySelectorAll(`button[data-question="${questionId}"]`);
                allButtonsInGroup.forEach(btn => btn.classList.remove('selected-btn'));
                this.classList.add('selected-btn');

                // Set the value of the hidden input to the selected answer
                let input = document.querySelector(`input[name="q${questionId}"]`);
                input.value = this.getAttribute('data-answer');
                
                // Check if this set of questions is fully answered
                let allAnswered = true;
                let setStart = Math.floor(question.dataset.index / 2) * 2;
                for (let i = setStart; i < setStart + 2 && i < allQuestions.length; i++) {
                    if (!allQuestions[i].querySelector('input[type="hidden"]').value) {
                        allAnswered = false;
                        break;
                    }
                }

                if (allAnswered) {
                    showNextSet();
                }
            });
        });
    });
});
