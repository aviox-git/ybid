$(document).ready(function() {
	$(window).scroll(function() {
	    if ($(this).scrollTop() >= 50) {        // If page is scrolled more than 50px
	        $('#return-to-top').fadeIn(300);    // Fade in the arrow
	    } else {
	        $('#return-to-top').fadeOut(300);   // Else fade out the arrow
	    }
	});
	$('#return-to-top').click(function() {      // When arrow is clicked
	    $('body,html').animate({
	        scrollTop : 0                       // Scroll to top of body
	    }, 1000);
	});
	$(".owl-carousel").owlCarousel({
	  autoplay: true,
	  lazyLoad: true,
	  loop: true,
	  margin: 20,
	   /*
	  animateOut: 'fadeOut',
	  animateIn: 'fadeIn',
	  */
	  responsiveClass: true,
	  autoHeight: true,
	  autoplayTimeout: 7000,
	  smartSpeed: 800,
	  nav: true,
	  responsive: {
	    300: {
	      items: 1
	    },

	    600: {
	      items: 2
	    },

	    1024: {
	      items: 3
	    },

	    1366: {
	      items: 3
	    }
	  }
	});
	// $('nav li a').click(function(e) {

 //        $('nav li.active').removeClass('active');

 //        var $parent = $(this).parent();
 //        $parent.addClass('active');
 //        e.preventDefault();
 //    });
 	$('.collapse1').collapse();
 // $('.read_more').click(function() {
 // 	$(".moretext").slideToggle();
 // 	if ($('.read_more').text() == "Read More") {
 //   	 	$(this).text("Read Less")
 //  	} else {
 //    	$(this).text("Read More")
 //  	}
 // });
//  $('#ma_link').click(function($e) {
//     $e.preventDefault();
//     doSomething();
// });
/*	$('.next-btn, .next-btn-gernal').click(function() {
		$('.ticket_popups').hide();
		$('.my_order_popup').show();
	});
	$('.pay-btn, .pay-btn-gernal').click(function() {
		$('.my_order_popup').hide();
		$('.my_order1_popup').show();
	});
	$('.pay-apply-btn, .pay-apply-gernal').click(function() {
		$('.my_order1_popup').hide();
		$('.congo_page_popup').show();
		//$('.ticket_popups').show();
	});
	$('.my_order, .my_order_gernal').click(function() {
		$('.congo_page_popup').hide();
		$('.payment_popup').show();
	});
	$(".back-btn, .back-btn-gernal").click(function() {
		$('.my_order_popup').hide();
		$('.ticket_popups').hide();
	});
	$(".back-btn-1, .back-btn-gernal1").click(function() {
		$('.my_order1_popup').hide();
		$('.my_order_popup').show();
	}); */
	//ticket_popups

	//js by anil singh
    $('.next-section-popup').click(function(){
		$(this).closest('.modal-common-div').hide();
		$(this).closest('.modal-common-div').next('.modal-common-div').show();
	})
	$('.prev-section-popup').click(function(){
		$(this).closest('.modal-common-div').hide();
		$(this).closest('.modal-common-div').prev('.modal-common-div').show();
	})

	$('#tickless-modal-lg, #assigned-modal-lg').on('hidden.bs.modal',function(){

		$(this).find('.modal-common-div').hide();
		$(this).find('.modal-common-div:first').show();	
	});



});