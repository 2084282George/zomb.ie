<<<<<<< HEAD
$(document).ready( function() {

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });
    
});

/*
$(document).ready( function() {
    
    $("#move-btn").click( function(event) {
        alert("You hit the move button");
        
        $.get('/rango/move_street/' function(data){
            
        });
        //do something
    });
    
});


    
    $("#enter-btn").click( function(event) {
        //do something
    });
   
    $("#wait-btn").click( function(event) {
        //do something
    });

    $("#search-btn").click( function(event) {
        //do something
    });

    $("#exit-btn").click( function(event) {
        //do something
    });

    $("#fight-btn").click( function(event) {
        //do something
    });

    $("#run-btn").click( function(event) {
        //do something
    });
    
}); */

=======
function do_move() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById(request).innerHTML = xhttp.responseText;
    }
  };
  xhttp.open("GET", "request.txt", true);
  xhttp.send();
}
>>>>>>> 716d89f7baad635312d03ee2c2910872989e8d2a
