var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

$(document).ready(function() {
    $("abbr.timeago").timeago();
});

function showTooltip(x, y, contents) {
    $("#tooltip").remove();
    
    $('<div id="tooltip">' + contents + '</div>').css( {
        position: 'absolute',
        display: 'none',
        top: y + 5,
        left: x + 5,
        border: '1px solid #ccc',
        padding: '5px',
        'background-color': '#7CA0C7',
        'color': '#fff',
        opacity: 0.80
    }).appendTo("body").fadeIn(200);
}

var previousPoint = null;
var date = new Date();

var DAYS_PERIOD = null;

function trafficGraph(placeholder, data, days=null) {
    var plot = $.plot(placeholder, data, {xaxis:{mode:'time'}, points:{show:true}, lines:{show:true}, grid:{hoverable:true}});
    DAYS_PERIOD = days
    
    placeholder.bind("plothover", function (event, pos, item) {
        if (item) {
            if (previousPoint != item.datapoint) {
                previousPoint = item.datapoint;
                
                date.setTime(item.datapoint[0]).toString;
                if(DAYS_PERIOD==365)
                    showTooltip(item.pageX, item.pageY, item.series.label + ' on ' + monthNames[date.getMonth()] + ' is ' + item.datapoint[1]);
                else
                    showTooltip(item.pageX, item.pageY, item.series.label + ' on ' + monthNames[date.getMonth()] + ' ' + date.getDate() + ' is ' + item.datapoint[1]);
            }
        } else {
            $("#tooltip").remove();
            previousPoint = null;
        }
    });
}
