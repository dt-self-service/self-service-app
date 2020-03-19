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

$("#get_all_windows").on('click', function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    if($("#id_cluster_name").val() !== ""){

      var form = $('#get_window_list');
      var url = form.attr('action');
      var csrftoken = getCookie("csrftoken");
      $.ajax({
            type: "POST",
            url: "/maintenance/get_window_list",
            data: form.serialize(), // serializes the form's elements.
            dataType: "json",
            headers: {
              "X-CSRFToken": csrftoken
            },
            success: function(data)
            {
              var maintenance_list = $('#dataTable').DataTable();
              maintenance_list.clear().draw();
              data['values'].forEach( maintenance_window =>
                maintenance_list.row.add([
                  maintenance_window['name'],
                  maintenance_window['description']
                ]).draw(false)
              );
              var status_field = $('#status_area');
              status_field.removeClass();
              status_field.empty();

              status_field.addClass("alert alert-success");
              status_field.append("<strong>Success!</strong");

            },
            error: function(xhr, status, error)
            {
              alert(xhr.responseText);
              var status_field = $('#status_area');
              status_field.removeClass();
              status_field.empty();

              status_field.addClass("alert alert-danger");
              status_field.append("<strong>Unable to fetch windows!</strong");

            }
          });
      }
      else{
        var status_field = $('#status_area');
        status_field.removeClass();
        status_field.empty();

        status_field.addClass("alert alert-danger");
        status_field.append("<strong>Please Choose a Cluster!</strong");
      }
  });

  $("#get_window_details").on('click', function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $('#view_window');
    var url = form.attr('action');
    var csrftoken = getCookie("csrftoken");
    $.ajax({
          type: "POST",
          url: "/maintenance/get_window_details",
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