// convert string to proper case
String.prototype.toProperCase = function () {
	return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

// msgbox
function msgbox(msg, title) {
	$("#message-box").on("show.bs.modal", function (e) {
		$(".modal-title").html(title ? title : "Message");
		$(".modal-body").html(msg);
	});
	$('#message-box').modal();
}

// datepicker
$(function() {
	$("#datepicker").datepicker({
		inline: true,
		showOtherMonths: true,
		dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
	});
});

// issue submit form
var issue_form;
issue_form = "<form name='issue' id='issue' action='/shout' method='POST'>\
			<div class='form-group'>\
				<input type ='text' class='form-control' name='subject' placeholder='Subject' autocomplete='on' data-name='subject' data-mandatory='yes'>\
			</div>\
			<div class='form-group'>\
				<textarea type='text' class='form-control' name='description' placeholder='Description' autocomplete='on' data-name='description' rows='10' data-mandatory='no'></textarea>\
			</div>\
			<div class='form-group'>\
				<button type='submit' class='btn btn-primary'>Shout</button>\
			</div>\
		</form>";

$(".show-issue").on("click", function() {
	msgbox(issue_form, '<i class="fa fa-bug"></i> Report an Issue');
});

// about message 
var about_us;
about_us = "<p>Digital libraries will start gaining ground in India in the present \
				century. We are heading toward an environment in which digital \
				information may substitute for much print-based information. A library's\
				existence does not depend on the physical form of documents. Its mission\
				is to link the past and the present, and help shape the future by\
				preserving the records of human culture, as well as integrating\
				emerging information technologies. This mission is unlikely to change \
				in the near future.\
			</p>";

$(".show-about").on("click", function() {
	msgbox(about_us, '<i class="fa fa-info-circle"></i> About Us');
});

// -------------------------------------------------------------------------------------------------------
// action bar commands

// Refresh
$("#action-bar #refresh").on("click", function() {
	var current_module = document.cookie.split(";")[3].split("=")[1];

	$.ajax({
		type: "GET",
		url: "/refresh",
		data: { "module": current_module },
		dataType: "json",
		success: function(r) {
			var result = "";

			if (r[0]) {
				$.each(r, function(i, record) {
					result += '<div class="row records">\
						<div class="col-md-1">\
							<div class="checkbox">\
								<label class="control-label">\
									<input type="checkbox" name="check" data-name="check" data-id="' + record.id + '">\
								</label>\
							</div>\
						</div>\
						<div class="col-md-11">\
							<div class="form-group">\
								<label class="control-label">\
									<a href="' + current_module.toLowerCase() + '/' + record.id + '">' + record.id + '</a>\
								</label>\
							</div>\
						</div>\
					</div>';
				});
			}
			else {
				result = '<div class="well">\
					<h4>No ' + current_module + 's found</h4>\
					<hr>\
					<button class="btn btn-primary" id="new_record"> Make New ' + current_module + '</button>\
				</div>';
			}

			$(".records-list").empty();
			$(".records-list").append(result);
		}
	});
});

// New
$("#action-bar #new, #new_record").on("click", function() {
	window.location = "/" + document.cookie.split(";")[3].split("=")[1].toLowerCase() + "/new";
});

// Check All
$("#action-bar #check_all").on("click", function() {
	// uncheck all checkboxes if all are checked
	if ($('input[data-name="check"]').length == $('input[data-name="check"]:checked').length) {
		$('input[data-name="check"]').each(function() {
			this.checked = false;
		});
	}
	else {
		// check all boxes
		$('input[data-name="check"]').each(function() {
			this.checked = true;
		});
	}
});

// Delete
$("#action-bar #delete").on("click", function() {
	var title = '<i class="fa fa-times-circle"> Delete</i>';
	var current_module = document.cookie.split(";")[3].split("=")[1];

	if (!$('input[data-name="check"]:checked').length) {
		msgbox("Please select any record(s) to delete", title);
	}
	else {
		$('input[data-name="check"]:checked').each(function() {
			msg_body = '<div>Are you sure you want to delete these record(s) permanently?</div>\
				<div class="text-right">\
					<button class="btn btn-primary" id="delete-yes">Yes</button>\
					<button class="btn btn-default" id="delete-no">No</button>\
				</div>';

			msgbox(msg_body, title);

			$("#delete-no").on("click", function() {
				$('#message-box').modal('hide');
			});

			// delete the selected records permanently
			ids = [];
			$("#delete-yes").on("click", function() {
				$('input[data-name="check"]:checked').each(function() {
					ids.push($(this).attr("data-id"));
				});

				$('#message-box').modal('hide');

				$.ajax({
					type: "POST",
					url: "/delete",
					data: { "module": current_module, "ids": JSON.stringify(ids) },
					dataType: "json",
					success: function(r) {
						$("#action-bar #refresh").trigger("click");
					}
				});
			});
		});
	}
});

// -------------------------------------------------------------------------------------------------------