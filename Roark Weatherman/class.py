class Weather():
    def __init__(self, region_name, region_type_id, modifier):
        self.region_name = region_name
        self.region_type_id = region_type_id
        self.modifier = modifier

    def increase_