var idk = $('#idk').val();

var ajax_url = '/administration/article_creator/'
var add_url = ajax_url + 'add/'
var edit_url = ajax_url + 'edit/'
var delete_url = ajax_url + 'delete/'

$( function() {
$( "#sortable" ).sortable();
$( "#sortable" ).disableSelection();
});

function add_component_success(data, header, modal, kind){
    $('.html_templates li').clone().appendTo('.articleSkeleton');
    $('.articleSkeleton li:last-child ').attr('id', data.idk);
    $('#'+data.idk).prepend(data.kind);
    $('#'+data.idk +" .header_name").text(header);
    $('#'+data.idk +" .editComponent").attr('data-target', '#edit' + capitalize(kind) + 'Modal');
    $('#'+data.idk +" .component_idk").val(data.idk);
    $('#'+data.idk +" .component_idk").attr('name', 'component_idk');
    $('#'+data.idk +" .component_position").attr('name', 'component_position');
    $(modal).modal('hide');
}

function edit_component_success(data, header, modal,kind, input, componentData,idk){
    $(modal.concat(" ","#id_header")).val(header);
    $(modal.concat(" ",input)).val(componentData);
    $('#'+idk+' '+'.header_name').text(header);
    $(modal).modal('hide');
}

function postComponent(url, modal, input, kind, success_function=none){
    var componentData = $(modal+' '+input).val();
    var header = $(modal.concat(" ","#id_header")).val();
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

function fillEditedForm(clicked){
    let idk = clicked.closest('li').attr('id');
    var post_data = {'idk': idk, 'cmd': 'before_edit'};
    $.ajax({
        type: 'POST',
        url: edit_url,
        data: post_data,
        dataType: 'json',
        success: function (data) {
            if (data.success){
                var input = $(data.modal.concat(" ", data.input_el)).val(data.component_data);
                var header = $(data.modal.concat(" ", "#id_header")).val(data.header);
                $(data.modal).attr('data-idk', idk);
            }
        }
    });
}


$('.articleSkeleton').delegate(".editComponent", "click", function(){
    fillEditedForm($(this));
})

$('.articleSkeleton').delegate(".editImage", "click", function(){
    fillEditedImage($(this));
});

$('.articleSkeleton').delegate(".deleteComponent", "click", function() {
    let li = $(this).parent()
    let idk = li.attr('id');
    let post_data = {'idk': idk};
    function hideComponent(){li.remove()};
    sweetAlert('Czy na pewno chcesz usunąć ten element?', '', 'Usuń', delete_url, post_data=post_data, success_function=hideComponent);
})

$('#addParagraph').click(function(){
    postComponent(add_url, '#newParagraphModal','#id_text', 'text', add_component_success);
});

$('#editParagraph').click(function(){
    postComponent(edit_url, '#editTextModal', '#id_text', 'text', edit_component_success)
});

$('#addQuote').click(function(){
    postComponent(add_url, '#newQuoteModal', '#id_quote','quote', add_component_success);
});

$('#editQuote').click(function(){
    postComponent(edit_url, '#editQuoteModal', '#id_quote', 'quote', edit_component_success)
});

$('#addVideo').click(function(){
    postComponent(add_url, '#newUrlModal', '#id_url', 'url', add_component_success);
});

$('#editVideo').click(function(){
    postComponent(edit_url, '#editUrlModal', '#id_url', 'url', edit_component_success);
});

$('#editImage').click(function(){
    postComponent(edit_url, '#editImageModal', '#id_image', 'image', edit_component_success);
});


$('#addImage').click(function(){
    var data = new FormData($('#new-image-form').get(0));
    var header = $('#id_header').val();
    $.ajax({
        url: add_url,
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.success){
                $('.html_templates li').clone().appendTo('.articleSkeleton');
                $('.articleSkeleton li:last-child ').attr('id', data.idk);
                $('#'+data.idk).prepend(data.kind);
                $('#'+data.idk +" .header_name").text(header);
                $('#'+data.idk +" .editComponent").attr('data-target', '#edit' + capitalize(data.kind) + 'Modal');
                $('#'+data.idk +" .editComponent").attr('class', 'pull-right editImage');
                $('#'+data.idk +" .editComponent").removeClass("editComponent" ).addClass( "editImage" );
                $('#'+data.idk +" .component_idk").val(data.idk);
                $('#'+data.idk +" .component_idk").attr('name', 'component_idk');
                $('#'+data.idk +" .component_position").attr('name', 'component_position');
                $('#newImageModal').modal('hide');
        }
    }});
});



function fillEditedImage(clicked){
    let idk = clicked.closest('li').attr('id');
    var post_data = {'idk': idk, 'cmd': 'before_edit'};
    $.ajax({
        type: 'POST',
        url: edit_url,
        data: post_data,
        dataType: 'json',
        success: function (data) {
            if (data.success){
                var input = $(data.modal.concat(" ", data.input_el)).val(data.component_data);
                var header = $(data.modal.concat(" ", "#id_header")).val(data.header);
                $(data.modal).attr('data-idk', idk);
            }
        }
    });
};

$('#article_form').submit(function() {
    $("#sortable .component_position").each(function() {
      $(this).val($(this).parent().index());
    });
    return true;
});


