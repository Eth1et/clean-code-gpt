project = QgsProject.instance()
points_layer = project.mapLayersByName("Pontok")[0]

renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())
root_rule = renderer.rootRule()

bus_stop_rule = root_rule.children()[0].clone()
bus_stop_rule.setLabel('bus_stop')
bus_stop_rule.setFilterExpression('"amenity" IS NULL')
bus_stop_symbol_props = bus_stop_rule.symbol().symbolLayer(0).properties()
bus_stop_symbol_props['color'] = 'blue'
bus_stop_symbol_props['size'] = '4'
bus_stop_symbol_props['name'] = 'star'
bus_stop_rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(bus_stop_symbol_props)))
root_rule.appendChild(bus_stop_rule)

fuel_rule = root_rule.children()[0].clone()
fuel_rule.setLabel('fuel_rule')
fuel_rule.setFilterExpression('"amenity" = \'fuel\' OR "amenity" = \'charging_station\'')
fuel_symbol_props = fuel_rule.symbol().symbolLayer(0).properties()
fuel_symbol_props['color'] = 'red'
fuel_symbol_props['size'] = '4'
fuel_symbol_props['name'] = 'square'
fuel_rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(fuel_symbol_props)))
root_rule.appendChild(fuel_rule)

else_rule = root_rule.children()[0].clone()
else_rule.setLabel('else_rule')
else_rule.setFilterExpression('ELSE')
else_symbol_props = else_rule.symbol().symbolLayer(0).properties()
else_symbol_props['color'] = 'yellow'
else_symbol_props['size'] = '4'
else_symbol_props['name'] = 'circle'
else_rule.setSymbol(QgsMarkerSymbol(QgsMarkerSymbol.createSimple(else_symbol_props)))
root_rule.appendChild(else_rule)

root_rule.removeChildAt(0)

points_layer.setRenderer(renderer)
points_layer.triggerRepaint()

# Count points within polygons
polygons_layer = project.mapLayersByName("Települések")[0]
point_count_field = 'buszmegall'

polygons_layer.startEditing() 
polygons_layer.addAttribute(QgsField(point_count_field, QVariant.Int))
polygons_layer.updateFields()
polygons_layer.commitChanges()
iface.vectorLayerTools().stopEditing(polygons_layer)

with edit(polygons_layer):
    for polygon_feature in polygons_layer.getFeatures():
        count = 0
        polygon_geom = polygon_feature.geometry()
        for point_feature in points_layer.getFeatures():
            if polygon_geom.intersects(point_feature.geometry()) and not point_feature['amenity']:
                count += 1
        polygon_feature[point_count_field] = QVariant(count)
        polygons_layer.updateFeature(polygon_feature)