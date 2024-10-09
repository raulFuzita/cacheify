import os

def get_env_var(name, default=None, var_type=str):
    """
    Retrieve an environment variable and cast it to the specified type.

    :param name: The name of the environment variable
    :param default: The default value to return if the environment variable is not set
    :param var_type: The type to which the environment variable should be cast
    :return: The environment variable cast to the specified type, or the default value
    """
    value = os.getenv(name, default)

    if value is None:
        return default

    try:
        if var_type == bool:
            # Convert to boolean: True if the string is 'true' (case insensitive), else False
            return value.lower() in ['true', '1', 'yes', 'y', 'on']
        elif var_type == int:
            # Convert to integer
            return int(value)
        elif var_type == float:
            # Convert to float
            return float(value)
        else:
            # Default case: return the value as is, assuming it's a string
            return value
    except ValueError:
        # If conversion fails, return the default value
        return default