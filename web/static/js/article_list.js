var ajax_url = '/article_list/ajax/'
var article_list_url = '/article_list/'
$('#advanced_fields').hide();

$('table').delegate(".delete_article","click",  function(){
    let idk = $(this).data('idk');
    let post_data = { 'cmd': 'delete_article', 'idk': idk};
    let button = $(this);
    function hide_row(){
        button.closest('tr').hide(400);
    }
    sweetAlert('Czy napewno chcesz usunąć artykuł?', 'Zmiany są nieodwracalne', 'Usuń', article_list_url, post_data, success_function=hide_row);
});

$('table').delegate(".trigger_article","click",  function(){
    let idk = $(this).data('idk');
    let button = $(this);
    if (button.attr('data-trigger') == 'unpublish_article'){
        var button_text = 'Opublikuj';
        var button_cmd = 'publish_article';
        var command = 'unpublish_article';
    } else {
        var button_text = 'Ukryj';
        var button_cmd = 'unpublish_article';
        var command = 'publish_article';
    }
    let post_data = { 'cmd': command, 'idk': idk};
    button.text(button_text)
    button.attr('data-trigger',button_cmd)

    simplePost(article_list_url, post_data);
});


$('tbody :checkbox').change(function(){
    if (this.checked){
        $('.change_selected').prop('disabled', false);
    } else {
        $('.change_selected').prop('disabled', true);
    }
})


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


$("#search_in_articles").click(function(){
    var search_form = $('#search_form');
    $.post(ajax_url, search_form.serialize(),
        function (data) {
            $('#article_list').html(data);
        }
    );
});

$('#clear_search_form').click(function(){
    document.getElementById("search_form").reset();
});

$('#advanced_searching').click(function(){
    $('#advanced_fields').toggle(200);
})


$("#delete_selected").click(function(){
    var idks =[]
    $('tbody :checkbox:checked').each(function(){
        idks.push($(this).attr('data-idk'))
    })
    alert(idks)
})


