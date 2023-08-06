def parse_config(config: dict) -> dict:
    """
    parses the dictionary so that restructure function can understand it

    :param config: unparsed raw dictionary of details
    :return: parsed dictionary of details
    """
    parsed_object = {}
    for key in config:
        for template in config[key]:
            if type(template) == dict:  # renaming of files
                parsed_object[template['old']] = {
                    'dir': key,
                    'file': template['new']
                }

            else:
                parsed_object[template] = {
                    'dir': key,
                    'file': template
                }

    return parsed_object
