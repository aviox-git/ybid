
$('.delete').on('click', function() {
		window.history.back();
	});

// stripe js

	function readURL(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();
			reader.onload = function(e) {
				$('#preview').attr('src', e.target.result);
			}

			reader.readAsDataURL(input.files[0]);
		}
	}
		$("#logo-img").on('change',function() {
			var image = $(this);
				readURL(this);

		});


	function readURLS(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();
			reader.onload = function(e) {
				$('#back_img_preview').attr('src', e.target.result);
			}

			reader.readAsDataURL(input.files[0]);
		}
	}
		$("#back_doc").on('change',function() {
			var image = $(this);
	
				readURLS(this);

		});

$('.stripe').on("click",function() {

	$('.loader').show();

	var $inputs = $('#stripe_form :input');
	var values = {};
	$inputs.each(function() {
	values[this.name] = $(this).val();
		});
	var error_list  =[];
	var submit = true;
	var country = $(".countries option:selected").attr('countryid')
	var coun = $('.hidden_country').val(country);
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
 	if (values['address-1'] == null || values['address-1'] == ""){
 	   stateError = "Address Is Required";
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
 	if (values['img'] == null || values['img'] == ""){
 	   cc_numberError = "Passport Image Is Required";
 	   error_list.push(cc_numberError)
 	   submit = false;
 	}

 	if (values['img'] == values['front_image']){
 		imgError = "Both Identity documents are same";
	 	error_list.push(imgError)
	 	submit = false;
 	}

	if (values['front_image'] == null || values['front_image'] == ""){
 	   cc_numberError = "Driver license Image Is Required";
 	   error_list.push(cc_numberError)
 	   submit = false;
 	}
 	if (values['emp_number'] == null || values['emp_number'] == ""){
 	   emp_numberError = "Phone Number Is Required";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
 	if (values['ssn_number'] == null || values['ssn_number'] == ""){
 	   emp_numberError = "SSN Number Is Required";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
 	if (values['dob'] == null || values['dob'] == ""){
 	   emp_numberError = "DOB Number Is Required";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
 	if (values['routing_number'] == null || values['routing_number'] == ""){
 	   emp_numberError = "Rounting Number Is Required";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
 	if (values['account_number'] == null || values['account_number'] == ""){
 	   emp_numberError = "Account Number Is Required";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
 	if (values['retype_account_number'] == null || values['retype_account_number'] == ""){
 	   emp_numberError = "Retype Account Number Is Required";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
 	var account_num = $('.account').val();
 	var re_accout = $('.re-account').val();
 	if (account_num != re_accout){
 	   emp_numberError = "Account Number Does Not Match";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
 	if (values['last_four'] == null || values['last_four'] == ""){
 	   emp_numberError = "Last Four Account Digits Is Required";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}

 	var account_digits = (account_num).slice(-4);

 	if (values['last_four'].length > 0 && values['last_four'] != account_digits){
 	   emp_numberError = "Last Four Digits are Invalid.";
 	   error_list.push(emp_numberError)
 	   submit = false;
 	}
  	if (error_list.length > 0){
		$('.alert-danger').show();
		$('.alert-danger').html("");
		var i;
		for (i = 0; i<error_list.length; i++){
			$('.alert-danger').append('<p>'+ error_list[i]+'</p>')
		}
		$('html, body').animate({
	    scrollTop: $(".alert-danger").offset().top
		}, 1);
		$('.loader').hide();	

  }
  var for_country = $(".countries option:selected").attr('countryid');
  var state = $('#stateId').val();
  var city = $('#cityId').val();
  var address_1 =  values['address-1'];
  var address_2 = values['address-2'];
  var zip = values['zip'];
  var emp_number = values['emp_number'];
  var ssn_number = values['ssn_number'];
  var dob = values['dob'];
  var routing_number = values['routing_number'];
  var account_number = values['account_number'];
  var last_four = values['last_four'];
  var front_image = $('input[name="front_image"]').prop('files')[0];
  var img = $('input[name="img"]').prop('files')[0];
  
  var formdata = new FormData();
  formdata.append('for_country', for_country);
  formdata.append('state', state);
  formdata.append('city', city);
  formdata.append('address_1', address_1);
  formdata.append('zip', zip);
  formdata.append('emp_number', emp_number);
  formdata.append('ssn_number', ssn_number);
  formdata.append('dob', dob);
  formdata.append('routing_number', routing_number);
  formdata.append('account_number', account_number);
  formdata.append('front_image', front_image);
  formdata.append('img', img);
  formdata.append('csrfmiddlewaretoken',token);

  if (submit==true){
  	  $.ajax({
		   url: urls,
		   type: 'post',
		   cache : false,
		   processData : false, 
		   contentType : false,
		   data: formdata,
		         
	       success: function(response){
	       	if (response.status==true){
	       		window.location.href = response.url
	       	}
	       	else{
	       		$('.loader').hide();
	       		$('.alert-danger').html("");
	            $('.alert-danger').append('<p>'+  response.message +'</p>')
	            $('.alert-danger').show();

	             $('html, body').animate({
	            	scrollTop: $(".alert-danger").offset().top
	            },1); 

	       	}
	  		}

	});
  }
})
$(function() {
  $( "#dob" ).datepicker({
        autoclose: true, 
        todayHighlight: true,
         endDate: '-18y'
          })
})


// stripe js end