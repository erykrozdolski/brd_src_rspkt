
$('#change_cover').change(function(){
    readUrl(this, '#preview_cover')
    $('#cover_info').empty();
});

$('#add_image').change(function(){
    readUrl(this, '#preview_image')
});


$('#cancel_image').click(function(){
    $('#preview_image').empty();
    $('#add_image').empty();
})