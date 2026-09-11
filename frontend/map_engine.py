import pydeck as pdk
import pandas as pd

# Curated High-Tech Neon Palette for 3D Cadastral Visualization
COLOR_PALETTE = {
    'Commercial': [0, 212, 255, 230],          # Neon Cyan
    'Apartment': [168, 85, 247, 230],          # Electric Violet
    'Underground Parking': [251, 146, 60, 240],# Glowing Amber
    'Transit': [16, 185, 129, 230],            # Cyber Emerald
    'Subsurface Utility': [244, 63, 94, 240],  # Rose / Magma Red
}

import json
import base64

# Satellite & Hybrid raster styles for MapLibre / Deck.gl
_ESRI_SATELLITE_SPEC = {
    "version": 8,
    "sources": {
        "satellite": {
            "type": "raster",
            "tiles": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],
            "tileSize": 256,
            "maxzoom": 19
        }
    },
    "layers": [
        {"id": "satellite-layer", "type": "raster", "source": "satellite", "minzoom": 0, "maxzoom": 22}
    ]
}

_HYBRID_SATELLITE_SPEC = {
    "version": 8,
    "sources": {
        "satellite": {
            "type": "raster",
            "tiles": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],
            "tileSize": 256,
            "maxzoom": 19
        },
        "labels": {
            "type": "raster",
            "tiles": ["https://basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}.png"],
            "tileSize": 256,
            "maxzoom": 19
        }
    },
    "layers": [
        {"id": "satellite-layer", "type": "raster", "source": "satellite", "minzoom": 0, "maxzoom": 22},
        {"id": "labels-layer", "type": "raster", "source": "labels", "minzoom": 0, "maxzoom": 22}
    ]
}

_SATELLITE_URI = "data:application/json;base64," + base64.b64encode(json.dumps(_ESRI_SATELLITE_SPEC).encode()).decode()
_HYBRID_URI = "data:application/json;base64," + base64.b64encode(json.dumps(_HYBRID_SATELLITE_SPEC).encode()).decode()

MAP_STYLES = {
    "🛰️ Satellite View (High-Res)": _SATELLITE_URI,
    "🛰️ Hybrid Satellite (Labels & Roads)": _HYBRID_URI,
    "🌌 Dark Matter (Default)": "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    "☀️ Minimalist Light": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
    "🧭 Voyager Detailed": "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
}

CITY_VIEWPORTS = {
    "🇮🇳 Pan-India (National Cadastre)": {"lat": 22.5000, "lon": 79.5000, "zoom": 4.3, "pitch": 35, "bearing": 0, "radius": 22000, "scale": 1800},
    "🇮🇳 Pan-India (Subcontinent)": {"lat": 22.5000, "lon": 79.5000, "zoom": 4.3, "pitch": 35, "bearing": 0, "radius": 22000, "scale": 1800},
    "Gurugram (NCR - Cyber City & Golf Course Corridor)": {"lat": 28.4952, "lon": 77.0895, "zoom": 15.2, "pitch": 62, "bearing": 30, "radius": 75, "scale": 1},
    "Navi Mumbai (MMR - Belapur & Seawoods TOD)": {"lat": 19.0216, "lon": 73.0181, "zoom": 15.3, "pitch": 62, "bearing": 32, "radius": 70, "scale": 1},
    "Mumbai (MMR - Worli Sea Face & BKC Financial Centre)": {"lat": 19.0400, "lon": 72.8400, "zoom": 13.0, "pitch": 60, "bearing": 25, "radius": 130, "scale": 1},
    "New Delhi (NCT - Lutyens & Central Business District)": {"lat": 28.6328, "lon": 77.2197, "zoom": 14.5, "pitch": 58, "bearing": 20, "radius": 110, "scale": 1},
    "Bengaluru Urban (BBMP - IT Corridor, Whitefield & CBD)": {"lat": 12.9780, "lon": 77.6100, "zoom": 13.0, "pitch": 60, "bearing": 30, "radius": 140, "scale": 1},
    "GIFT City (Gandhinagar / Ahmedabad IFSC)": {"lat": 23.1610, "lon": 72.6840, "zoom": 15.6, "pitch": 64, "bearing": 40, "radius": 65, "scale": 1},
    "Hyderabad (GHMC - Cyberabad & HITEC City)": {"lat": 17.4480, "lon": 78.3800, "zoom": 14.2, "pitch": 60, "bearing": 30, "radius": 110, "scale": 1},
    "Chennai (GCC - OMR IT Expressway & Central)": {"lat": 13.0200, "lon": 80.2600, "zoom": 13.2, "pitch": 58, "bearing": 20, "radius": 130, "scale": 1},
    "Kolkata (KMC - New Town IT Hub & Underwater Metro)": {"lat": 22.5830, "lon": 88.4000, "zoom": 13.2, "pitch": 58, "bearing": 20, "radius": 130, "scale": 1},
}

def render_3d_map(df, selected_region=None, custom_center=None, map_theme="Dark Matter (Default)", selected_property_id=None):
    """
    Renders an interactive, futuristic 3D Cadastral Deck.gl map.
    Supports pan-India continent scale down to micro-parcel vertical footprints.
    Highlights the selected parcel with vibrant cyan and ground beacon halo.
    """
    if df.empty:
        # Fallback empty view centered on India
        view_state = pdk.ViewState(latitude=22.5, longitude=79.5, zoom=4.3, pitch=30)
        return pdk.Deck(layers=[], initial_view_state=view_state)

    map_df = df.copy()

    # Determine colors - highlight selected parcel in bright cyber cyan
    if selected_property_id is not None:
        map_df['color'] = map_df.apply(
            lambda r: [0, 242, 254, 255] if r['property_id'] == selected_property_id else COLOR_PALETTE.get(r['type'], [148, 163, 184, 220]),
            axis=1
        )
    else:
        map_df['color'] = map_df['type'].apply(lambda x: COLOR_PALETTE.get(x, [148, 163, 184, 220]))
    
    # Tooltip label formatting
    map_df['elevation_label'] = map_df.apply(
        lambda r: f"Subsurface: {r['base_elevation']}m to {r['base_elevation'] + r['total_height']}m" 
        if r['base_elevation'] < 0 
        else f"Surface to +{r['total_height']}m",
        axis=1
    )
    map_df['archetype_display'] = map_df['archetype'].apply(
        lambda a: str(a).replace('_', ' ').title() if pd.notna(a) and str(a) != 'None' else 'Parametric Modern'
    ) if 'archetype' in map_df.columns else 'Parametric Modern'

    # Determine camera view state & scale
    pan_india_default = CITY_VIEWPORTS.get("🇮🇳 Pan-India (National Cadastre)") or CITY_VIEWPORTS.get("🇮🇳 Pan-India (Subcontinent)") or list(CITY_VIEWPORTS.values())[0]
    preset = CITY_VIEWPORTS.get(selected_region, pan_india_default) if selected_region else pan_india_default
    
    if custom_center:
        # Focusing on a specific selected property
        view_lat = custom_center['lat']
        view_lon = custom_center['lon']
        zoom = 16.4
        pitch = 65
        bearing = 35
        radius = 55
        elevation_scale = 1
    elif selected_region and (selected_region.startswith("🇮🇳") or "Pan-India" in selected_region):
        view_lat = preset["lat"]
        view_lon = preset["lon"]
        zoom = preset["zoom"]
        pitch = preset["pitch"]
        bearing = preset["bearing"]
        radius = preset["radius"]
        elevation_scale = preset["scale"]
    else:
        # Specific city or preset selected
        view_lat = preset["lat"]
        view_lon = preset["lon"]
        zoom = preset["zoom"]
        pitch = preset["pitch"]
        bearing = preset["bearing"]
        radius = preset["radius"]
        elevation_scale = 1

    view_state = pdk.ViewState(
        latitude=view_lat,
        longitude=view_lon,
        zoom=zoom,
        pitch=pitch,
        bearing=bearing
    )

    layers = []

    # 1. Main 3D Cadastral Extrusion Layer
    column_layer = pdk.Layer(
        'ColumnLayer',
        data=map_df,
        get_position='[lon, lat]',
        get_elevation='total_height',
        elevation_scale=elevation_scale,
        radius=radius,
        get_fill_color='color',
        pickable=True,
        extruded=True,
        auto_highlight=True,
    )
    layers.append(column_layer)

    # 2. Add halo / ground footprint ring for subsurface & iconic parcels
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=map_df,
        get_position='[lon, lat]',
        get_radius=radius * 1.35,
        get_fill_color=[255, 255, 255, 40],
        get_line_color='color',
        line_width_min_pixels=2,
        stroked=True,
        filled=True,
        pickable=False
    )
    layers.append(scatter_layer)

    # 3. Dedicated Glowing Beacon Ring for Selected Property
    if selected_property_id is not None:
        sel_subset = map_df[map_df['property_id'] == selected_property_id]
        if not sel_subset.empty:
            sel_halo = pdk.Layer(
                'ScatterplotLayer',
                id="selected-beacon-halo",
                data=sel_subset,
                get_position='[lon, lat]',
                get_radius=radius * 2.2,
                get_fill_color=[0, 242, 254, 70],
                get_line_color=[0, 242, 254, 255],
                line_width_min_pixels=3,
                stroked=True,
                filled=True,
                pickable=False
            )
            layers.append(sel_halo)

    # Add Satellite raster tile layers if satellite mode is selected
    if "Satellite" in map_theme:
        sat_tile_layer = pdk.Layer(
            "TileLayer",
            id="esri-satellite-basemap",
            data="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            min_zoom=0,
            max_zoom=19,
            tile_size=256
        )
        layers.insert(0, sat_tile_layer)
        if "Hybrid" in map_theme:
            label_tile_layer = pdk.Layer(
                "TileLayer",
                id="carto-labels-overlay",
                data="https://basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}.png",
                min_zoom=0,
                max_zoom=19,
                tile_size=256
            )
            layers.append(label_tile_layer)

    # Informative & Minimalist Glassmorphism Tooltip
    tooltip_html = """
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; min-width: 200px; padding: 4px 6px;">
        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; font-weight: 600; margin-bottom: 2px;">
            {city}, {state} &bull; ID: #{property_id}
        </div>
        <div style="font-size: 14px; font-weight: 700; color: #ffffff; margin-bottom: 6px;">
            {name}
        </div>
        <div style="font-size: 11px; margin-bottom: 3px; color: #cbd5e1;">
            <span style="color: #64748b;">Type:</span> <b>{type}</b> &bull; <span style="color: #38bdf8;">{archetype_display}</span>
        </div>
        <div style="font-size: 11px; margin-bottom: 3px; color: #cbd5e1;">
            <span style="color: #64748b;">Vertical Span:</span> <b>{total_height}m</b> ({elevation_label})
        </div>
        <div style="font-size: 11px; margin-bottom: 3px; color: #cbd5e1;">
            <span style="color: #64748b;">Owner:</span> {owner}
        </div>
        <div style="font-size: 11px; margin-top: 5px; padding-top: 4px; border-top: 1px solid rgba(255,255,255,0.1); color: #38bdf8;">
            <b>₹{valuation_cr} Cr</b> &bull; <span style="color: #10b981;">{status}</span>
        </div>
    </div>
    """

    # Resolve map style with fuzzy fallback
    map_style_url = MAP_STYLES.get(map_theme)
    if not map_style_url:
        for k, v in MAP_STYLES.items():
            if map_theme.lower() in k.lower():
                map_style_url = v
                break
    if not map_style_url:
        map_style_url = MAP_STYLES["🌌 Dark Matter (Default)"]

    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={
            "html": tooltip_html,
            "style": {
                "backgroundColor": "rgba(15, 23, 42, 0.94)",
                "backdropFilter": "blur(8px)",
                "color": "#ffffff",
                "border": "1px solid rgba(255, 255, 255, 0.12)",
                "borderRadius": "10px",
                "boxShadow": "0 12px 30px rgba(0, 0, 0, 0.5)",
                "padding": "10px 14px"
            }
        },
        map_style=map_style_url,
        height=680
    )