def get_metadata_value(meta):
    if 'metadata-value' in meta:
        return meta['metadata-value']
    else:
        return '\033[31mEmpty\033[0m'
