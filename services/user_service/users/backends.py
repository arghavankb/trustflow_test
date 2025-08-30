from django.contrib.auth.backends import BaseBackend
from ldap3 import Server, Connection, SUBTREE


class LDAPBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        if not email or not password:
            return None

        server = Server("172.19.19.2", port=389)
        conn = Connection(server, user=email, password=password)

        if not conn.bind():
            return None

        conn.search(
            search_base="OU=Root,DC=TomanPay,DC=local",
            search_filter=f"(mail={email})",
            search_scope=SUBTREE,
            attributes=[
                "givenName",
                "sn",
                "mail",
                "department",
                "title",
                "sAMAccountName",
            ],
        )

        if not conn.entries:
            return None

        attrs = conn.entries[0]

        return {
            "username": attrs.sAMAccountName.value if attrs.sAMAccountName else "",
            "email": email,
            "first_name": attrs.givenName.value if attrs.givenName else "",
            "last_name": attrs.sn.value if attrs.sn else "",
            "department": attrs.department.value if attrs.department else "",
            "title": attrs.title.value if attrs.title else "",
        }
