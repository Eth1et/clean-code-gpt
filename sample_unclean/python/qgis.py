project = QgsProject.instance()

# Symbol Rules
v = project.mapLayersByName("Pontok")[0]

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()

bus_stop_rule = root_rule.children()[0].clone()
bus_stop_rule.setLabel('bus_stop')
bus_stop_rule.setFilterExpression('"amenity" IS NULL')
props = bus_stop_rule.symbol().symbolLayer(0).properties()
props['color'] = 'blue'
props['size'] = '4'
props['name'] = 'star'
bus_stop_rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props)));
root_rule.appendChild(bus_stop_rule)

fuel_rule = root_rule.children()[0].clone()
fuel_rule.setLabel('fuel_rule')
fuel_rule.setFilterExpression('"amenity" = \'fuel\' OR "amenity" = \'charging_station\'')
props = fuel_rule.symbol().symbolLayer(0).properties()
props['color'] = 'red'
props['size'] = '4'
props['name'] = 'square'
fuel_rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props)));
root_rule.appendChild(fuel_rule)

else_rule = root_rule.children()[0].clone()
else_rule.setLabel('else_rule')
else_rule.setFilterExpression('ELSE')
props = else_rule.symbol().symbolLayer(0).properties()
props['color'] = 'yellow'
props['size'] = '4'
props['name'] = 'circle'
else_rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(props)));
root_rule.appendChild(else_rule)

root_rule.removeChildAt(0)

v.setRenderer(renderer)
v.triggerRepaint()

# Count ...
t = project.mapLayersByName("Települések")[0]
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
            if geom.intersects(point_feature.geometry()) and point_feature['amenity'] == NULL:
                count += 1
        feature[feature_name] = QVariant(count)
        t.updateFeature(feature)
