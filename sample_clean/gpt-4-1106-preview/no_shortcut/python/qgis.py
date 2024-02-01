project = QgsProject.instance()

# Retrieve layers by name
points_layer = project.mapLayersByName("Pontok")[0]
towns_layer = project.mapLayersByName("Települések")[0]

# Define a function to create symbol rules
def create_symbol_rule(label, expression, color, size, shape):
    rule = QgsRuleBasedRenderer.Rule(QgsMarkerSymbol())
    rule.setLabel(label)
    rule.setFilterExpression(expression)
    symbol_properties = rule.symbol().symbolLayer(0).properties()
    symbol_properties['color'] = color
    symbol_properties['size'] = size
    symbol_properties['name'] = shape
    rule.setSymbol(QgsMarkerSymbol.createSimple(symbol_properties))
    return rule

# Create a rule-based renderer
renderer = QgsRuleBasedRenderer(QgsMarkerSymbol())

# Access the root rule of the renderer
root_rule = renderer.rootRule()

# Define rules
bus_stop_rule = create_symbol_rule('Bus Stop', '"amenity" IS NULL', 'blue', '4', 'star')
fuel_rule = create_symbol_rule('Fuel', '"amenity" = \'fuel\' OR "amenity" = \'charging_station\'', 'red', '4', 'square')
else_rule = create_symbol_rule('Others', 'ELSE', 'yellow', '4', 'circle')

# Append rules as children of the root rule
root_rule.appendChild(bus_stop_rule)
root_rule.appendChild(fuel_rule)
root_rule.appendChild(else_rule)

# Remove the default rule
root_rule.removeChildAt(0)

# Set the renderer to the points layer
points_layer.setRenderer(renderer)
points_layer.triggerRepaint()

# Attribute name to count bus stops within towns
bus_stop_count_attr = 'buszmegall'

# Add attribute to count bus stops
attributes_addition = towns_layer.startEditing() 
towns_layer.addAttribute(QgsField(bus_stop_count_attr, QVariant.Int))
towns_layer.updateFields()
towns_layer.commitChanges()
iface.vectorLayerTools().stopEditing(towns_layer)

# Start editing towns layer to update feature counts
with edit(towns_layer):
    for town_feature in towns_layer.getFeatures():
        bus_stop_count = 0
        town_geometry = town_feature.geometry()
        for point_feature in points_layer.getFeatures():
            if town_geometry.intersects(point_feature.geometry()) and point_feature['amenity'] is None:
                bus_stop_count += 1
        town_feature[bus_stop_count_attr] = bus_stop_count
        towns_layer.updateFeature(town_feature)