from api.common.pagination import (
    CursorPagination,
)


class ChallengeCursorPagination(CursorPagination):
    ordering = "id"

    def get_additional_metadata(self):
        return {
            "active_challenges": {
                "total": 100,
                "difficulties": [
                    {
                        "easy": 40,
                        "medium": 30,
                        "hard": 20,
                        "crazy": 10,
                    }
                ],
            }
        }
