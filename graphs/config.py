def config():
    # Configurations for the graph
    return dict({
        'toImageButtonOptions' : {
            'format': 'svg', 
            'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
        },
        'displaylogo' : False,
        'modeBarButtonsToRemove' : [
            "zoom2d", 
            "pan2d", 
            "select2d", 
            "lasso2d", 
            "zoomIn2d", 
            "zoomOut2d",
            "hoverClosestCartesian", 
            "hoverCompareCartesian", 
            "zoom3d", 
            "pan3d", 
            "orbitRotation", 
            "tableRotation", 
            "handleDrag3d", 
            "resetCameraDefault3d", 
            "resetCameraLastSave3d", 
            "hoverClosest3d",
            "zoomInGeo", 
            "zoomOutGeo", 
            "resetGeo", 
            "hoverClosestGeo", 
            "hoverClosestGl2d", 
            "hoverClosestPie", 
            "toggleHover", 
            "resetViews"
        ]
    }  
    )