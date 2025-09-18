"""Writer package."""

NODE_ATTRIBUTE_RE = r"([?&]([\w\-\_]+)=\"((?:\\\"|[^\"])+)\")"
NODE_RE = rf"((\.?\/?)([\w\-\_ ]+)({NODE_ATTRIBUTE_RE}*))"
