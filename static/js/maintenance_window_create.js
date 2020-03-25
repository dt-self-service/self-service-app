toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "2000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "show",
  "hideMethod": "fadeOut"
}

$( document ).ready(function() {
  //$( '#collapseTwo' ).addClass("show");
  $( '#nav-maintenance' ).addClass("active");
  $( '#nav-maintenance-create' ).addClass("active");
});

conditional_day_of_week = $("#div_id_window_day_of_week")
conditional_day_of_month = $("#div_id_window_day_of_month")
conditional_start_time = $("#div_id_window_start_time")
conditional_duration = $("#div_id_window_duration")

function hide_unused_fields(){
  ($('#id_window_recurrence').val() === "WEEKLY") ? conditional_day_of_week.show() : conditional_day_of_week.hide();
  ($('#id_window_recurrence').val() === "MONTHLY") ? conditional_day_of_month.show() : conditional_day_of_month.hide();
  if ($('#id_window_recurrence').val() !== "ONCE") {
    conditional_start_time.show(); 
    conditional_duration.show(); 
  } else {
    conditional_start_time.hide(); 
    conditional_duration.hide(); 
  }
}
hide_unused_fields();
$('#id_window_recurrence').on('change', hide_unused_fields);

$('#add_more_button').click(function() {
  var form_idx = $('#id_form-TOTAL_FORMS').val();
  $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
  $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$("#submit_create").on('click', function(e) {

  e.preventDefault(); // avoid to execute the actual submit of the form.

  var form = $('#create_form');
  var url = form.attr('action');
  var csrftoken = getCookie("csrftoken");
  $.ajax({
    type: "POST",
    url: "/maintenance/submit_create",
    data: form.serialize(), // serializes the form's elements.
    headers: {
      "X-CSRFToken": csrftoken
    },
    success: function(data)
    {
      toastr["success"]("Maintenance Window Created!");

    },
    error: function(data)
    {
      toastr["error"]("Failed! (Do you have all required Inputs?)");
    }
  });
});