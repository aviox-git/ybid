

    $(document).ready(function() {
    $('#example').DataTable();
} );
    $("#other_search").on("click", function(e){
  if ( $('.other_pages_search').css('display') == 'none'){
    $(".other_pages_search").css('display','block');
    $(".other_pages_search").show(50);
     e.stopPropagation();
       
  }
  else{
    $(".other_pages_search").css('display','none');
  }
  });


$(".other_pages_search").click(function(e){
    e.stopPropagation();
});

$(document).click(function(){
    $(".other_pages_search").hide();
});