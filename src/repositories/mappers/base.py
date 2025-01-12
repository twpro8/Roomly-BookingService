



class DataMapper:
    db_model = None
    schema = None

    def map_to_domain_entity(self, data):
        return self.schema.model_validate(data, from_attributes=True)

    def map_to_persistence_entity(self, data):
        return self.db_model(**data.model_dump())
