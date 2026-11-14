// Adds the CARTO vector basemap, drawn by MapLibre GL, to every Leaflet map
// whose container has the "carto-basemap" class (set via dl.Map(className=...)).
// MapLibre and its Leaflet plugin are only loaded once such a map is created.
// dash-leaflet's own "load" event fires before custom handlers are bound,
// so we use a Leaflet init hook instead.
(function () {
    const MAPLIBRE = "https://cdn.jsdelivr.net/npm/maplibre-gl@4.7.1/dist/maplibre-gl";
    const PLUGIN = "https://cdn.jsdelivr.net/npm/@maplibre/maplibre-gl-leaflet@0.0.22/leaflet-maplibre-gl.js";
    const STYLE = "/basemap/positron.json";
    const ATTRIBUTION =
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' +
        ' contributors &copy; <a href="https://carto.com/">CARTO</a>';
    let loading = null;

    function loadScript(src) {
        return new Promise(function (resolve, reject) {
            const script = document.createElement("script");
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    function loadMapLibre() {
        if (!loading) {
            const css = document.createElement("link");
            css.rel = "stylesheet";
            css.href = MAPLIBRE + ".css";
            document.head.appendChild(css);
            loading = loadScript(MAPLIBRE + ".js").then(function () {
                return loadScript(PLUGIN);
            });
        }
        return loading;
    }

    if (!window.L) {
        return;
    }
    L.Map.addInitHook(function () {
        const map = this;
        if (!map.getContainer().classList.contains("carto-basemap")) {
            return;
        }
        loadMapLibre().then(function () {
            L.maplibreGL({ style: STYLE, attribution: ATTRIBUTION }).addTo(map);
        });
    });
})();
