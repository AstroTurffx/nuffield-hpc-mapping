

// === On DOM ready ===
$(document).ready(function() {
    // Register `onFormSubmit` event
    $("#filter-form").submit(function () { onFormSubmit(this); return false })

    // Enable map pin tooltips
    $("div#map-container").tooltip({
        selector: "[data-bs-toggle='tooltip']",
        container: 'div#map-container'
    })

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
    let cards = $("div#search-results > div.result-card:not(#skeleton-card)")
    let pins = $("#map-container > .map-pin")

    if (state) {
        $("div#internal-error").hide()
        $("#reset-filters").hide()
        skeletonCard.show()
        cards.remove()
        pins.remove()
    }
    else {
        skeletonCard.hide()
        cards.show()
        pins.show()
    }
}

function setHPCs(data) {
    $("div#search-results").append(data.html)
    $("div#search-results > .result-card")
    .on("mouseenter mouseleave", function() {
        system_id = $(this).data("system-id");
        pin = $(`.map-pin[data-system-id=${system_id}]`);
        pin.toggleClass("selected-pin");
    })

    $("div#map-container").append(data.pins)
    SVGInject($("div#map-container > img.map-pin")).then(() => {
        $("div#map-container > .map-pin").on("mouseenter mouseleave", function() {
            system_id = $(this).data("system-id")
            $(`.card[data-system-id=${system_id}]`).toggleClass("selected-card")
        })
    })

    setLoadingState(false)
}

function doubleRangeFirst(slider, max100){  
    slider.style.setProperty('--start', (slider.value/max100) + '%')
    $(slider).parents().eq(1).find("span").eq(0).text(numberWithCommas(slider.value))
}

function doubleRangeSecond(slider, max100){
    slider.previousElementSibling.style.setProperty('--stop', (slider.value/max100) + '%')
    $(slider).parents().eq(1).find("span").eq(1).text(numberWithCommas(slider.value))
}

function resetFilters(){
    // Reset form
    $("form#filter-form")[0].reset()

    // Reset double ranges
    let s = $(".double-range > input").each(function() {
        let els = $(this).get(0).style
        els.setProperty("--start", "0%")
        els.setProperty("--stop", "100%")

        let value = $(this).attr("value")
        let i = $(this).index()
        $(this).parents().eq(1).find("span").eq(i).text(numberWithCommas(value))
    })

    api_loadAll()
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
            setHPCs(data)
        },
        error: function(req, textStatus, errorThrown) {
            setLoadingState(false)
            console.warn(req.responseText)
            $("div#internal-error").toggle()
        },
        contentType: "application/json; charset=utf-8"
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
            setHPCs(res)
            $("#reset-filters").show()
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

const MAP_BOUNDS_LAT_1 = 60.846142;
const MAP_BOUNDS_LAT_2 = 49.162600;
const MAP_BOUNDS_LNG_1 = -10.476361;
const MAP_BOUNDS_LNG_2 = 1.765083;
const MERC_Y = (lat) => Math.log(Math.tan(lat/2 + Math.PI/4))
function coordsToPosition(lat,lng){
    deg2rad = Math.PI/180
    rlat = lat * deg2rad
    ymax = MERC_Y(MAP_BOUNDS_LAT_1 * deg2rad)
    ymin = MERC_Y(MAP_BOUNDS_LAT_2 * deg2rad)
    t = 100.0 * (ymax - MERC_Y(rlat)) / (ymax - ymin)

    // I think linear projection should be fine right?
    l = 100.0 * (lng-MAP_BOUNDS_LNG_1) / (MAP_BOUNDS_LNG_2-MAP_BOUNDS_LNG_1);
    return `top: ${t}%; left: ${l}%;`    
}