def is_xpath_selector(selector):
    """
    A basic method to determine if a selector is an xpath selector.
    """
    if (
            selector.startswith("/")
            or selector.startswith("./")
            or selector.startswith("(")
    ):
        return True
    return False


def is_link_text_selector(selector):
    """
    A basic method to determine if a selector is a link text selector.
    """
    if (
            selector.startswith("link=")
            or selector.startswith("link_text=")
            or selector.startswith("text=")
    ):
        return True
    return False


def is_partial_link_text_selector(selector):
    """
    A basic method to determine if a selector is a partial link text selector.
    """
    if (
            selector.startswith("partial_link=")
            or selector.startswith("partial_link_text=")
            or selector.startswith("partial_text=")
            or selector.startswith("p_link=")
            or selector.startswith("p_link_text=")
            or selector.startswith("p_text=")
    ):
        return True
    return False


def is_name_selector(selector):
    """
    A basic method to determine if a selector is a name selector.
    """
    if selector.startswith("name=") or selector.startswith("&"):
        return True
    return False


def get_link_text_from_selector(selector):
    """
    A basic method to get the link text from a link text selector.
    """
    if selector.startswith("link="):
        return selector[len("link="):]
    elif selector.startswith("link_text="):
        return selector[len("link_text="):]
    elif selector.startswith("text="):
        return selector[len("text="):]
    return selector


def get_partial_link_text_from_selector(selector):
    """
    A basic method to get the partial link text from a partial link selector.
    """
    if selector.startswith("partial_link="):
        return selector[len("partial_link="):]
    elif selector.startswith("partial_link_text="):
        return selector[len("partial_link_text="):]
    elif selector.startswith("partial_text="):
        return selector[len("partial_text="):]
    elif selector.startswith("p_link="):
        return selector[len("p_link="):]
    elif selector.startswith("p_link_text="):
        return selector[len("p_link_text="):]
    elif selector.startswith("p_text="):
        return selector[len("p_text="):]
    return selector


def get_name_from_selector(selector):
    """
    A basic method to get the name from a name selector.
    """
    if selector.startswith("name="):
        return selector[len("name="):]
    if selector.startswith("&"):
        return selector[len("&"):]
    return selector

def is_id_selector(selector):
    """
    A basic method to determine whether a ID selector or not
    """
    if ":id" in selector:
        return True
    return False
