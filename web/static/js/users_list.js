var users_list_url = '/user_list/'
$('#advanced_fields').hide();

$('table').delegate(".delete_user","click",  function(){
    let idk = $(this).data('idk');
    let post_data = { 'cmd': 'delete_user', 'idk': idk};
    let button = $(this);
    function hide_row(){
        button.closest('tr').hide(400);
    }
    sweetAlert('Czy napewno chcesz usunąć użytkownika?', 'Zmiany są nieodwracalne', 'Usuń', users_list_url, post_data, success_function=hide_row);
});

$('table').delegate(".trigger_user_status","click",  function(){
    let idk = $(this).data('idk');
    let button = $(this);
    let tr = button.closest('tr');
    if (button.attr('data-trigger') == 'block_user'){
        tr.find('.trigger_user_status').text('Odblokuj');
        tr.find('.user_status').text('zablokowany');
        var command = 'block_user';
        button.attr('data-trigger', 'unblock_user');
    } else {
        tr.find('.trigger_user_status').text('Zablokuj');
        tr.find('.user_status').text('aktywny');
        var command = 'unblock_user';
        button.attr('data-trigger', 'block_user');
    }
    let post_data = { 'cmd': command, 'idk': idk};

    simplePost(users_list_url, post_data);
});



$('#select_all').click(function(event) {
    if(this.checked) {
        $(':checkbox').each(function() {
            this.checked = true;
        });
    } else {
        $(':checkbox').each(function() {
            this.checked = false;
        });
    }
});



