$(function () {
    $(".checkall-checkbox").on("click", function () {
        if ($(this).prop("checked")) {
            $(".data-table tr").addClass("selected");
        } else {
            $(".data-table tr").removeClass("selected");
        }
    });

    $(".data-table__row").on("click", function (event) {
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
        } else {
            $(this).addClass("selected");
        }
    });
});

function runListAction(event, url) {
    event.stopPropagation();
    event.preventDefault();
    if (confirm("Really?")) {
        var batch_ids = [];
        $(".data-table__row.selected").each(function () {
            batch_ids.push($(this).attr("data-id"));
        });
        $.ajax({
            url: url + "/" + $(event.target).val(),
            data: {
                ids: batch_ids.join(",")
            },
            dataType: "json"
        }).done(function (data) {
            if (data.remove_rows) {
                $(".data-table__row.selected").fadeOut();
            }
            $(event.target).val("");
        }).fail(function () {
            alert("Something went wrong");
        });
    }
}

function removeRow(event, url) {
    event.stopPropagation();
    event.preventDefault();
    if (confirm("Really?")) {
        $.ajax({
            url: url,
            dataType: "text"
        }).done(function () {
            console.debug("DONE");
            $(event.target).parents("tr").fadeOut();
        }).fail(function () {
            alert("Something went wrong");
        });
    }
}