import requests
import sys
from typing import List, Dict, Any, Optional


def get_reviews(
    url: str = "http://localhost:8000/api/v1/reviews/",
    timeout: int = 10,
    auth_token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Obtiene reseñas desde la API.

    Args:
        url: URL de la API
        timeout: Tiempo máximo de espera para la respuesta
        auth_token: Token de autenticación (si es necesario)

    Returns:
        Lista de reseñas

    Raises:
        Exception: Si hay errores en la solicitud
    """
    headers = {"accept": "application/json", "User-Agent": "ReviewClient/1.0"}

    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Lanza excepción para códigos de error HTTP

        if response.headers.get("content-type") != "application/json":
            raise ValueError(
                f"Formato de respuesta inesperado: {response.headers.get('content-type')}"
            )

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}", file=sys.stderr)
        raise
    except ValueError as e:
        print(f"Error al procesar la respuesta: {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        raise


def display_reviews(reviews: List[Dict[str, Any]]) -> None:
    """Muestra las reseñas formateadas"""
    if not reviews:
        print("No se encontraron reseñas.")
        return

    for review in reviews:
        print(f"Score: {review['score']} - {review['review']}")


if __name__ == "__main__":
    try:
        reviews = get_reviews()
        display_reviews(reviews)
    except Exception:
        sys.exit(1)
