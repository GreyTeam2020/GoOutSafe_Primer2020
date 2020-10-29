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
    if ($("#submitReview").length){
        $("#submitReview").click(() => {$("#reviewForm").submit();});
    }

    if($("#reservation_date").length) {
        $('#reservation_date').datetimepicker({
            inline: true,
            format: 'd/m/Y H:i'
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

    if ($("#registerRestaurantSubmit").length){
        $('#open_lunch').datetimepicker({
          datepicker:false,
          format:'H:i'
        });
        $('#close_lunch').datetimepicker({
          datepicker:false,
          format:'H:i'
        });
        $('#open_dinner').datetimepicker({
          datepicker:false,
          format:'H:i'
        });
        $('#close_dinner').datetimepicker({
          datepicker:false,
          format:'H:i'
        });
    }

    $("#searchSubmit").click(function(){
        let search = $("#searchbar").val();
        console.log(search)
        if (search){
            window.location = "/restaurant/search/"+search;
        } else {
            window.location = "/"
        }

    })

    $(".deleteBooking").click(deleteDialog);
    // $("#restaurantID").val($(this).data("id"));
    function deleteDialog() {
        Swal.fire({
          title: 'Do you want to save the changes?',
          showDenyButton: true,
          showCancelButton: true,
          confirmButtonText: `Save`,
          denyButtonText: `Don't save`,
        }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            Swal.fire('Saved!', '', 'success')
          } else if (result.isDenied) {
            Swal.fire('Changes are not saved', '', 'info')
          }
        })
    }

});
