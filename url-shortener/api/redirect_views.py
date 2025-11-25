from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.responses import RedirectResponse

from schemas.short_url import ShortUrl

from api.api_v1.short_urls.dependencies import prefetch_short_urls


router = APIRouter(prefix="/r", tags=["Redirect"])


"""
Возвращает объект сокращенной ссылки по ее slug

Параметры:
    slug (str): slug сокращенной ссылки

Возвращает:
    ShortUrl: объект сокращенной ссылки

Исключения:
    HTTPException: 404 если сокращенная ссылка не найдена
"""


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
):

    return RedirectResponse(url=str(url.target_url))
