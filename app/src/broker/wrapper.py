class TransferObject:
    # Wrapper třída pro přenášení dat mezi skripty
    def __init__(self, operation, entity, data):
        self.operation = operation
        self.entity = entity
        # Generované ID pro MongoDB
        data['_id'] = f"{entity}_{data['id']}"
        self.data = self.convert_ids(data)

    def to_dict(self):
        return {
            'operation': self.operation,
            'entity': self.entity,
            'data': self.data
        }

    # Konverze ID z MySQL entity do Monga
    def convert_ids(self, original_data):
        id_aliases = {
            'author': 'user',
        }

        converted_data = {}
        for key, value in original_data.items():
            if key.endswith("_id") and len(key) > 3 and str(value).isnumeric():
                original_key = key[:-3]
                if original_key in id_aliases:
                    alias = id_aliases[original_key]
                    converted_data[key] = f"{alias}_{value}"
                else:
                    converted_data[key] = f"{key[:-3]}_{value}"
            else:
                converted_data[key] = value
        return converted_data

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict['operation'], data_dict['entity'], data_dict['data'])
