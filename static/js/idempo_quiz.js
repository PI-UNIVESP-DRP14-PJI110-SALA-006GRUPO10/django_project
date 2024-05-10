document.addEventListener("DOMContentLoaded", function() {
    const allQuestions = document.querySelectorAll('.quiz-question');
    let currentSetIndex = 0;

    function showNextSet() {
        allQuestions[currentSetIndex].style.display = 'none';
        if (currentSetIndex + 1 < allQuestions.length) {
            allQuestions[currentSetIndex + 1].style.display = 'none';
        }

        currentSetIndex += 2;
        if (currentSetIndex < allQuestions.length) {
            allQuestions[currentSetIndex].style.display = 'block';
            if (currentSetIndex + 1 < allQuestions.length) {
                allQuestions[currentSetIndex + 1].style.display = 'block';
            }
        } else {
            document.getElementById('submitBtn').style.display = 'block';
        }
    }

    allQuestions.forEach(question => {
        question.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', function() {
                const questionId = this.getAttribute('data-question');
                const allButtonsInGroup = document.querySelectorAll(`button[data-question="${questionId}"]`);
                allButtonsInGroup.forEach(btn => btn.classList.remove('selected-btn'));
                this.classList.add('selected-btn');

                let input = document.querySelector(`input[name="q${questionId}"]`);
                input.value = this.getAttribute('data-answer');
                
                let allAnswered = true;
                let setStart = Math.floor(question.dataset.index / 2) * 2;
                for (let i = setStart; i < setStart + 2 && i < allQuestions.length; i++) {
                    if (!allQuestions[i].querySelector('input[type="hidden"]').value) {
                        allAnswered = false;
                        break;
                    }
                }

                if (allAnswered) {
                    setTimeout(showNextSet, 250);
                }
            });
        });
    });
});
