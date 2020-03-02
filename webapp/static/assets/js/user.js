
// account info js


$('.update_info').on("click",function() {
	var values = {};
	var $inputs = $('#update_info_form :input');

	$inputs.each(function() {
	values[this.name] = $(this).val();
		});
	var error_list  =[];
	var submit = true;

	if (values['email'] == null || values['email'] == ""){
 	   emailError = "Email Is Required";
 	   error_list.push(emailError)
 	   submit = false;
 	}
 

 	
	var email = document.getElementById('Email').value;
	var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i

	if(!pattern.test(email)){
	 error_list.push('Not a Valid Email Address');
	 submit = false;
	}

	if ($('input[name="old_pass"]').val().trim().length > 0 ){

		var password = $("#password").val().trim();
		var conf_password = $("#confirm_password").val().trim();

		if (password.length == 0){
			error_list.push('Password is required');
	 		submit = false;
		}

		if (conf_password.length == 0){
			error_list.push('Confirm Password is required');
	 		submit = false;
		}

		if (password  !== conf_password){
			error_list.push('Passwords didnt matched');
	 		submit = false;
		}

	}

 	var venue_telephone = $('#telephone_number').val(); 
 	// var pattern = /^\+(?:[0-9] ?){6,11}[0-9]$/;

    if (venue_telephone.length!=10){
 		error_list.push('Not a Valid Telephone Number')
 		submit = false;
    } 
     if (values['billing_add'] == null || values['billing_add'] == ""){
 	   addressError = "Billing Address Is Required";
 	   error_list.push(addressError)
 	   submit = false;
 	}
   
	if (values['country'] == null || values['country'] == ""){
 	   countryError = "Country Is Required";
 	   error_list.push(countryError)
 	   submit = false;
 	}
 	if (values['state'] == null || values['state'] == ""){
 	   stateError = "State Is Required";
 	   error_list.push(stateError)
 	   submit = false;
 	}
 	if (values['city'] == null || values['city'] == ""){
 	   cityError = "City Is Required";
 	   error_list.push(cityError)
 	   submit = false;
 	}
 	if (values['zip'] == null || values['zip'] == ""){
 	   zipError = "Zip Is Required";
 	   error_list.push(zipError)
 	   submit = false;
 	}
 	if (values['cc_number'] == null || values['cc_number'] == ""){
 	   cc_numberError = "Credit Card Number Is Required";
 	   error_list.push(cc_numberError)
 	   submit = false;
 	}
 	if (values['month'] == null || values['month'] == ""){
 	   cc_numberError = "Credit Card Expiration Month is required";
 	   error_list.push(cc_numberError)
 	   submit = false;
 	}
 	if (values['year'] == null || values['year'] == ""){
 	   cc_numberError = "Credit Card Expiration Year is required";
 	   error_list.push(cc_numberError)
 	   submit = false;
 	}
 	
 	// if (values['about_seller'] == null || values['about_seller'] == ""){
 	//    about_sellerError = "About Seller is Required";
 	//    error_list.push(about_sellerError)
 	//    submit = false;
 	// }

 	
	var terms = $('input[name="terms"]:checked').val();
 	if (terms  == null || terms == "" || terms == undefined){
 			termsError = "Please agree with Terms";
		 	error_list.push(termsError)
		 	submit = false;
 	  
	}
  	if (error_list.length > 0){
  	$('.alert-danger').show();
  	$('.alert-danger').html("");
  	var i;
  	for (i = 0; i<error_list.length; i++){
  		$('.alert-danger').append('<p>'+ error_list[i]+'</p>')
  		$('html, body').animate({
        scrollTop: $(".alert-danger").offset().top
    	}, 1);
  	}

  }
  return submit;
  });


$("#logo-img").on('change',function() {
			var image = $(this);
			let img = new Image();
			img.src = window.URL.createObjectURL(event.target.files[0])
			img.onload = () => {

				if (img.width > 200 || img.height > 200){
						alert(`Invalid Image: width:${img.width} and height:${img.height}`);
						image.val("");
					}
				else{

					image.closest('.form-group').find('.cb-logo').html('');
					image.closest('.form-group').find('.cb-logo').append(`<img class="cb-log" src="${img.src}" alt="logo-img">`)
				}
			}

		});

		$('#pdf').on('change',function(){
			var src = window.URL.createObjectURL(event.target.files[0])
			$(this).closest('.form-group').find('.cb-logo').show();
			$(this).closest('.form-group').find('.cb-logo').find('a').attr('href',src);
		});
