

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

function cardExpandAdditionalInfo(x){
    // I know it looks stupid but i gotta do it cause it could be undefined
    let card = $(x)
    hasExpanded = card.data("hasExpanded") == true 
    card.data("hasExpanded", !hasExpanded)
    
    // Flip icon
    card.find("svg.arrow-icon").css({
        "transform": "rotate(" + !hasExpanded * 180 + "deg)" + (!hasExpanded ? " translateY(-0.125rem)" : "")
    })

    // Show rows
    let table = $(card.parents()[3])
    table.find("tbody#additional-info > tr").each(function (i) {
        $(this).toggle()
    })

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
