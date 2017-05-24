var ajax_url = '/article_list/ajax/'


$('.deleteButton').click(function(){
    let idk = $(this).data('idk');
    let post_data = { 'cmd': 'deleteArticle', 'idk': idk};
    sweetAlert('Czy napewno chcesz usunąć artykuł?', 'Zmiany są nieodwracalne', 'Usuń', ajax_url, post_data);
});

