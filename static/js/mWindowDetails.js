var maintenance_list = $('#dataTable').DataTable();

$(document).ready(function(){
  maintenance_list.destroy();
  maintenance_list = $('#dataTable').DataTable({
    // select: true,
    'columnDefs': [
      {
        "targets": [2],
        "visible": false,
        "searchable": false
      }
    ]
  });
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

function insert_value(data_field, textbox_id){
  if (data_field) {
    $("#" + textbox_id).val(data_field);
    $("#" + textbox_id).removeAttr("hidden");
  }
  else {
    $("#" + textbox_id).attr("hidden", true);
  }

}

$("#get_all_windows").on('click', function(e) {
    console.log("get all from tenant");

    e.preventDefault(); // avoid to execute the actual submit of the form.
    if($("#id_cluster_name").val() !== ""){

      var form = $('#get_window_list');
      var url = form.attr('action');
      var csrftoken = getCookie("csrftoken");
      $.ajax({
            type: "POST",
            url: "/maintenance/get_all_windows",
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
                  maintenance_window['description'],
                  maintenance_window['id']
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
    console.log("get single");

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log(maintenance_list.row(".selected").data()[2]);
    var selected_item = {
      "window_id": maintenance_list.row(".selected").data()[2],
      "cluster_name": $("#id_cluster_name").val(),
      "tenant_name":  $("#id_tenant_name").val()
    }


    var form = $('#view_window');
    var url = form.attr('action');
    var csrftoken = getCookie("csrftoken");
    $.ajax({
          type: "POST",
          url: "/maintenance/get_window_details",
          data: selected_item, // serializes the form's elements.
          dataType: "json",
          headers: {
            "X-CSRFToken": csrftoken
          },
          success: function(returned_data)
          {
            var status_field = $('#status_area')
            status_field.removeClass()
            status_field.empty();

            status_field.addClass("alert alert-success")
            status_field.append("<strong>Success!</strong")
            
            insert_value(returned_data['name'], "maintenance_window_name");
            insert_value(returned_data['description'], "maintenance_window_desc");
            insert_value(returned_data['type'], "window_plan");
            
            insert_value(returned_data['suppression'], "window_suppression");
            // insert_value(returned_data['scope'], "maintenance_window_name");
            insert_value(returned_data['schedule']['recurrenceType'], "window_recurrence");
            if (returned_data['schedule'].hasOwnProperty("recurrence")){
              insert_value(returned_data['schedule']['recurrence']['dayOfWeek'], "maintenance_day_of_week");
              insert_value(returned_data['schedule']['recurrence']['dayOfMonth'], "maintenance_day_of_month");
              insert_value(returned_data['schedule']['recurrence']['startTime'], "maintenance_start_time");
              insert_value(returned_data['schedule']['recurrence']['durationMinutes'], "maintenance_duration_minutes");
            }
            else {
              insert_value(undefined, "maintenance_day_of_week");
              insert_value(undefined, "maintenance_day_of_month");
              insert_value(undefined, "maintenance_start_time");
              insert_value(undefined, "maintenance_duration_minutes");
            }
            insert_value(returned_data['schedule']['start'], "maintenance_start");
            insert_value(returned_data['schedule']['end'], "maintenance_end");
            insert_value(returned_data['schedule']['zoneId'], "maintenance_zone_id");
            console.log(returned_data);


          },
          error: function(returned_data)
          {
            var status_field = $('#status_area')
            status_field.removeClass()
            status_field.empty();

            status_field.addClass("alert alert-danger")
            status_field.append("<strong>Unable to fetch windows!</strong")

          }
        });
  });

$("#dataTable tbody").on( 'click', 'tr', function () {
  var table = $('#dataTable').DataTable();
  var id = table.row( this ).id();
  console.log("ID: " + id);
  console.log("clicked row");
  // if ($(this).hasClass('selected')) {
    // $(this).removeClass('selected');
    // console.log("remove select")
  // }
    maintenance_list.$('tr.selected').removeClass('selected');
  $(this).addClass('selected');
  console.log("add select");
  console.log(maintenance_list.rows( { selected: true } ).data());
  console.log(maintenance_list.rows( { selected: true } ).count())
  console.log(maintenance_list.row( this ).id())

});