window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng, ctx) {
            const p = feature.properties;
            const color = p.source === "ep" ? "#3a0ca3" : "#4895ef";
            const marker = L.circleMarker(latlng, {
                radius: 5,
                color: color,
                fillColor: color,
                fillOpacity: 0.8,
                weight: 1
            });

            let html = '<b>' + (p.title || '') + '</b><br/>' +
                'Lat: ' + latlng.lat.toFixed(2) + ', Lon: ' + latlng.lng.toFixed(2) + '<br/>';
            if (p.source === 'ob') {
                html += 'Period: ' + (p.period || 'N/A') + '<br/>' +
                    'Elevation: ' + (p.elev || 'N/A') + ' m<br/>' +
                    'Time zone: GMT' + (p.tz || 'N/A') + '<br/>' +
                    '99% Heating DB: ' + (p.heat99 || 'N/A') + '<br/>' +
                    '1% Cooling DB: ' + (p.cool1 || 'N/A') + '<br/>' +
                    'Source: Climate.OneBuilding.Org';
            } else {
                html += 'Source: EnergyPlus';
            }
            marker.bindTooltip(html, {
                sticky: true,
                opacity: 0.9
            });
            return marker;
        }
    }
});