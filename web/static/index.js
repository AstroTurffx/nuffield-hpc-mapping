

// === On DOM ready ===
$(document).ready(function() {
    // Register `onFormSubmit` event
    $("#filterForm").submit(function () { onFormSubmit(); return false })

    // Load
    api_loadAll()


})


// ========================
// === Document actions ===
// ========================
function onFormSubmit() {

}

function cardExpandAdditionalInfo(x){
    let card = $(x)
    // I know it looks stupid but i gotta do it cause it could be undefined
    hasExpanded = card.data("hasExpanded") == true 
    card.data("hasExpanded", !hasExpanded)
    
    // Flip icon
    card.find("svg.arrow-icon").css({
        "transform": "rotate(" + !hasExpanded * 180 + "deg)" + (!hasExpanded ? " translateY(-0.125rem)" : "")
    })

    // Show rows
    let table = $(card.parents()[3])
    table.find("tbody#additional-info").toggle()
    // table.find("tbody#additional-info > tr").each(function (i) {
    //     $(this).toggle()
    // })

}

function setLoadingState(state) {
    let skeletonCard = $("div#skeleton-card")
    let cards = $("div#search-results > div.result-card")

    if (state) {
        $("div#internal-error").hide()
        skeletonCard.show()
        cards.each(function(i) {
            if ( !$(this).is(skeletonCard) )
                $(this).hide()
        })
    }
    else { 
        skeletonCard.hide()
        cards.each(function(i) {
            if ( !$(this).is(skeletonCard) )
                $(this).show()
        })
    }
}



// =====================
// === Backend comms ===
// =====================
function api_loadAll() {
    setLoadingState(true)
    $.ajax({
        type: "POST",
        url: "api/hpcs/all",
        data: JSON.stringify({
            "limit": 10,
            "offset": 0
        }),
        success: function(data, status) {
            $("div#search-results").append(data)
            setLoadingState(false)
        },
        error: function(req, textStatus, errorThrown) {
            setLoadingState(false)
            console.warn(req.responseText)
            $("div#internal-error").toggle()
        },
        contentType: "application/json; charset=utf-8"
    });
}
