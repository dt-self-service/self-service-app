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

$("#get_all_windows").on('submit', function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $('#create_form');
    var url = form.attr('action');
    var csrftoken = getCookie("csrftoken");
    $.ajax({
          type: "POST",
          url: "/maintenance/submit_view",
          data: form.serialize(), // serializes the form's elements.
          dataType: "json",
          headers: {
            "X-CSRFToken": csrftoken
          },
          success: function(data)
          {
            var status_field = $('#status_area')
            status_field.removeClass()
            status_field.empty();

            status_field.addClass("alert alert-success")
            status_field.append("<strong>Success!</strong")

          },
          error: function(data)
          {
            var status_field = $('#status_area')
            status_field.removeClass()
            status_field.empty();

            status_field.addClass("alert alert-danger")
            status_field.append("<strong>Unable to fetch windows!</strong")

          }
        });
  });