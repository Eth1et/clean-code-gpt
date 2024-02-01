project = QgsProject.instance()

# Symbol Rules
layer = project.mapLayersByName("Pontok")[0]

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()

def create_symbol_rule(label, filter_expression, color, size, name):
    rule = root_rule.children()[0].clone()
    rule.setLabel(label)
    rule.setFilterExpression(filter_expression)
    props = rule.symbol().symbolLayer(0).properties()
    props['color'] = color
    props['size'] = size
    props['name'] = name
    rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props)))
    root_rule.appendChild(rule)

create_symbol_rule('bus_stop', '"amenity" IS NULL', 'blue', '4', 'star')
create_symbol_rule('fuel_rule', '"amenity" = \'fuel\' OR "amenity" = \'charging_station\'', 'red', '4', 'square')
create_symbol_rule('else_rule', 'ELSE', 'yellow', '4', 'circle')

root_rule.removeChildAt(0)

layer.setRenderer(renderer)
layer.triggerRepaint()

# Count ...
layer_points = project.mapLayersByName("Pontok")[0]
layer_polygons = project.mapLayersByName("Települések")[0]
feature_name = 'buszmegall'

layer_polygons.startEditing() 
layer_polygons.addAttribute(QgsField(feature_name, QVariant.Int))
layer_polygons.updateFields()
layer_polygons.commitChanges()
iface.vectorLayerTools().stopEditing(layer_polygons)

with edit(layer_polygons):
    for feature_polygon in layer_polygons.getFeatures():
        count = 0
        geom_polygon = feature_polygon.geometry()
        for point_feature in layer_points.getFeatures():
            if geom_polygon.intersects(point_feature.geometry()) and not point_feature['amenity']:
                count += 1
        feature_polygon[feature_name] = QVariant(count)
        layer_polygons.updateFeature(feature_polygon)