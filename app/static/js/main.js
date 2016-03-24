
$('#flash-message').delay(1500).fadeOut('slow');

$('.flash-dismiss').click(function() {
    $(this).parent().addClass('dismissed')
});
