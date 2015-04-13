var book_form = '<form name="book_shelf" id="book_shelf" action="/book/new" method="POST" enctype="multipart/form-data">\
					<div class="form-group">\
						<label class="control-label">Upload Cover Photo</label>\
						<input type="file" class="form-control" name="book_cover_photo" data-name="book_cover_photo" data-mandatory="yes" id="book_cover_photo">\
					</div>\
					<div class="form-group">\
						<label class="control-label">Upload Book</label>\
						<input type="file" class="form-control" name="ebook" data-name="ebook" data-mandatory="yes" id="ebook">\
					</div>\
					<div class="form-group">\
						<label class="control-label">Book Name</label>\
						<input type ="text" class="form-control" name="book_name" autocomplete="on" data-name="book_name" data-mandatory="yes">\
					</div>\
					<div class="form-group">\
						<label class="control-label">Author</label>\
						<input type="text" class="form-control" name="author" autocomplete="on" data-name="author" data-mandatory="no">\
					</div>\
					<div class="form-group">\
						<label class="control-label">Publisher</label>\
						<input type="text" class="form-control" name="publisher" autocomplete="on" data-name="publisher" data-mandatory="no">\
					</div>\
					<div class="form-group">\
						<label class="control-label">Edition</label>\
						<input type="text" class="form-control" name="edition" autocomplete="on" data-name="edition" data-mandatory="no">\
					</div>\
					<div class="form-group">\
						<label class="control-label">Rate</label>\
						<input type="text" class="form-control" name="rate" autocomplete="off" data-name="rate" data-mandatory="no">\
					</div>\
					<div class="form-group">\
						<label class="control-label">Favorite</label>\
						<select class="form-control" name="favorite">\
							<option>Yes</option>\
							<option>No</option>\
						</select>\
					</div>\
					<div class="form-group">\
						<label class="control-label">More Details</label>\
						<textarea class="form-control" name="more_details" rows="5" autocomplete="off" data-name="more_details" data-mandatory="no"></textarea>\
					</div>\
					<div class="form-group">\
						<button type="submit" class="btn btn-primary">Save</button>\
					</div>\
				</form>';

// show dialog box for adding book
$("#add-book").on("click", function() {
	msgbox(book_form, '<i class="fa fa-book"></i> Add Book');
});


// show books matching with book name
$("#search_books").on("click", function() {
	search_text = $("#search_text").val();
	if (!search_text) {
		msgbox("Please enter some text to search", null);
	}
	else {
		$.ajax({
			type: "GET",
			url: "/search_book_name",
			data: { "search_text": search_text },
			dataType: "json",
			success: function(r) {
				$("#bookshelf_slider #panel_slider").empty();
				$("#bookshelf_slider #panel_slider").append(r);
			}
		});
	}
});


// refresh books
$("#refresh_books").on("click", function() {
	$("#search_text").val("");
	$.ajax({
		type: "GET",
		url: "/refresh_books",
		dataType: "json",
		success: function(r) {
			$("#bookshelf_slider #panel_slider").empty();
			$("#bookshelf_slider #panel_slider").append(r);
		}
	});
});


// Check All
$("#check_all").on("click", function() {
	// uncheck all checkboxes if all are checked
	if ($('input[data-name="book"]').length == $('input[data-name="book"]:checked').length) {
		$('input[data-name="book"]').each(function() {
			this.checked = false;
		});
	}
	else {
		// check all boxes
		$('input[data-name="book"]').each(function() {
			this.checked = true;
		});
	}
});


// Delete
$("#delete").on("click", function() {
	var title = '<i class="fa fa-times-circle"> Delete</i>';

	if (!$('input[data-name="book"]:checked').length) {
		msgbox("Please select any book(s) to delete", title);
	}
	else {
		$('input[data-name="book"]:checked').each(function() {
			msg_body = '<div>Are you sure you want to delete these book(s) permanently?</div>\
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
				$('input[data-name="book"]:checked').each(function() {
					ids.push($(this).attr("data-id"));
				});

				$('#message-box').modal('hide');

				$.ajax({
					type: "POST",
					url: "/delete",
					data: { "module": "Book", "ids": JSON.stringify(ids) },
					dataType: "json",
					success: function(r) {
						$("#refresh_books").trigger("click");
					}
				});
			});
		});
	}
});


// make files downloadable
$("#download").on("click", function() {
	var selected_checkbox = $('input[data-name="book"]:checked').length;
	
	if (!selected_checkbox) {
		msgbox("Please select any book(s) to download")
	}
	else if (selected_checkbox > 1) {
		msgbox("You cannot download multiple eBooks at a time")
	}
	else {
		$.ajax({
			type: "GET",
			url: "/get_book_path",
			data: { "book_id": $('input[data-name="book"]:checked').attr("data-id") },
			dataType: "json",
			success: function(book_path) {
				window.location = book_path;
			}
		});
	}
});


// make files sharable
$("#share").on("click", function() {
	var selected_checkbox = $('input[data-name="book"]:checked').length;
	
	if (!selected_checkbox) {
		msgbox("Please select any book(s) to share")
	}
	else {
		$.ajax({
			type: "GET",
			url: "/get_users",
			data: { "book_id": $('input[data-name="book"]:checked').attr("data-id") },
			dataType: "json",
			success: function(data) {
				var users = "";

				// prepare list of users for dialog box
				$.each(data, function(index, value) {
					users += '<div class="container">\
							<div class="row">\
								<div class="col-md-12">\
									<div class="checkbox">\
										<label class="control-label">\
											<input type="checkbox" name="user" data-name="user" id="user" data-user="' + value.id + '">' + value.id + '\
										</label>\
									</div>\
								</div>\
							</div>\
						</div>';
				});

				body_title = '<h4>Share with :</h4>';
				body_bottom = '<br><a href="/share" class="btn btn-primary" id="share_books">Share</a>';

				msgbox(body_title + users + body_bottom, '<i class="fa fa-share"></i> Share');
			}
		});
	}
});


// share files with user
$("#share_books").on("click", function() {
	var books = [];
	var users = [];
	
	$('input[data-name="book"]:checked').each(function() {
		books.push($(this).attr("data-id"));
	});

	$('input[data-name="user"]:checked').each(function() {
		users.push($(this).attr("data-user"));
	});

	console.log(books);
	console.log(users);

	if (books && users) {
		$.ajax({
			type: "POST",
			url: "/share",
			data: { "books": JSON.stringify(books), "users": JSON.stringify(users) },
			dataType: "json",
			success: function(r) {
				$("#refresh_books").trigger("click");
			}
		});
	}
});