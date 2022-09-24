function doDelete(msg)
{
    var ans = confirm(msg);
    if(!ans)
        event.preventDefault();
}

function search(myInput , myTable) {

    console.log(myInput);
    console.log(myTable);
    // Declare variables 
    var input ,  filter, table, tr, td, i;
    input = document.getElementById(myInput);
    filter = input.value.toUpperCase();
    table = document.getElementById(myTable);
    tr = table.getElementsByTagName("tr");
    var input_text = document.getElementById(myInput).value;
    var digit = /\d/;
    var text = /[A-z]/

    if(digit.exec(input_text) > 0){
        for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
          if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        } 
      }
    }else{
      // Loop through all table rows, and hide those who don't match the search query
      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2];
        if (td) {
          if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        } 
      }

      
    }
}
