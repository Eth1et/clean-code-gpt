project_instance = QgsProject.instance()
bus_layer = project_instance.mapLayersByName("Pontok")[0]

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()

def create_rule(label, filter_expression, color, size, name):
    rule = root_rule.children()[0].clone()
    rule.setLabel(label)
    rule.setFilterExpression(filter_expression)
    props = rule.symbol().symbolLayer(0).properties()
    props['color'] = color
    props['size'] = size
    props['name'] = name
    rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props)))
    root_rule.appendChild(rule)

create_rule('bus_stop', '"amenity" IS NULL', 'blue', '4', 'star')
create_rule('fuel_rule', '"amenity" = \'fuel\' OR "amenity" = \'charging_station\'', 'red', '4', 'square')
create_rule('else_rule', 'ELSE', 'yellow', '4', 'circle')

root_rule.removeChildAt(0)

bus_layer.setRenderer(renderer)
bus_layer.triggerRepaint()

# Counting ...
point_layer = project_instance.mapLayersByName("Települések")[0]
feature_name = 'bus_stop_count'

point_layer.startEditing() 
point_layer.addAttribute(QgsField(feature_name, QVariant.Int))
point_layer.updateFields()
point_layer.commitChanges()
iface.vectorLayerTools().stopEditing(point_layer)

with edit(point_layer):
    for feature in point_layer.getFeatures():
        count = 0
        geom = feature.geometry()
        for point_feature in bus_layer.getFeatures():
            if geom.intersects(point_feature.geometry()) and point_feature['amenity'] == NULL:
                count += 1
        feature[feature_name] = QVariant(count)
        point_layer.updateFeature(feature)