// core 

$('.delete').on('click', function() {
    window.history.back();
  });

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
      let img = new Image();
      img.src = window.URL.createObjectURL(event.target.files[0])
      img.onload = () => {

        if (img.width > 400 || img.height > 400){
            alert(`Invalid Image: width:${img.width} and height:${img.height}`);
            image.val("");
          }
        else{

          image.closest('.form-group').find('.add-img').html('');
          image.closest('.form-group').find('.add-img').append(`<img class="cb-log" src="${img.src}" alt="logo-img">`)
        }
      }
  
});


$('.update').on("click", function() {

  var $inputs = $('#site_form :input');

  var values = {};
  $inputs.each(function() {
    values[this.name] = $(this).val();
  });
  var error_list  =[];
  var submit = true;

  if (values['site_name'] == null || values['site_name'] == "") {
    nameError = "Please Enter Site Name";
    error_list.push(nameError);
    submit = false;
  }
  

  if (values['site_url'] == null || values['site_url'] == "") {
    last_nameError = "Please Enter Site Url";
    error_list.push(last_nameError);
    submit = false;
  }
   

  if (values['description'] == null || values['description'] == "") {
    emailError = "Please Enter Description";
    error_list.push(emailError);
    submit = false;
  }


  if (values['tags'] == null || values['tags'] == "") {
    repeat_emailError = "Please Enter Tags";
    error_list.push(repeat_emailError);
    submit = false;
  }


  if (values['youtube'] == null || values['youtube'] == "") {
    passwordError = "Please Enter Youtube link";
    error_list.push(passwordError);
    submit = false;
  }
  if (values['facebook'] == null || values['facebook'] == "") {
    confirm_passwordError = "Please Enter Facebook link";
    error_list.push(confirm_passwordError);
    submit = false;
  }
 
  if (values['google'] == null || values['google'] == "") {
    confirm_passwordError = "Please Enter Google link";
    error_list.push(confirm_passwordError);
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
})


// company

//   if (input.files && input.files[0]) {
//     var reader = new FileReader();
//     reader.onload = function(e) {
//       $('#preview').attr('src', e.target.result);
//     }
    
//     reader.readAsDataURL(input.files[0]);
//   }
// }
// $("#logo-img").on('change',function() {
//   var image = $(this);
//   let img = new Image();
//   img.src = window.URL.createObjectURL(event.target.files[0])
//   img.onload = () => {
//   if (img.height > 160 || img.width > 160){
//     alert('Invalid Image');
//     $(this).val("");
//   }
//   else{
//     image.closest('.form-group').find('.add-img').html('');
//     image.closest('.form-group').find('.add-img').append(`<img class="cb-log" src="${img.src}" alt="logo-img">`)
//   }
//   }
// });

$('.save').on("click", function() {

var values = {};

var error_list  =[];
var submit = true;

var company_name = $('input[name="company_name"]').val();
if (company_name == null || company_name == "") {
    typesError = "Please Enter Company Name.";
    error_list.push(typesError);
    submit = false;
  }
var address = $('input[name="address"]').val();
if (address == null || address == "") {
    addError = "Please Enter Address.";
    error_list.push(addError);
    submit = false;
  }
var city = $('input[name="city"]').val();
if (city == null || city == "") {
    addError = "Please Enter City.";
    error_list.push(addError);
    submit = false;
  }
  var state = $('input[name="state"]').val();
if (state == null || state == "") {
    addError = "Please Enter State.";
    error_list.push(addError);
    submit = false;
  }

var zip = $('input[name="zip"]').val();
if (zip == null || zip == "") {
    addError = "Please Enter Zip Code.";
    error_list.push(addError);
    submit = false;
  }
  var phone = $('input[name="phone"]').val();
if (phone == null || phone == "") {
    addError = "Please Enter Telephone Number.";
    error_list.push(addError);
    submit = false;
  }
var email = $('input[name="email"]').val();
if (email == null || email == "") {
    addError = "Please Enter Email.";
    error_list.push(addError);
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
