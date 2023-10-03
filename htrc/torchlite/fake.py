from faker import Faker
from random import randint

from htrc.torchlite.models.schemas import WorksetSummary, VolumeMetadata, WorksetInfo

faker = Faker()


def generate_workset_summary() -> WorksetSummary:
    return WorksetSummary(
        id=faker.uuid4(),
        name=faker.word().lower(),
        description=faker.paragraph(),
        author=faker.name().lower(),
        isPublic=faker.boolean(),
        numVolumes=randint(1, 10),
    )


def generate_volume_metadata() -> VolumeMetadata:
    return VolumeMetadata(
        htid=faker.unique.word().lower(),
        title=faker.name(),
        pubDate=randint(1800, 2023),
        genre=faker.word().lower(),
        typeOfResource=faker.word().lower(),
        category=faker.word().lower(),
        contributor=faker.name(),
        publisher=faker.name(),
        accessRights="public",
        pubPlace=faker.city(),
        language=faker.language_name(),
        sourceInstitution=faker.company(),
    )


def generate_workset_info() -> WorksetInfo:
    num_vols = randint(1, 10)
    return WorksetInfo(
        id=faker.uuid4(),
        name=faker.word().lower(),
        description=faker.paragraph(),
        author=faker.word().lower(),
        isPublic=faker.boolean(),
        numVolumes=randint(1, 10),
        volumes=[
            generate_volume_metadata() for _ in range(num_vols)
        ]
    )