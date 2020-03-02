$('.delete').on('click', function() {
    window.history.back();
  });
	


// LOGIN JS

$('.login').on("click", function() {
  
var $inputs = $('#login_form :input');

var values = {};
$inputs.each(function() {
  values[this.name] = $(this).val();
});
var error_list  =[];
var submit = true;

if (values['email'] == null || values['email'] == "") {
  passwordError = "Please enter Email";
  error_list.push(passwordError);
  submit = false;
}

if (values['password'] == null || values['password']  == "") {
  passwordError = "Please enter password";
  error_list.push(passwordError);
  submit = false;
}

if (error_list.length > 0){
    $('.alert-danger').show();
    $('.alert-danger').html("");
    var i;
    for (i = 0; i<error_list.length; i++){
      $('.alert-danger').append('<p>'+ error_list[i]+'</p><hr>')
        $('html, body').animate({
        scrollTop: $(".alert-danger").offset().top
    },1);
    }

  }
  return submit;

 });

// end login js 


// registration js


$('.register').on("click", function() {

  var $inputs = $('#register_form :input');

  var values = {};
  $inputs.each(function() {
    values[this.name] = $(this).val();
  });
  var error_list  =[];
  var submit = true;

  if (values['first_name'] == null || values['first_name'] == "") {
    nameError = "Please enter first name";
    error_list.push(nameError);
    submit = false;
  }
   var f_length = (values['first_name']) 
  if (f_length.length < 2) {
    nameError = "Please enter  minimum 2 character in First Name";
    error_list.push(nameError);
    submit = false;
  }
  if (values['last_name'] == null || values['last_name'] == "") {
    last_nameError = "Please enter last name";
    error_list.push(last_nameError);
    submit = false;
  }
   var lastname_length = (values['last_name']) 
  if (lastname_length.length < 2) {
    nameError = "Please enter  minimum 2 character in Last Name";
    error_list.push(nameError);
    submit = false;
  }

   if (values['email'] == null || values['email'] == "") {
    emailError = "Please enter email";
    error_list.push(emailError);
    submit = false;
  }
  var useremail = $('#Email').val();
  var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i

if(!pattern.test(useremail))
  {
   error_list.push('not a valid e-mail address');
  }


if (values['remail'] == null || values['remail'] == "") {
    repeat_emailError = "Please enter confirm email";
    error_list.push(repeat_emailError);
    submit = false;
  }
  if (values['email'] != values['remail']) {
    emailNotmatch = "Email does not match";
    error_list.push(emailNotmatch);
    submit = false;
  }
  if (values['check_email'] == "false") {
    repeat_emailError = "Email Already Exist";
    error_list.push(repeat_emailError);
    submit = false;
  }
  if (values['password'] == null || values['password'] == "") {
    passwordError = "Please enter password";
    error_list.push(passwordError);
    submit = false;
  }
  if (values['confirm_password'] == null || values['confirm_password'] == "") {
    confirm_passwordError = "Please enter confirm password";
    error_list.push(confirm_passwordError);
    submit = false;
  }
  if (values['password'] != values['confirm_password']) {
    passwordNotmatch = "Password does not match";
    error_list.push(passwordNotmatch);
    submit = false;
  }
  var country = $('#countryId').val();
  if (country  == null || country == "" || country == undefined){
  countryError = "Please Select Country";
  error_list.push(countryError)
  submit = false;     
  } 
  var state = $('#stateId').val();
  if (state  == null || state == "" || state == undefined){
  stateError = "Please Select State";
  error_list.push(stateError)
  submit = false;     
  } 
  var terms = $('input[name="terms"]:checked').val();
  if (terms  == null || terms == "" || terms == undefined){
    checkboxError = "Please agree with Terms";
    error_list.push(checkboxError)
    submit = false;     
  }

  if (error_list.length > 0){
    $('.alert-danger').show();
    $('.alert-danger').html("");
    var i;
    for (i = 0; i<error_list.length; i++){
      $('.alert-danger').append('<p>'+ error_list[i]+ '</p><hr>')
      $('html, body').animate({
        scrollTop: $(".alert-danger").offset().top
    }, 1);
    }

  }
 return submit;
});


$('#Email').on('focusout',function() {
var email = $('#Email').val();
  $.ajax({
   url: check_email_url,
   type: 'post',
   data:{
         'csrfmiddlewaretoken': token,
         'email':email,
    
         },
         
          success: function(response){
            if (response.status == true){
              $("input[name = 'check_email']").val('false');
              $('.alert-danger').html("");
              $('.alert-danger').show();
              $('.alert-danger').append('<p>'+  response.message +'</p>')
              $('html, body').animate({
                scrollTop: $(".alert-danger").offset().top
              },1);            
          
         }
         else{
          $("input[name = 'check_email']").val('true');
            $('.alert-danger').html("");
          $('.alert-danger').hide();
       }
      }

      });   
  })

// end registration js


// forget_password js
  
$('.forget_password').click(function() {

var values = {};
var error_list  =[];
var submit = true;

var forget_email = $('.forget-email').val();

 if (forget_email == null || forget_email=="") {
  	passwordError = "Please Enter Email";
  	error_list.push(passwordError);
  	submit = false;
  }

  if (error_list.length > 0){
  	$('.alert-danger').show();
  	$('.alert-danger').html("");

  	for (i = 0; i<error_list.length; i++){
  		$('.alert-danger').append('<p>'+ error_list[i]+'</p>')
  		$('html, body').animate({
        scrollTop: $(".alert-danger").offset().top
    },1);
  	}

  }

  return submit;
});

// end forget_password js

// new passwor js


$('.new_password').on("click", function() {
console.log()
var $inputs = $('#new_password_form :input');

var values = {};
$inputs.each(function() {
  values[this.name] = $(this).val();
});
var error_list  =[];
var submit = true;

 if (values['password'] == null || values['password'] == "") {
    passwordError = "Please enter password";
    error_list.push(passwordError);
    submit = false;
  }
  if (values['conf_password'] == null || values['conf_password'] == "") {
    confirm_passwordError = "Please enter confirm password";
    error_list.push(confirm_passwordError);
    submit = false;
  }
  if (values['password'] != values['conf_password']) {
    passwordNotmatch = "Password does not match";
    error_list.push(passwordNotmatch);
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
    },1);
    }

  }

  return submit;
});