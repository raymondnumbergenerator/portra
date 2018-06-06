function plot_points(points, channel) {
    var elem = document.getElementById('points-' + channel);
    for (var i = 0; i < points.length; i++) {
        elem.innerHTML += `<g id="${channel}-${i}"><circle class="tonecurve-point p-${channel}" cx="${points[i][0]}" cy="${points[i][1]}" r="3"></circle></g>`;
    }
}

function put_tooltips(points, channel) {
    var elem = document.getElementById('tc-' + channel + '-tooltip');
    for (var i = 0; i < points.length; i++) {
        elem.innerHTML += `<div class="mdl-tooltip tonecurve-tooltip" data-mdl-for="${channel}-${i}">${(points[i][0] / 255 * 100).toFixed(1)} / ${((255 - points[i][1]) / 255 * 100).toFixed(1)}%</div>`
    }
}

function fix_crushed_tc(points, channel) {
    var elem = document.getElementById('tc-crushed-' + channel);
    if (points[0][0] != 0) {
        elem.innerHTML += `<path class="tonecurve-curve curve-${channel}" d="M0 ${points[0][1]} ${points[0][0]} ${points[0][1]}"></path>`
    }
    if (points[points.length - 1][0] != 255) {
        elem.innerHTML += `<path class="tonecurve-curve curve-${channel}" d="M255 ${points[points.length - 1][1]} ${points[points.length - 1][0]} ${points[points.length - 1][1]}"></path>`
    }
}

function draw_histogram(points, channel) {
    var elem = document.getElementById('tc-hist-' + channel);
    var d = 'M0 255 ';
    for (var i = 0; i < points.length; i++) {
        d += `${i} ${points[i]} `;
    }
    d += '255 255';
    elem.setAttribute("d", d);
}
