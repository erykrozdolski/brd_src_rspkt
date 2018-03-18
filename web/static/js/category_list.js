var category_ajax_url = '/category/'

$('#category_table').on("click", ".delete_category", function(event){
    let idk = $(this).data('idk');
    let post_data = { 'cmd': 'delete_category', 'idk': idk};
    let button = $(this);

    function success_function(post_data){
        $('#'+idk).hide();
    }
    sweetAlert('Czy na pewno chcesz usunąć kategorię?', 'Zmiany są nieodwracalne', 'Usuń', category_ajax_url,
                post_data, success_function=success_function)
});


