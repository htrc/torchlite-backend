from uuid import uuid4


class TorchliteBase:
    def __init__(self) -> None:
        self.id = str(uuid4())
        self.persister = None
        self.ef_model = None


# class Dashboard(TorchliteBase):
#     def __init__(self) -> None:
#         super().__init__()
#         self.persister = persisters.DashboardPersister()

#     def __repr__(self) -> str:
#         return f"torchlite.Dashboard(id={self.id[-11:]})"

#     def persist(self):
#         if self.persister and self.ef_model:
#             self.persister.persist(self.ef_model)
