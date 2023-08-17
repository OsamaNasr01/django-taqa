
const total_e = document.getElementById('total_data').value
const total_data =JSON.parse(total_e) 

function total() {
    for (var id in total_data) {
        document.getElementById(id).innerText = total_data[id].toLocaleString ({minimumFractionDigits: 2})
    }
}
document.addEventListener("DOMContentLoaded", total())