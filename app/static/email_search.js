$(document).ready(function() {
    const emailInput = $('#emailInput');
    const emailOptions = $('#emailOptions');

    emailInput.on('input', function() {
        const searchTerm = $(this).val();

        if (searchTerm) {
            $.get(`/search_emails?query=${searchTerm}`, function(emails) {
                emailOptions.html('');

                emails.forEach(function(email) {
                    const option = $('<div class="email-option"></div>').text(email);
                    option.on('click', function() {
                        emailInput.val(email);
                        emailOptions.html('');
                    });
                    emailOptions.append(option);
                });
            });
        } else {
            emailOptions.html('');
        }
    });
});

$(document).ready(function() {
    $('#emailInput').on('input', function() {
        var query = $(this).val();
        $.get('/search_emails', { query: query }, function(data) {
            var options = '';
            for (var i = 0; i < data.length; i++) {
                options += '<option value="' + data[i] + '">' + data[i] + '</option>';
            }
            $('#emailOptions').html(options);
        });
    });
});

