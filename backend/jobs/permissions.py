# jobs/permissions.py
from rest_framework.permissions import BasePermission, IsAdminUser


class IsApprovedStudent(BasePermission):
    """
    Allow only authenticated users who have a Student profile approved.
    """
    message = "Student account is not approved by admin yet."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        prof = getattr(user, "student_profile", None)
        return bool(prof and prof.is_approved)


class IsApprovedCompany(BasePermission):
    """
    Allow only authenticated users who have a Company profile approved.
    """
    message = "Company account is not approved by admin yet."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        prof = getattr(user, "company_profile", None)
        return bool(prof and prof.is_approved)
