project = QgsProject.instance()

# Define symbol rules
points_layer = project.mapLayersByName("Pontok")[0]

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()

def create_rule(label, filter_exp, color, size, name):
    rule = root_rule.children()[0].clone()
    rule.setLabel(label)
    rule.setFilterExpression(filter_exp)
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

points_layer.setRenderer(renderer)
points_layer.triggerRepaint()

# Count intersections
towns_layer = project.mapLayersByName("Települések")[0]
feature_name = 'buszmegall'

towns_layer.startEditing()
field = QgsField(feature_name, QVariant.Int)
towns_layer.addAttribute(field)
towns_layer.updateFields()
towns_layer.commitChanges()
iface.vectorLayerTools().stopEditing(towns_layer)

with edit(towns_layer):
    for town_feature in towns_layer.getFeatures():
        count = 0
        town_geom = town_feature.geometry()
        for point_feature in points_layer.getFeatures():
            if town_geom.intersects(point_feature.geometry()) and point_feature['amenity'] is None:
                count += 1
        town_feature[feature_name] = QVariant(count)
        towns_layer.updateFeature(town_feature)