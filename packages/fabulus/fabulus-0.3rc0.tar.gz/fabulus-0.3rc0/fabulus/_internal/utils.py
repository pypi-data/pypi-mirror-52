def to_string(obj, protected: bool = False, internal: bool = False) -> str:
    """
    String representation of all variables of ``obj``

    :param obj: target object
    :param protected: include protected variables (_abc)
    :param internal: include internal variables (abc_)
    :return: String representation of ``obj``
    """
    clazz = obj.__class__.__name__

    printed_params = []
    for name, value in vars(obj).items():
        if (protected or not name.startswith('_')) and (internal or not name.endswith('_')):
            if type(value) is str:
                printed_params.append(f"{name}='{value}'")
            else:
                printed_params.append(f'{name}={value}')

    params = ', '.join(printed_params)

    return f'{clazz}({params})'
