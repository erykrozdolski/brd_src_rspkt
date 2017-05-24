var idk = $('#idk').val();
var span = '<span class="ui-icon ui-icon-arrowthick-2-n-s"></span>'


var edit_button = "<button class='pull-right editComponent' type='button' name='component' data-toggle='modal' data-target='empty_target'>Edytuj</button>";
var delete_button = "<button class='pull-right deleteComponent' type='button' name='component'>Usuń</button>";
var component_position_input = "<input class='component_position' type='hidden' name='component_position'>";
var component_li = '<li class="ui-state-default component_li"></li>'
var ajax_url = '/administration/article_creator/'
var add_url = ajax_url + 'add/'
var edit_url = ajax_url + 'edit/'
var delete_url = ajax_url + 'delete/'

$( function() {
$( "#sortable" ).sortable();
$( "#sortable" ).disableSelection();
});

function add_component_success(data, header, modal, kind){
    $('.articleSkeleton').append(component_li);
    let component_last_li = $('.articleSkeleton li:last-child')
    component_last_li.html(span+data.kind+' '+header+edit_button.replace('empty_target','#edit' + capitalize(kind) + 'Modal')+delete_button+'</li>')
    component_last_li.attr('id', data.idk);
    component_last_li.append("<input class='component_idk' type='hidden' name='component_idk'"+'value='+data.idk+'>');
    component_last_li.append(component_position_input);
    $(modal).modal('hide');
}

function edit_component_success(data, header, modal,input, componentData){
    $(modal.concat(" ","#id_header")).val(header);
    $(modal.concat(" ",input)).val(componentData);
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
                success_function(data, header, modal, kind, input, componentData);
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
                $('.articleSkeleton').append(component_li);
                let component_last_li = $('.articleSkeleton li:last-child')
                component_last_li.html(span+data.kind+' '+header+edit_button+delete_button+'</li>')
                component_last_li.attr('id', data.idk);
                component_last_li.append("<input class='component_idk' type='hidden' name='component_idk'"+'value='+data.idk+'>');
                component_last_li.append(component_position_input);
                $('#newImageModal').modal('hide');
        }
    }});
});


$('#article_form').submit(function() {
    $("#sortable .component_position").each(function() {
      $(this).val($(this).parent().index());
    });
    return true;
});


