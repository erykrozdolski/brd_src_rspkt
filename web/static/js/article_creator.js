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
    $('#'+data.idk +" .editComponent").attr('data-target', '#' + capitalize(kind) + 'Modal');
    $('#'+data.idk +" .component_idk").val(data.idk);
    $('#'+data.idk +" .component_idk").attr('name', 'component_idk');
    $('#'+data.idk +" .component_position").attr('name', 'component_position');
    $(modal).modal('hide');
}

function edit_component_success(data, header, modal, kind, input, componentData,idk){
    $(modal.concat(" ","#id_header")).val(header);
    $(modal.concat(" ",input)).val(componentData);
    $('#'+idk+' '+'.header_name').text(header);
    $(modal).modal('hide');
}

function postComponent(url, modal, input, kind, success_function=none){
    if (kind=='text'){
        var componentData = "chuj";
    }
    else if (kind=='image'){
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
                    $('#'+data.idk +" .editComponent").attr('data-target', '#' + capitalize(data.kind) + 'Modal');
                    $('#'+data.idk +" .editComponent").attr('class', 'pull-right editImage');
                    $('#'+data.idk +" .editComponent").removeClass("editComponent" ).addClass( "editImage" );
                    $('#'+data.idk +" .component_idk").val(data.idk);
                    $('#'+data.idk +" .component_idk").attr('name', 'component_idk');
                    $('#'+data.idk +" .component_position").attr('name', 'component_position');
                    $('#ImageModal').modal('hide');
            }
           }
        });
    }
    else{
        var componentData = $(modal+' '+input).val();
    }
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
                if (data.input_el == '#id_text'){
                    $('#id_text').text(data.component_data);
                } else {
                    var input = $(data.modal.concat(" ", data.input_el)).val(data.component_data);
                }
                var header = $(data.modal.concat(" ", "#id_header")).val(data.header);
                $(data.modal).attr('data-idk', idk);
                let button = $(data.modal.concat(' ','.confirm_button'));
                let modal_header = $(data.modal.concat(' ','.modal-title'));
                button.attr('data-cmd','edit')
                button.attr('text','edit')
                button.text(button.attr('data-edit'))
                modal_header.text(modal_header.attr('data-edit'))
            }
        }
    });
}

$('.articleSkeleton').delegate(".editComponent", "click", function(){
    fillEditedForm($(this));
})

$('body').delegate(".addComponent", "click", function(){
    let modal = $(this).attr('data-target')
    let modal_header = $(modal.concat(' ','.modal-title'));
    let button = $(modal.concat(' ','.confirm_button'))
    button.text(button.attr('data-add'))
    modal_header.text(modal_header.attr('data-add'))
    $('.modal input, textarea').each(function(){
        $(this).html('');
        $(this).val('');
    });
    $('#id_text').text('');

})


$('.articleSkeleton').delegate(".editImage", "click", function(){
    fillEditedImage($(this));
});

$('.articleSkeleton').delegate(".deleteComponent", "click", function() {
    let li = $(this).closest('li');
    let idk = li.attr('id');
    let post_data = {'idk': idk};
    function hideComponent(){li.remove()};
    sweetAlert('Czy na pewno chcesz usunąć ten element?', '', 'Usuń', delete_url, post_data=post_data, success_function=hideComponent);
})

$('#confirmText').click(function(){
    if ($(this).attr('data-cmd')=='add'){
        postComponent(add_url, '#TextModal','#id_text', 'text', add_component_success);
    } else{
        postComponent(edit_url, '#TextModal', '#id_text', 'text', edit_component_success)
    }

});

$('#confirmQuote').click(function(){
    if ($(this).attr('data-cmd')=='add'){
        postComponent(add_url, '#QuoteModal', '#id_quote','quote', add_component_success);
    } else{
        postComponent(edit_url, '#QuoteModal', '#id_quote', 'quote', edit_component_success)
    }
});

$('#confirmVideo').click(function(){
    if ($(this).attr('data-cmd')=='add'){
        postComponent(add_url, '#UrlModal', '#id_url', 'url', add_component_success);
    } else{
        postComponent(edit_url, '#UrlModal', '#id_url', 'url', edit_component_success);
    }
});

$('#confirmImage').click(function(){
    if ($(this).attr('data-cmd')=='add'){
        postComponent(add_url, '#ImageModal', '#id_image', 'image', add_component_success);
    } else{
        postComponent(edit_url, '#ImageModal', '#id_image', 'image', edit_component_success);
    }
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
                let button = $(data.modal.concat(' ','.confirm_button'));
                let modal_header = $(data.modal.concat(' ','.modal-title'));
                button.attr('data-cmd','edit')
                $('#preview_image').attr('src',data.component_data);
                $('#image_cmd_input').attr('value','editImage');
                button.text(button.attr('data-edit'))
                modal_header.text(modal_header.attr('data-edit'))

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
