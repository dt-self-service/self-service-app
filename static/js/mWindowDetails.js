var maintenance_list = $('#dataTable').DataTable();

const isDict = dict => {
  return typeof dict === "object" && !Array.isArray(dict);
};

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
  var details_table = $("#details_table").DataTable();
  details_table.destroy();
  details_table = $("#details_table").DataTable({
    "ordering": false,
    "pageLength": 50
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
    $("#" + textbox_id).attr("hidden", false);
  }
  else {
    $("#" + textbox_id).attr("hidden", true);
  }

}

$("#get_all_windows").on('click', function(e) {
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

function populate_details(returned_data){
  var details_table = $("#details_table").DataTable();
  for (var k in returned_data){
    if (isDict(returned_data[k])){populate_details(returned_data[k]);}
    else{details_table.row.add([k, returned_data[k]]).draw(false);}
  }
}

  $("#get_window_details").on('click', function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
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

            var details_table = $("#details_table").DataTable();
            details_table.clear();
            populate_details(returned_data);


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
  if ($(this).hasClass('selected')) {
    $(this).removeClass('selected');
  }
  else{
    maintenance_list.$('tr.selected').removeClass('selected');
    $(this).addClass('selected');
  }
});