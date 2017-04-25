function sweetPost(ajax_url, post_data, success_function){
    $.ajax({
        type: 'POST'
        url: ajax_url,
        data: post_data,
        dataType: 'json',
        success: success_function(data){
            if data.success {};
        }
    })
}

function sweetAlert(title, text, confirm_text){
  swal({
      title: title,
      text: text,
      type: "warning",
      showCancelButton: true,
      confirmButtonClass: "btn-danger",
      confirmButtonText: confirm_text,
      cancelButtonText: "Anuluj",
      closeOnConfirm: false
    },
  function(){
      sweetPost(ajax_url, post_data, success_function=undefined)
  });
}


