import re

def get_ip_address(s: str, pattern = r"^[^:]+://[^:]+") -> str:
    if not s:
        return None
    result = re.match(pattern, s)

    if not result:
        return None

    return result.group(0)