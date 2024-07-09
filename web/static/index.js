

// === On DOM ready ===
$(document).ready(function() {
    // setLoadingState(false)
    
    // Register `onFormSubmit` event
    $("#filterForm").submit(function () { onFormSubmit(); return false })

    // Load



})


// ========================
// === Document actions ===
// ========================
function onFormSubmit() {

}

function setLoadingState(state) {
    if (state) {
        $("#search-results-spinner").show()
        $("#search-results").hide()
    }
    else{
        $("#search-results-spinner").hide()
        $("#search-results").show()
    }
}


// =====================
// === Backend comms ===
// =====================
