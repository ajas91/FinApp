function removeRow(r) {
    var i = r.parentNode.parentNode.parentNode.rowIndex;
	document.getElementById("myTable").deleteRow(i);
}
