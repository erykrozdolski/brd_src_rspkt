$('select').select2({
    placeholder: '',
    width: "100%",
    containerCssClass: "select2_container",
    allowClear: true
});



$('.dateinput').datepicker();

function sweetPost(ajax_url, post_data, success_function=undefined){
    $.ajax({
        type: 'POST',
        url: ajax_url,
        data: post_data,
        dataType: 'json',
        complete: function(post_data){
            success_function(post_data);
        }

    })
}

function sweetAlert(title, text, confirm_text='Usuń', ajax_url=undefined, post_data=undefined, success_function=undefined){

  swal({
      title: title,
      text: text,
      type: "warning",
      showCancelButton: true,
      confirmButtonClass: "btn-danger",
      confirmButtonText: confirm_text,
      cancelButtonText: "Anuluj",
    }).then(function(isConfirm){

    if (isConfirm){
      sweetPost(ajax_url, post_data, success_function);
    }
  }
)};

function simplePost(url, post_data, success_function=function(){}){
    $.ajax({
        type: 'POST',
        url: url,
        data: post_data,
        dataType: 'json',
        success: function (post_data) {
            if (data.success){
                success_function(post_data);
            }
        }
    })
};

function capitalize(s){
    return s[0].toUpperCase() + s.slice(1);
};

function readUrl(input,image) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $(image)
                .attr('src', e.target.result)
                .width(100)
                .height(100);
        };
        reader.readAsDataURL(input.files[0]);
    }
}



$('#hamburger').click(function(){
    $("#mySidenav").toggleClass('open');
    $("#hamburger").toggleClass('open');
});

$('input[type="text"]').on('change focus blur', function (e) {
    $(this).parents('.control-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
}).trigger('blur');

$('input[type="email"]').on('change focus blur', function (e) {
    $(this).parents('.control-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
}).trigger('blur');

$('input[type="password"]').on('change focus blur', function (e) {
    $(this).parents('.control-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
}).trigger('blur');

$('textarea').on('change focus blur', function (e) {
    $(this).parents('.control-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
}).trigger('blur');

$(document).ready(function(){
    $("input[type='text']").parent().siblings(".control-label").addClass("floating");
    $("input[type='password']").parent().siblings(".control-label").addClass("floating");
    $("input[type='email']").parent().siblings(".control-label").addClass("floating");
    $("textarea").parent().siblings(".control-label").addClass("floating");
    $("select").parent().siblings(".control-label").addClass("floating");
    $(".select2_container").closest('.control-group').toggleClass('focused', $(this).text() != '');
    alert($(".select2_container").text());
})

$(".select2_container").on('change focus blur', function (e){
    $(this).closest('.control-group').toggleClass('focused', (e.type === 'focus' || $(this).text() != ''));
});


$("textarea").keyup(function(){
    $(this).height("auto");
    $(this).css("padding","0")
    $(this).height(this.scrollHeight+5);
})
