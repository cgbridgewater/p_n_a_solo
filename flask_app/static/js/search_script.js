function searchUser() {
    let filter = document.getElementById('filter').value.toUpperCase();
    let userTable = document.getElementById('userTable');
    let tr = userTable.getElementsByTagName('tr');
    let found = false; // Flag to track if any results are found


    for (var i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName('td')[0];
        if (td) {
            let textvalue = td.textContent || td.innerHTML;
            if (textvalue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = '';
            found = true; // Set the flag to true if a result is found
            } else {
            tr[i].style.display = 'none';
            }
        }
    }
    
    if (!found) {
    // If no results are found, display "EMPTY"
        let emptyRow = document.createElement('tr');
        let emptyCell = document.createElement('td');
        emptyCell.setAttribute('colspan', tr[0].getElementsByTagName('td').length);
        emptyCell.textContent = 'No Results Found! Click "X" to reload';
        emptyRow.appendChild(emptyCell);
        userTable.innerHTML = '';
        userTable.appendChild(emptyRow);
    }
}