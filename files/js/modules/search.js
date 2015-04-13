$("#search_books").on("click", function() {
	search_text = $("#search_text").val();
	if (!search_text) {
		msgbox("Please enter some text to search", null);
	}
	else {
		$.ajax({
			type: "GET",
			url: "/search_books",
			data: {
				"search_text": search_text, 
				"by_name": $('#by_name').is(":checked"), 
				"by_author": $('#by_author').is(":checked"), 
				"by_publisher": $('#by_publisher').is(":checked")
			},
			dataType: "json",
			success: function(r) {
				var row = "";
				if (r[0]) {
					// if table is not there then first prepare table
					if (!$("#result_table").html()) {
						$("#result_area").empty();
						$("#result_area").append('<table class="table table-bordered table-hover" name="result_table" id="result_table">\
							<thead>\
								<tr class="active">\
									<th>Book ID</th>\
									<th>Book Name</th>\
									<th>Edition</th>\
									<th>Author</th>\
									<th>Publisher</th>\
									<th>Rate</th>\
								</tr>\
							</thead>\
							<tbody></tbody>\
						</table>');
					}
					$("#result_table tbody").html("");

					// create rows for individual books
					$.each(r, function(i, book) {
						row += '<tr>\
									<td><a href="/book/' + book.id + '">' + book.id + '</a></td>\
									<td>' + book.book_name + '</td>\
									<td>' + book.edition + '</td>\
									<td>' + book.author + '</td>\
									<td>' + book.publisher + '</td>\
									<td>' + book.rate + '</td>\
								</tr>';
					});

					$("#result_table tbody").append(row);
				}
				else {
					no_result = '<div class="well text-center">\
							<h4><i class="fa fa-info-circle"></i> Oops! No results found for "' + search_text + '"</h4>\
						</div>';

					$("#result_area").empty();
					$("#result_area").append(no_result);
				}
			}
		});
	}
});