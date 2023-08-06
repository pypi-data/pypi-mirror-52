$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('.bucket-content').on({
        click: function() {
            var attr = $(this).attr("project");
            $('div[project="' + attr + '"]').each(function (index, element) {
                $(this).toggleClass("bucket-content-highlight");
            });
        },
    });
    $('input[type=checkbox].user-toggle').each(function () {
        this.checked = true;
    });
    $('input[type=checkbox].user-toggle').on("click", function () {
        console.debug($(this).val() + ": " + this.checked);
        var state = this.checked;
        $('.' + $(this).val()).each(function (index, element) {
            if (state === true) {
                $(element).show();
            } else {
                $(element).hide();
            }
        });
    });
    $('input[type=checkbox].all-user-toggle').on("click", function () {
        var state = this.checked;
        $('.user-toggle').each(function (index, element) {
            this.checked = state;
        });
        $('.user-bucket').each(function (index, element) {
            if (state === true) {
                $(element).show();
            } else {
                $(element).hide();
            }
        });
    });
});
