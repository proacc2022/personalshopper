from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from product.models import Category, Product, Images


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "category_name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('category_name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'


class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'product_stock']
    list_filter = ['category', 'product_name']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('product_name',)}


class ImagesAdmin(admin.ModelAdmin):
    list_filter = ['product']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
