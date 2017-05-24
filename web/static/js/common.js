function sweetPost(ajax_url, post_data, success_function=undefined){
    $.ajax({
        type: 'POST',
        url: ajax_url,
        data: post_data,
        dataType: 'json',
        success: function (data){
            if (data.success){
                success_function();
            }
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

function simplePost(url, post_data, success_function=none){
    $.ajax({
        type: 'POST',
        url: url,
        data: post_data,
        dataType: 'json',
        success: function (data) {
            if (data.success){
                success_function();
            }
        }
    })
};

function capitalize(s){
    return s[0].toUpperCase() + s.slice(1);
};
