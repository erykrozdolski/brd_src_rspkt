var ajax_url = '/article_list/ajax/'

function sweetPost(ajax_url, post_data, success_function=undefined){

    $.ajax({
        type: 'POST',
        url: ajax_url,
        data: post_data,
        dataType: 'json',
        success: function (data){
            if (data.success){

            } else {

            }
        }
    })
}

function sweetAlert(title, text, confirm_text, ajax_url=undefined, post_data=undefined, success_function=undefined){
  swal({
      title: title,
      text: text,
      type: "warning",
      showCancelButton: true,
      confirmButtonClass: "btn-danger",
      confirmButtonText: confirm_text,
      cancelButtonText: "Anuluj",
      closeOnConfirm: false,
    },
  function(isConfirm){
    if (isConfirm){
      sweetPost(ajax_url, post_data, success_function);
    }
  }
)};




$('.deleteButton').click(function(){
    let idk = $(this).data('idk');
    let post_data = { 'cmd': 'deleteArticle', 'idk': idk};
    sweetAlert('Czy napewno chcesz usunąć artykuł?', 'Zmiany są nieodwracalne', 'Usuń', ajax_url, post_data);
});

