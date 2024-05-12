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

document.addEventListener("DOMContentLoaded", function() {
    const submitButton = document.getElementById('submitButton');

    submitButton.addEventListener('click', function() {
        submitButton.style.display = 'none';

        const inputValue = currentSelectedCell;
        const trimmedInputValue = inputValue.textContent.trim();

        const csrftoken = getCookie('csrftoken');

        const xhr = new XMLHttpRequest();
        const url = '/fitness/schedule_workout'

        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Request successful');
            } else {
                console.error('Request failed');
            }
        };

        const data = JSON.stringify({ inputValue: trimmedInputValue });
        xhr.send(data);

    });
});

function handleCellClick(day, hour) {
    var dayString = String(day);

    var daysOfWeek = ['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var validDay = daysOfWeek[day];

    if (validDay) {
        var cellId = `${validDay.toLowerCase()}_${hour}`;
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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
