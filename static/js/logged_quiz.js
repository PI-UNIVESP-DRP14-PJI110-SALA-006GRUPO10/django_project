$(document).ready(function() {
    $('#questionForm').on('submit', function(e) {
        e.preventDefault();
        $.post('/quiz/', $(this).serialize(), function(data) {
            $('#question').text(data.question_text);
            $('input[name="question_id"]').val(data.question_id);
        });
    });
});