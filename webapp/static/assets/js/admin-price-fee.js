$(function () {
    $('input').attr('disabled', true);
    $('.btn-success').hide();
  $(".datepicker").datepicker({ 
        autoclose: true, 
        todayHighlight: true,
        format: 'dd/mm/yyyy'
  });
});

  $('.btn-info').on('click',function(){
     $('input').attr('disabled',false);
     $('.btn-success').show();
  });

  var arr = {}

  $('input').on('change',function(){

    var id = $(this).data('id');
    var name = $(this).attr('name');
    var value = $(this).val();

    if (id in arr){
      for (obj of arr[id]){
         if(obj['name'] == name){
            obj['value'] = value;
            return;
         }
      }
        arr[id].push({
          'name':name,
          'value': value,
           });
    }
    else{
      arr[id] = [{
          'name':name,
          'value': value,
           }]
    }
  });

 $('#updateForm').on('submit',function(e){
    e.preventDefault();
    var all_arry = JSON.stringify(arr);
    $.ajax({
      url: url,
      type: 'post',
      data:{
        'csrfmiddlewaretoken': token,
        'all_arry' : all_arry
      },
      success: function(response){
        console.log(response);
        window.location.reload();
      },
    });


  });
