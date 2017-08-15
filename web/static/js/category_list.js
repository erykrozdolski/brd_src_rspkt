function postComponent(url, modal, input, kind, success_function=none){
    var idk = $(modal).attr('data-idk');
    var post_data = {'header': header, 'kind': kind, 'idk': idk};
    post_data[kind] = componentData;

}

$('#addSection').click(function(){
    var post_data = {};
    $.post('/administration/category_list/', post_data, function(data){

    });
});
