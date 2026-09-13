import hashlib
import math
import logging
from typing import List, Union
import numpy as np
from backend.config.settings import settings

logger = logging.getLogger(__name__)


class Embedder:
    """Multi-provider embedding generator with fixed 384-dimensional dense vectors."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.provider = settings.EMBEDDING_PROVIDER
        self._openai_client = None
        self._gemini_client = None

        if self.provider in ["gemini", "google"] and settings.GEMINI_API_KEY:
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except ImportError:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=settings.GEMINI_API_KEY)
                    self._gemini_client = genai
                except Exception as e:
                    logger.warning(f"Failed to initialize Gemini client for embeddings: {e}. Falling back to semantic projection.")
                    self.provider = "tfidf_semantic"
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client for embeddings: {e}. Falling back to semantic projection.")
                self.provider = "tfidf_semantic"

        if self.provider == "openai" and settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client for embeddings: {e}. Falling back to semantic projection.")
                self.provider = "tfidf_semantic"

    def embed_text(self, text: str) -> List[float]:
        """Generates a single dense vector embedding of dimension `self.dimension`."""
        if not text or not text.strip():
            return [0.0] * self.dimension

        if self.provider in ["gemini", "google"] and self._gemini_client:
            try:
                if hasattr(self._gemini_client, "models"):
                    res = self._gemini_client.models.embed_content(
                        model="text-embedding-004",
                        contents=text,
                    )
                    return res.embedding.values[: self.dimension]
                else:
                    res = self._gemini_client.embed_content(
                        model="models/text-embedding-004",
                        content=text,
                    )
                    return res["embedding"][: self.dimension]
            except Exception as e:
                logger.warning(f"Gemini embedding error: {e}. Falling back to semantic projection.")

        if self.provider == "openai" and self._openai_client:
            try:
                resp = self._openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text,
                    dimensions=self.dimension,
                )
                return resp.data[0].embedding
            except Exception as e:
                logger.warning(f"OpenAI embedding error: {e}. Falling back to semantic projection.")

        return self._semantic_dense_embed(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch embedding generation."""
        return [self.embed_text(t) for t in texts]

    def _semantic_dense_embed(self, text: str) -> List[float]:
        """High-entropy deterministic semantic projection with n-gram hashing and L2 normalization."""
        vec = np.zeros(self.dimension, dtype=np.float32)
        words = text.lower().replace("-", " ").split()

        # Word tokens and bigrams
        tokens = list(words)
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")

        for token in tokens:
            # MD5 hash to bucket index
            h = hashlib.md5(token.encode("utf-8")).hexdigest()
            idx = int(h[:8], 16) % self.dimension
            sign = 1.0 if int(h[8:10], 16) % 2 == 0 else -1.0
            # Weight term length and frequency
            weight = math.log(1.0 + len(token))
            vec[idx] += sign * weight

        # L2 normalize
        norm = np.linalg.norm(vec)
        if norm > 1e-6:
            vec = vec / norm
        return vec.tolist()
