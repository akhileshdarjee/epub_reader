$("#book").submit(function( event ) {
	var book_id = document.book.book_id.value;
	var ebook = document.book.ebook.value;
	var book_cover = document.book.book_cover_photo.value;
	var book_name = document.book.book_name.value;
	var publisher = document.book.publisher.value;
	var author = document.book.author.value;
	var edition = document.book.edition.value;
	var rate = document.book.rate.value;
	var more_details = document.book.more_details.value;

	var mandatory = ["book_id", "book_name", "ebook", "book_cover"];

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