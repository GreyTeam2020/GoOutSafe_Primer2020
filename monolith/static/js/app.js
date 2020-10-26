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
});
