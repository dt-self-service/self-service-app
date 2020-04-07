var maintenance_list = $('#dataTable').DataTable();

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
                ]).draw()
              );
              toastr["success"]("Success!");

            },
            error: function(xhr, status, error)
            {
              // alert(xhr.responseText);
              toastr["error"]("Unable to fetch windows!");
            }
          });
      }
    else{
      toastr["error"]("Please Choose a Cluster!");
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
            toastr["success"]("Success!");

            var details_table = $("#details_table").DataTable();
            details_table.clear();
            populate_details(returned_data);


          },
          error: function(returned_data)
          {
            toastr["error"]("Unable to fetch windows!");
          }
        });
  });

  // Update function re-directs to the Update page and sends the data 
  $("#update_window_details").on('click', function(e) {
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
          url: "/maintenance/update",
          data: selected_item, // serializes the form's elements.
          dataType: "json",
          headers: {
            "X-CSRFToken": csrftoken
          },
          success: function(returned_data)
          {
            toastr["success"]("Success!");

            var details_table = $("#details_table").DataTable();
            details_table.clear();
            populate_details(returned_data);


          },
          error: function(returned_data)
          {
            toastr["error"]("Unable to fetch windows!");
          }
        });
  });

// Delete page will prompt ARE YOU SURE? this will be an AJAX delete call (same page) 
$("#delete_window").on('click', function(e) {
  console.log("Delete button was clicked")
  e.preventDefault(); // avoid to execute the actual submit of the form.
  $('.confirmModal').click(function(e) {
    e.preventDefault();              
    $.confirmModal('Are you sure to delete this?', function(el) {
      console.log("Ok was clicked!")
      //do delete operation
      var selected_item = {
        "window_id": maintenance_list.row(".selected").data()[2],
        "cluster_name": $("#id_cluster_name").val(),
        "tenant_name":  $("#id_tenant_name").val()
      }
    
      var form = $('#delete_window');
      var url = form.attr('action');
      var csrftoken = getCookie("csrftoken");
      $.ajax({
            type: "POST",
            url: "/maintenance/delete_window",
            data: selected_item, // serializes the form's elements.
            dataType: "json",
            headers: {
              "X-CSRFToken": csrftoken
            },
            success: function(returned_data)
            {
              toastr["success"]("Maintenance Window successfully deleted!");
    
              var details_table = $("#details_table").DataTable();
              details_table.clear();
              populate_details(returned_data);
    
    
            },
            error: function(returned_data)
            {
              toastr["error"]("Unable to fetch windows!");
            }
          });
    });
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