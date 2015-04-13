$("#profile").submit(function( event ) {
	var login_id = document.profile.login_id.value;
	var password = document.profile.password.value;
	var confirm_password = document.profile.confirm_password.value;

	var mandatory = ["login_id", "password", "confirm_password"];

	for (x=0; x<=mandatory.length-1; x++) {
		if (!eval(mandatory[x])) {
			event.preventDefault();
			msg = "Please Enter " + mandatory[x].replace("_", " ").toProperCase();
			$("#message-box").on("show.bs.modal", function (e) {
				$(".modal-body").html(msg);
			});
			$('#message-box').modal();
			break;
		}
	}
});