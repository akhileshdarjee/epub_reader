$("#registration").submit(function( event ) {
	var first_name = document.registration.first_name.value;
	var last_name = document.registration.last_name.value;
	var email = document.registration.email.value;
	var password = document.registration.password.value;
	var confirm_password = document.registration.confirm_password.value;
	var date_of_birth = document.registration.dob.value;

	var mandatory = ["first_name", "email", "password", "confirm_password", "date_of_birth"];

	for (x=0; x<=mandatory.length-1; x++) {
		if (!eval(mandatory[x])) {
			msg = "Please Enter " + mandatory[x].replace("_", " ").toProperCase();
			msgbox(msg);
			break;
		}
	}

	if (password != confirm_password)
		msgbox("Passwords does not match");
});