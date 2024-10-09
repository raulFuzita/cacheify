import sys

def python_version() -> str:
    """
    Returns the current Python version as a string in the format 'major.minor.micro'.
    
    Returns:
        str: The Python version.
    """
    version_info = sys.version_info
    return f"{version_info.major}.{version_info.minor}.{version_info.micro}"


def compare_python_version(passed_version: str) -> int:
    """
    Compare the current Python version with a passed version string.

    Args:
        passed_version (str): The version string to compare against the current Python version.
                              It should be in the format 'major.minor.patch', e.g., '3.9.2' or '3.9'.

    Returns:
        int: Returns -1 if the current Python version is less than the passed version,
             0 if they are equal, and 1 if the current Python version is greater.

    Raises:
        ValueError: If the passed version string is not in a valid format.
    """
    try:
        # Convert the current Python version to a tuple
        current_version_tuple = sys.version_info[:3]

        # Convert the passed version to a tuple of integers, padding missing components
        passed_version_parts = passed_version.split(".")
        passed_version_tuple = tuple(int(part) for part in passed_version_parts) + (0,) * (3 - len(passed_version_parts))

        # Compare the current and passed versions
        if current_version_tuple < passed_version_tuple:
            return -1
        elif current_version_tuple == passed_version_tuple:
            return 0
        else:
            return 1
    except ValueError:
        raise ValueError("Invalid version format. Please use a format like '3.9.2' or '3.9'.")