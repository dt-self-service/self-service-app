$('#id_cluster_name').change(function(){
    var chosen_cluster = $(this).val();
    $.ajax({
      type: "GET",
      url: "/get_tenant",
      data: { "chosen_cluster": chosen_cluster},
      dataType: 'json',
      success: function(data){
        $('#id_tenant_name').empty()
        $.each(data, function(idx, obj) {
          $('#id_tenant_name').append($("<option />").val(obj).text(obj));
        });
      }
    });
  });