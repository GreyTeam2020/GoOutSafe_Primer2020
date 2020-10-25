$("#newBook").click(function(){
    $("#bookTableForm").submit();
});
$("#showBooking").click(showBookRestaurant);

function showBookRestaurant(){
    $("#restaurantID").val($(this).data("id"));
    $("#bookTable").modal("show");
}