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

	$("body").on("click", ".delete", function(e) {
		e.preventDefault();
		var $this = $(this),
			$row = $this.parents("tr").first(),
			$updatable = $this.parents(".updatable").first(),
			url = $updatable.data("url");

		data = {'delete':true};
		$.post(url, data, function(data, textStatus, jqXHR){
			$row.remove();
		});
	});

	$("body").on("saved", function(e, data) {
		var response = jQuery.parseJSON(data);
		$("#title").html(response['expense_description']);

		if (response['type'] == 'item') {
			if(response['item_created']) {
				$("#expense-table").find("tr").last().replaceWith(response['item_form']);
				$("#expense-table").append(response['empty_form']);
			} else {
				$("#expense-table").find("[data-pk="+response['item_pk']+']').replaceWith(response['item_form']);
			}
			$(".chosen-select").chosen();
		} 

		$.get("/api/userbar", function(data, textStatus, jqXHR){
			$(".userbar").replaceWith(data);
		});
	});

	$(".chosen-select").chosen();

	$("#bulk-select").change(function(){
		var selectedSelects = $("input[name=bulk-assign]:checked").parents("tr").find("[name=users]"),
			toSelect = $(this).val();
		console.log(selectedSelects);
		selectedSelects.each(function() {
			var val = $(this).val(),
				valList = val === null ? [] : val;
			valList.push(toSelect);
			$(this).val(valList);
			$(this).change();
			$(this).trigger("chosen:updated");
			console.log(this);
		});
		$("#bulk-select").val(null);
		$("#bulk-select").trigger("chosen:updated");
	});

	$("#bulk-select-all-none").click(function(e){
		e.preventDefault();
		if($(this).text() == 'All') {
			$(this).text('None');
			$("input[name=bulk-assign]").prop("checked", true);
		} else {
			$(this).text('All');
			$("input[name=bulk-assign]").prop("checked", false);
		}
	})
});