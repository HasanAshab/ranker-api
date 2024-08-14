from django.test import TestCase, tag
from ranker.users.permissions import (
    DeleteUserPermission,
)
from ranker.users.factories import (
    UserFactory,
)


@tag("users", "permissions")
class DeleteUserPermissionTestCase(TestCase):
    fixtures = ["level_titles"]
    permission = DeleteUserPermission()

    def test_user_can_delete_own_account(
        self,
    ):
        user = UserFactory()
        result = self.permission.can_delete_user(user, user)
        self.assertTrue(result)

    def test_user_can_not_delete_other_users(
        self,
    ):
        user1, user2 = UserFactory.create_batch(2)
        result = self.permission.can_delete_user(user1, user2)
        self.assertFalse(result)

    def test_staff_can_delete_own_account(
        self,
    ):
        staff = UserFactory(staff=True)
        result = self.permission.can_delete_user(staff, staff)
        self.assertTrue(result)

    def test_staff_can_delete_user(
        self,
    ):
        staff = UserFactory(staff=True)
        user = UserFactory()
        result = self.permission.can_delete_user(staff, user)
        self.assertTrue(result)

    def test_staff_can_not_delete_other_staffs(
        self,
    ):
        staff1 = UserFactory(staff=True)
        staff2 = UserFactory(staff=True)
        result = self.permission.can_delete_user(staff1, staff2)
        self.assertFalse(result)

    def test_staff_can_not_delete_admin(
        self,
    ):
        staff = UserFactory(staff=True)
        admin = UserFactory(admin=True)
        result = self.permission.can_delete_user(staff, admin)
        self.assertFalse(result)

    def test_admin_can_delete_own_account(
        self,
    ):
        admin = UserFactory(admin=True)
        result = self.permission.can_delete_user(admin, admin)
        self.assertTrue(result)

    def test_admin_can_delete_user(
        self,
    ):
        admin = UserFactory(admin=True)
        user = UserFactory()
        result = self.permission.can_delete_user(admin, user)
        self.assertTrue(result)

    def test_admin_can_delete_staff(
        self,
    ):
        admin = UserFactory(admin=True)
        staff = UserFactory(staff=True)
        result = self.permission.can_delete_user(admin, staff)
        self.assertTrue(result)

    def test_admin_can_not_delete_other_admins(
        self,
    ):
        admin1 = UserFactory(admin=True)
        admin2 = UserFactory(admin=True)
        result = self.permission.can_delete_user(admin1, admin2)
        self.assertFalse(result)
