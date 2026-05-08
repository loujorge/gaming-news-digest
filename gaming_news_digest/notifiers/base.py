from __future__ import annotations

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseNotifier(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        ...

    def _chunk_message(self, message: str, max_chars: int = 4096) -> list[str]:
        if len(message) <= max_chars:
            return [message]

        chunks: list[str] = []
        current_chunk: list[str] = []
        current_len = 0

        for line in message.split("\n"):
            line_len = len(line) + 1  # +1 for newline
            if current_len + line_len > max_chars and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_len = 0
            if len(line) > max_chars:
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = []
                    current_len = 0
                for i in range(0, len(line), max_chars):
                    chunks.append(line[i : i + max_chars])
            else:
                current_chunk.append(line)
                current_len += line_len

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    def send_chunked(self, message: str, max_chars: int = 4096) -> bool:
        chunks = self._chunk_message(message, max_chars)
        total = len(chunks)
        all_ok = True

        for i, chunk in enumerate(chunks, 1):
            prefix = f"[{i}/{total}] " if total > 1 else ""
            if not self.send(prefix + chunk):
                logger.error("Failed to send chunk %d/%d", i, total)
                all_ok = False

        return all_ok
