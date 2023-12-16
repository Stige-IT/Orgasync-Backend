from multiprocessing import managers

from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer
from alembic import op

role_table = table("role", column("id", String), column("name", String))
type_employee_table = table("type_employee", column("id", String), column("name", String), column("level", Integer))
type_company_table = table("type_company", column("id", String), column("name", String))


def seed_data():
    op.bulk_insert(
        role_table,
        [
            {"id": "a4e87ae3-5241-4a97-bcb5-61419af5cbf5", "name": "admin"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf11", "name": "user"},
        ],
    )
    op.bulk_insert(
        type_employee_table,
        [
            {"id": "8519592b-bac4-4bf7-922b-1766734ea7bd", "name": "owner", "level": 1},
            {"id": "8eba784c-5b18-45aa-b572-5423d2bb0d99", "name": "director", "level": 2},
            {"id": "c2e001c0-ecdc-44fe-a2be-4459c2c21bd6", "name": "manager", "level": 3},
            {"id": "1dd1cf31-31b5-489f-8d95-2b0376008eae", "name": "staff", "level": 4},
            {"id": "3045240d-9ee3-496d-9193-89ff8bb74573", "name": "intern", "level": 5},
            {"id": "879a1624-7254-4d2a-8c16-e38a32b5414d", "name": "freelance", "level": 6},
            {"id": "b922ff3a-0d49-4a7e-9b08-e5ecbd72dc33", "name": "part time", "level": 7},
            {"id": "11a576ee-14b8-4c3a-9b6d-53d677fa3ab2", "name": "client", "level": 8},
            {"id": "e6a0638f-211e-48b0-ba5d-88a34c8f0d94", "name": "guest", "level": 9},

        ],
    )

    op.bulk_insert(
        type_company_table,
        [
            {"id": "a4e87ae3-5241-4a97-bcb5-61419af5cbf5", "name": "Startup"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf11", "name": "Agency"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf12", "name": "Enterprise"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf13", "name": "Government"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf14", "name": "Education"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf15", "name": "Non Profit"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf16", "name": "Self Employed"},
            {"id": "40dce257-335b-480a-a3cd-163e2d74cf17", "name": "Other"},
        ],
    )
