var idk = $('#idk').val();
var span = '<span class="ui-icon ui-icon-arrowthick-2-n-s"></span>'
var edit_button = "<button class='pull-right' type='button' name='component'>Edytuj</button>";
var delete_button = "<button class='pull-right' type='button' name='component'>Usuń</button>";
var ajax_url = '/administration/article_creator/ajax/'

$( function() {
$( "#sortable" ).sortable();
$( "#sortable" ).disableSelection();
} );


function postComponent(cmd, modal, input){
    var componentData = $(input).val();
    var header = $(modal.concat(" ", "#id_header")).val();
    $.ajax({
        type: 'POST',
        url: ajax_url,
        data: {
            'cmd': cmd,
            'idk': idk,
            'componentData': componentData,
            'header': header,
        },
        dataType: 'json',
        success: function (data) {
            if (data.success){
                $('.articleSkeleton').append('<li class="ui-state-default component_li">'+span+header+edit_button+delete_button+'</li>');
                let hiddenValue = 'value='+data.idk+'>';
                $('.articleSkeleton').append("<input type='hidden' name='component_idk'"+hiddenValue);
                $('.articleSkeleton').append("<input class='component_position' type='hidden' name='component_position'>");

                $(modal).modal('hide');
                $(input).val('');
            }
        }
    });
}



$('#addParagraph').click(function(){
    postComponent('addParagraph','#paragraphModal','#id_text');
});

$('#addQuote').click(function(){
    postComponent('addQuote', '#quoteModal', '#id_quote');
});

$('#addVideo').click(function(){
    postComponent('addVideo', '#videoModal', '#id_video');
});

$('#addImage').click(function(){
    var data = new FormData($('#image-form').get(0));
    var header = $('#id_header').val();
    $.ajax({
        url: ajax_url,
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.success){
                let hiddenValue = 'value='+data.idk+'>';
                $('.articleSkeleton').append('<li class="ui-state-default component_li">'+span+header+edit_button+delete_button+'</li>');
                $('#'+data.idk).append(edit_button);
                $('#'+data.idk).append(delete_button);
                $('.articleSkeleton').append("<input type='hidden' name='component_idk'"+hiddenValue);
                $('.articleSkeleton').append("<input class='component_position' type='hidden' name='component_position'>");
                $('#imageModal').modal('hide');
                $('#id_image').val('');
        }
    }});
});


$('#article_form').submit(function() {
    $("#sortable  .component_position").each(function() {
      $(this).val($(this).parent().index());
    });
    return true;
});

