from django.contrib import admin

from home.models import Post, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_joined")
    list_filter = ("date_joined",)
    search_fields = (
        "username",
        "email",
    )
    date_hierarchy = "date_joined"
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = ("groups", "user_permissions")
    raw_id_fields = ()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "user__username")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("user", "content", "image")}),
        (
            "Date information",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    filter_horizontal = ()
    raw_id_fields = ("user",)
