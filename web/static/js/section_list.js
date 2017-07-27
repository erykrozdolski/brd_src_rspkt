function postComponent(url, modal, input, kind, success_function=none){
    var idk = $(modal).attr('data-idk');
    var post_data = {'header': header, 'kind': kind, 'idk': idk};
    post_data[kind] = componentData
    $.ajax({
        type: 'POST',
        url: url,
        data: post_data,
        dataType: 'json',
        success: function (data) {
            if (data.success){
                success_function(data, header, modal, kind, input, componentData,idk);
            }
        }
    });
}

$('#addSection').click(function(){
    postComponent(add_url, '#newSectionModal','#id_name', 'text', add_component_success);
});
