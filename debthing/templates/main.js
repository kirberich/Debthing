$(function() {
	$("body").on("change", ".update", function() {
		var $this = $(this),
			$updatable = $this.parents(".updatable").first(),
			url = $updatable.data("url"),
			$inputs = $updatable.find("input,select");

		if(!url) {
			url = $updatable.attr("action");
		}

		data = $inputs.serialize();
		$.post(url, data, function(data, textStatus, jqXHR){
			$this.trigger("saved", [data]);
		});
	});

	$("body").on("saved", "#expense-form", function(e, data) {
		var response = jQuery.parseJSON(data);
		$("#title").html(response['expense_description']);
	});

	$(".chosen-select").chosen();

	$("#bulk-select").change(function(){
		debugger;
	});
});