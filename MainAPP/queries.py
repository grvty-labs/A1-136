from . import models
from django.db.models import Prefetch


def CanvasImages(user, filters=None):
    # TODO:
    # Dado el usuario, es necesario obtener las respuestas seleccionadas para
    # poder determinar las imágenes a mostrar, pero debido a que existen
    # preguntas que se ordenan por prioridad, será necesario esperar a que
    # Diana nos indique la forma de calcular la categoría a partir de dicho
    # tipo de preguntas. Por lo mientras se usará un DUMMY
    categories = models.Category.objects.filter(hidden=False).prefetch_related(
        Prefetch(
            'clusters',
            queryset=models.Cluster.objects.filter(hidden=False)
        ),
        Prefetch(
           'clusters__isometric_images',
           queryset=models.IsometricImage.objects.filter(hidden=False)
        ),
    )
    return categories
