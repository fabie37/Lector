// This just has the functionality for the stars
$(function () {
    $(".fa-star").mouseover(function () {
        var value = $(this).attr('value');
        var rating_id = $(this).attr('id');
        for (i = 5; i > 0; i--) {

            $("i[id=" + rating_id + "][value=" + i + "]").removeClass("fas");
            $("i[id=" + rating_id + "][value=" + i + "]").addClass("far");
        }
        for (i = value; i > 0; i--) {
            $("i[id=" + rating_id + "][value=" + i + "]").removeClass("far");
            $("i[id=" + rating_id + "][value=" + i + "]").addClass("fas");
        }
    }).mouseout(function () {
        var value = $(this).attr('value');
        var rating_id = $(this).attr('id');
        console.log(rating_id);
        for (i = 5; i > 0; i--) {
            if ($("i[id=" + rating_id + "][value=" + i + "]").attr("data-id") == "checked") {
                $("i[id=" + rating_id + "][value=" + i + "]").removeClass("far");
                $("i[id=" + rating_id + "][value=" + i + "]").addClass("fas");
            }
        }
        for (i = value; i > 0; i--) {
            if ($("i[id=" + rating_id + "][value=" + i + "]").attr("data-id") != "checked") {
                $("i[id=" + rating_id + "][value=" + i + "]").removeClass("fas");
                $("i[id=" + rating_id + "][value=" + i + "]").addClass("far");
            }
        }
    }).click(function () {
        var value = $(this).attr('value');
        var rating_id = $(this).attr('id');
        for (i = 5; i > 0; i--) {
            $("i[id=" + rating_id + "][value=" + i + "]").attr("data-id", "unchecked");
        }
        for (i = value; i > 0; i--) {
            $("i[id=" + rating_id + "][value=" + i + "]").attr("data-id", "checked");
            $("i[id=" + rating_id + "][value=" + i + "]").removeClass("far");
            $("i[id=" + rating_id + "][value=" + i + "]").addClass("fas");
        }


        // Add ajax here

    });
});