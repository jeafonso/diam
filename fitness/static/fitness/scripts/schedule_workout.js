let currentSelectedCell = null;

document.addEventListener('DOMContentLoaded', function() {
    var table = document.getElementById('scheduleTable');
    if (table) {
        table.addEventListener('click', function(event) {
            var target = event.target;
            if (target.tagName === 'TD') {
                var day = target.cellIndex;
                var hour = target.parentElement.cells[0].innerHTML.split(':')[0];
                handleCellClick(day, hour);
            }
        });
    } else {
        console.error("Table element not found");
    }
});

document.addEventListener('DOMContentLoaded', function() {
    function hasSelectedCell() {
        return document.querySelector('.selected-cell') !== null;
    }

    function toggleSubmitButtonVisibility() {
        const submitButton = document.getElementById('submitButton');
        if (currentSelectedCell) {
            submitButton.style.display = 'block';
        } else {
            submitButton.style.display = 'none';
        }
    }

    const allCells = document.querySelectorAll('td');
    allCells.forEach(cell => {
        cell.addEventListener('click', function() {
            toggleSubmitButtonVisibility();
        });
    });
});

function handleCellClick(day, hour) {
    var dayString = String(day);

    var daysOfWeek = ['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var validDay = daysOfWeek[day];

    if (validDay) {
        var cellId = `${validDay.toLowerCase()}_${hour}`;
        console.log("cell ID = "+cellId);
        var cellElement = document.getElementById(cellId);

        if (cellElement) {

            if (currentSelectedCell) {
                currentSelectedCell.classList.remove('selected-cell');
            }

            cellElement.classList.add('selected-cell');
            currentSelectedCell = cellElement;
        } else {
            console.error("Cell element not found:", cellId);
        }

    } else {
        console.error("Invalid day index:", day);
    }
}
