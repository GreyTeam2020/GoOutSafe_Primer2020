$("#newBook").click(function(){
    $("#bookTableForm").submit();
});
$(".showBooking").click(showBookRestaurant);

function showBookRestaurant(){
    $("#restaurantID").val($(this).data("id"));
    $("#bookTable").modal("show");
}

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
});
