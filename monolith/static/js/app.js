//document ready routine
$(document).ready(function() {
    if ($("#myreservation").length){
        $('#myreservation').DataTable();
    }
    if ($("#allrestaurants").length){
        $('#allrestaurants').DataTable();
    }
    if ($("#mymenu").length){
        $('#mymenu').DataTable();
        $("#submitDish").click(() => {$("#addDishForm").submit();});
    }
    if ($("#myreservations").length){
        $('#myreservations').DataTable();
    }
    if ($("#mytables").length){
        $('#mytables').DataTable();
        $("#submitTable").click(() => {$("#addTableForm").submit();});
    }

    if($("#reservation_date").length) {
        $('#reservation_date').datetimepicker({
            inline: true,
            format: 'd/m/Y H:m'
        });
        $("#newBook").click(function () {
            $("#bookTableForm").submit();
        });
        $(".showBooking").click(function () {
            $("#restaurant_id").val($(this).data("id"));
            $("#bookTable").modal("show");
        });
    }

    let ratingItems = $(".ratingStats");
    if (ratingItems.length){
        ratingItems.each(function(index, e){
            let rating = parseFloat($(e).data("rating"));
			$(e).html("")
            for (let i=1; i<6; i++){
                if (rating >= 1){
                    $(e).append("<span class=\"material-icons\"> star </span>");
                } else if (rating > 0.5){
                    console.log(rating);
                    $(e).append("<span class=\"material-icons\"> star_half </span>");
                } else {
                    $(e).append("<span class=\"material-icons\"> star_border </span>");
                }
                rating--;
            }
        })
    }

    var switchView = $("#switchView");
    if (switchView.length){
        console.log("ci sono")
        switchView.click(function(){
            var cards = $("#card-view");
            var mapview = $("#map-view");
            if (mapview.is(":hidden")){
                cards.hide();
                mapview.show();
                map.invalidateSize()
                map.fitBounds(group.getBounds());
                switchView.html("Switch to Cards View");
            } else {
                mapview.hide();
                cards.show();
                switchView.html("Switch to Map View");
            }
        });
    }


    $('.deleteBooking').on('click', function(e) {
        e.preventDefault();
        $('#confirm').modal({
            backdrop: 'static',
            keyboard: false
        }).on('click', '#deleteReservation', function(e) {

        });
    });



});
