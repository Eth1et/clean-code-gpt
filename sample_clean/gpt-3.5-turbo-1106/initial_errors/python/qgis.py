project = QgsProject.instance()

# Symbol Rules
layer = project.mapLayersByName("Pontok")[0]

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()

def create_rule(label, filter_exp, color, symbol_shape):
    rule = root_rule.children()[0].clone()
    rule.setLabel(label)
    rule.setFilterExpression(filter_exp)
    props = rule.symbol().symbolLayer(0).properties()
    props['color'] = color
    props['size'] = '4'
    props['name'] = symbol_shape
    rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props)))
    root_rule.appendChild(rule)

create_rule('bus_stop', '"amenity" IS NULL', 'blue', 'star')
create_rule('fuel_rule', '"amenity" = \'fuel\' OR "amenity" = \'charging_station\'', 'red', 'square')
create_rule('else_rule', 'ELSE', 'yellow', 'circle')

root_rule.removeChildAt(0)

layer.setRenderer(renderer)
layer.triggerRepaint()

# Count ...
layer_points = project.mapLayersByName("Pontok")[0]
layer_polygons = project.mapLayersByName("Települések")[0]
field_name = 'buszmegall'

layer_polygons.startEditing()
layer_polygons.addAttribute(QgsField(field_name, QVariant.Int))
layer_polygons.updateFields()
layer_polygons.commitChanges()
iface.vectorLayerTools().stopEditing(layer_polygons)

with edit(layer_polygons):
    for feature_polygon in layer_polygons.getFeatures():
        count = 0
        polygon_geom = feature_polygon.geometry()
        for point_feature in layer_points.getFeatures():
            if polygon_geom.intersects(point_feature.geometry()) and point_feature['amenity'] == NULL:
                count += 1
        feature_polygon[field_name] = QVariant(count)
        layer_polygons.updateFeature(feature_polygon)