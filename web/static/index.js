

// === On DOM ready ===
$(document).ready(function() {
    // Register `onFormSubmit` event
    $("#filter-form").submit(function () { onFormSubmit(this); return false })

    // Load
    api_loadAll()


})


// ========================
// === Document actions ===
// ========================
function onFormSubmit(form) {
    let data = jsonArrayToDict($(form).serializeArray())
    api_searchHPCs(data)
}

function toggleModal(x, mode='toggle'){
    parentCard = $(x).parents("div.result-card")
    parentCard.find("div.result-card-modal").modal(mode)

    // I know it looks stupid but i gotta do it cause it could be undefined
    loadedNodeDetails = parentCard.data("loadedNodeDetails") == true
    if (!loadedNodeDetails && parentCard.find("div#node-details").length) {
        api_loadNodeDetails(x)
        parentCard.data("loadedNodeDetails", true) 
    }

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
                $(this).remove()
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

function doubleRangeFirst(slider, max100){  
    slider.style.setProperty('--start', (slider.value/max100) + '%')
    $(slider).parents().eq(1).find("span").eq(0).text(numberWithCommas(slider.value))
}

function doubleRangeSecond(slider, max100){
    slider.previousElementSibling.style.setProperty('--stop', (slider.value/max100) + '%')
    $(slider).parents().eq(1).find("span").eq(1).text(numberWithCommas(slider.value))
}


// ========================
// === Helper functions ===
// ========================
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function jsonArrayToDict(x) {
    res = {}
    x.forEach((item) => res[item.name] = item.value )
    return res
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
            // console.log(data.length)
            // console.log(data.start_range)
            $("div#search-results").append(data.html)
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

function api_loadNodeDetails(caller) {
    parentCard = $(caller).parents("div.result-card")
    systemId = parentCard.data("system-id")
    nodeDetails = parentCard.find("div#node-details")
    skeletonCard = nodeDetails.find("div.node-detail-card")
    internalErr = parentCard.find("div#internal-error")

    $.ajax({
        type: "GET",
        url: "api/hpcs/node_details/" + systemId,
        success: function(data, status) {
            skeletonCard.hide()
            nodeDetails.append(data)
        },
        error: function(req, textStatus, errorThrown) {
            console.log(req.responseText);
            skeletonCard.hide()
            internalErr.show()
        },
    });
}

function api_searchHPCs(data){
    data["limit"] = 10
    data["offset"] = 0
    setLoadingState(true)
    $.ajax({
        type: "POST",
        url: "api/hpcs/filter",
        data: JSON.stringify(data),
        success: function(res, status) {
            console.log("Got " + res.length + " results.")
            // console.log(res.start_range)
            $("div#search-results").append(res.html)
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