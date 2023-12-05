from authentication.views import InvoiceCrud
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'InvoiceCrud', InvoiceCrud, basename='InvoiceCrud')
urlpatterns = router.urls