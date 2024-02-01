project = QgsProject.instance()
points_layer = project.mapLayersByName("Pontok")[0]
v = points_layer

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()

def create_rule(label, filter_expression, color, size, symbol_name):
    rule = root_rule.children()[0].clone()
    rule.setLabel(label)
    rule.setFilterExpression(filter_expression)
    props = rule.symbol().symbolLayer(0).properties()
    props['color'] = color
    props['size'] = size
    props['name'] = symbol_name
    rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props)))
    root_rule.appendChild(rule)

bus_stop_rule = create_rule('bus_stop', '"amenity" IS NULL', 'blue', '4', 'star')
fuel_rule = create_rule('fuel_rule', '"amenity" = \'fuel\' OR "amenity" = \'charging_station\'', 'red', '4', 'square')
else_rule = create_rule('else_rule', 'ELSE', 'yellow', '4', 'circle')

root_rule.removeChildAt(0)

v.setRenderer(renderer)
v.triggerRepaint()

# Count ...
settlements_layer = project.mapLayersByName("Települések")[0]
t = settlements_layer
feature_name = 'buszmegall'

t.startEditing() 
t.addAttribute(QgsField(feature_name, QVariant.Int))
t.updateFields()
t.commitChanges()
iface.vectorLayerTools().stopEditing(t)

with edit(t):
    for feature in t.getFeatures():
        count = 0
        geom = feature.geometry()
        for point_feature in v.getFeatures():
            if geom.intersects(point_feature.geometry()) and not point_feature['amenity']:
                count += 1
        feature[feature_name] = QVariant(count)
        t.updateFeature(feature)