var ajax_url = '/article_list/ajax/'


$('.deleteButton').click(function(){
    let idk = $(this).data('idk');
    let post_data = { 'cmd': 'deleteArticle', 'idk': idk};
    let button = $(this);
    function hide_row(){
        button.closest('tr').hide(400);
    }
    sweetAlert('Czy napewno chcesz usunąć artykuł?', 'Zmiany są nieodwracalne', 'Usuń', ajax_url, post_data, success_function=hide_row);
});


$('.article_table').click(function(event) {
    if(this.checked) {
        $(':checkbox').each(function() {
            this.checked = true;
        });
    }
});