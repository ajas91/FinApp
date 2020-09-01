// function paginateTable(table, way, max){
//     max? paginateTable.max[table] = max : max = paginateTable.max[table];
//     way = way == 1? 1 : way == -1? 0 : -1;
//     var r = document.getElementById(table).rows, i = 0;
//     var row_1 = r[0]
//
//     for(i; i < r.length; ++i){ // find current start point
//         if(r[i].style.display != 'none'){
//             break;
//         };
//     };
//
//     for(i; i < r.length; ++i){ // continue on to find current end point
//         if(r[i].style.display == 'none'){
//             paginateTable.endPoint[table] = i;
//             break;
//         };
//         paginateTable.endPoint[table] = 0; // if no end point found, table is 'virgin' or at end
//     };
//
//     if(way == 1 && r[r.length - 1].style.display != 'none') return; // table was already at the end and we tried to move forward
//     // if moving forward, start will be old end, else start will be old start - max or 0, whichever is greater:
//     paginateTable.startPoint[table] = way? paginateTable.endPoint[table] : Math.max( 0, paginateTable.startPoint[table] - max);
//     paginateTable.endPoint[table] = paginateTable.startPoint[table] + --max; // new end will be new start + max - 1
//     for (i = r.length - 1; i > -1; --i) // set display of rows based upon whether or not they are in range of the calculated start/end points
//     r[i].style.display = i < paginateTable.startPoint[table] || i > paginateTable.endPoint[table]? 'none' : '';
// };
//
// paginateTable.startPoint = {};
// paginateTable.endPoint = {};
// paginateTable.max = {};
//
// if(window.addEventListener)
// window.addEventListener('load', paginateTable.init, false);
// else if (window.attachEvent)
// window.attachEvent('onload', paginateTable.init);
//
//
// // you can init as many tables as you like in here by id: paginateTable('id', 0, num_max_rows);
// paginateTable.init = function(){ // remove any not used
//     paginateTable('test_table', 0, 10);
// };
//
// //////////////// End Paginate Table Script ///////////////

// If *table* defines <thead> then this function replaces the table with N
// tables separated by a page break. Each new table starts with <thead> and its
// height is at most maxHeight pixels.
//
// *table* must not have the id attribute since it is cloned N-times. Use the
// class attribute instead.
//
// function splitTable(table, maxHeight) {
//     var header = table.children("thead");
//     if (!header.length)
//         return;
//
//     var headerHeight = header.outerHeight();
//     var header = header.detach();
//
//     var splitIndices = [0];
//     var rows = table.children("tbody").children();
//
//     maxHeight -= headerHeight;
//     var currHeight = 0;
//     rows.each(function(i, row) {
//         currHeight += $(rows[i]).outerHeight();
//         if (currHeight > maxHeight) {
//             splitIndices.push(i);
//             currHeight = $(rows[i]).outerHeight();
//         }
//     });
//     splitIndices.push(undefined);
//
//     table = table.replaceWith('<div id="_split_table_wrapper"></div>');
//     table.empty();
//
//     for(var i=0; i<splitIndices.length-1; i++) {
//         var newTable = table.clone();
//         header.clone().appendTo(newTable);
//         $('<tbody />').appendTo(newTable);
//         rows.slice(splitIndices[i], splitIndices[i+1]).appendTo(newTable.children('tbody'));
//         newTable.appendTo("#_split_table_wrapper");
//         if (splitIndices[i+1] !== undefined) {
//             $('<div style="page-break-after: always; margin:0; padding:0; border: none;"></div>').appendTo("#_split_table_wrapper");
//         }
//     }
// }
//
// $(function() { splitTable($(".test_table"), 300); });

// Basic example
$(document).ready(function () {
  $('#dtBasicExample').DataTable({
    "pagingType": "numbers" // "simple" option for 'Previous' and 'Next' buttons only
  });
  $('.dataTables_length').addClass('bs-select');
});
