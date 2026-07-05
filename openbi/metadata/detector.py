class KeyDetector:

    @staticmethod
    def is_primary_key_candidate(column_name: str, metadata) -> bool:
        """
        Determine whether a column is a likely primary key.
        """

        if not metadata.is_unique:
            return False

        if metadata.null_count > 0:
            return False

        name = column_name.lower()

        keywords = [
            "id",
            "_id",
            "key",
            "code",
            "number"
        ]

        return any(keyword in name for keyword in keywords)
    
    @staticmethod
    def is_foreign_key_candidate(column_name: str, metadata) -> bool:
        """
        Determine whether a column is a likely foreign key.
        """

        name = column_name.lower()

        # Foreign keys are usually NOT unique
        if metadata.is_unique:
            return False

        keywords = (
            "id",
            "_id",
            "ref",
            "_ref",
            "fk"
        )

        return any(
            keyword in name
            for keyword in keywords
        )