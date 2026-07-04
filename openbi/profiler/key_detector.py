class KeyDetector:

    KEYWORDS = {

        "id",

        "_id",

        "key",

        "code",

        "number"

    }

    @classmethod
    def detect(cls, column_name, metadata):

        if not metadata.is_unique:
            return False

        if metadata.null_count > 0:
            return False

        name = column_name.lower()

        return any(word in name for word in cls.KEYWORDS)