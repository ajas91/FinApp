<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
</head>

var $target = $("#targetT");

$("#sourceT tr").each(function() {
var $tds = $(this).children(),
    $row = $("<tr></tr>");
    var i=1;
 while(i<3)
 {
  alert(i)  ;  $row.append($tds.eq(i).clone()).appendTo($target);
    i++;

 }
});
