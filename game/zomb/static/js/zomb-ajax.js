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