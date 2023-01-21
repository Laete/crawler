import dataclasses
import enum


class LinkProcessingStatus(str, enum.Enum):
    NOT_PROCESSED = 'NOT_PROCESSED'
    IN_PROGRESS = 'IN_PROGRESS'
    PROCESSED = 'PROCESSED'


@dataclasses.dataclass
class Link:
    url: str
    depth: int
