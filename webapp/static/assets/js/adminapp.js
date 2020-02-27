$(document).ready(function() {
		// Create url on add page
		$("#page_title").on('keyup',function(){
			var title=$(this).val();
			var url=title.replace(/ /g,"-");
			$("#page_url").val(url);
		})
		// Create  page url on edit page
		$("#edit_page_title").on('keyup',function(){
			var title=$(this).val();
			var url=title.replace(/ /g,"-");
			$("#edit_page_url").val(url);
		})

      // change single page-status
      $("#manage_page_tbody").on('click','.page-status',function(){
      		var page_id=$(this).attr("data-id");
			$.ajax({
				url: "page-status",
				method: "GET",
				data:{
					"page_id":page_id
				}, 
			success: function(result){
				if (result.status==true) {
					$("#manage_page_tbody").load(location.href+" #manage_page_tbody>*", "");
				}
			}
		})
	});
    // delete- single-page
	$("#manage_page_tbody").on('click','.delete-page',function(){
			var page_id=$(this).attr("data-id");
			$.ajax({
				url: "delete-page",
				method: "GET",
				data:{
					"page_id":page_id
				}, 
			success: function(result){
				if (result.status==true) {
					$("#manage_page_tbody").load(location.href+" #manage_page_tbody>*", "");
				}
			}
		})
      });
	  
	  // change all pages status
	  $(".all-page-status").click(function(){
			var status=$(this).attr('data-id');
			var selected_pages = [];
			$.each($("input[name='select_page']:checked"), function(){
				selected_pages.push($(this).val());
				});
			console.log(selected_pages);
			$.ajax({
				url: "selected-pages-status",
				method: "POST",
				data:{
					"selected_pages":selected_pages,
					"status":status,
					"csrfmiddlewaretoken":token
				}, 
				success: function(result){
					if (result.status==true) {
						$("#manage_page_tbody").load(location.href+" #manage_page_tbody>*", "");
					}
				}
			})
	});
});
function selectAllBoxes(source) {
	var checkboxes = document.querySelectorAll('input[type="checkbox"]');
	for (var i = 0; i < checkboxes.length; i++) {
		if (checkboxes[i] != source)
			checkboxes[i].checked = source.checked;
		}
}