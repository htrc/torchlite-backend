from fastapi import APIRouter
from app.models import torchlite as torchlite
from app.models import db as db


class WidgetPersistenceError(Exception):
    """Persistence error of some kind"""

    pass


router: APIRouter = APIRouter(prefix="/widgets", tags=["widgets"], responses={404: {"description": "Not found"}})


# def pack(widget: torchlite.Widget) -> db.Widget:
#     db_object: db.Widget = db.Widget(id=widget.id, widget_class=widget._widget_class, workset_id=widget.workset.id)
#     return db_object


# def unpack(data: dict) -> torchlite.Widget:
#     db_object: db.Widget = db.Widget(**data)
#     match db_object.widget_class:
#         case "timeline":
#             widget = torchlite.TimelineWidget()
#         case _:
#             raise WidgetPersistenceError("no widget class {db_object.widget_class}")

#     widget.id = db.Widget.id

#     return widget


# @router.get("/", tags=["widgets"], response_model=None)
# async def read_widgets(db: redis.Redis = Depends(get_db)) -> Any:
#     db_data: Any = db.hgetall("widgets")
#     data = []
#     for _, v in db_data.items():
#         ws: torchlite.Widget = unpack(json.loads(v))
#         data.append(ws)
#     return data


# @router.get("/{widget_id}", tags=["widgets"], response_model=None)
# async def read_widget(widget_id: str, db: redis.Redis = Depends(get_db)) -> Any:
#     db_data: bytes | None = db.hget("widgets", widget_id)
#     if db_data is None:
#         raise WidgetPersistenceError(f"could not retrieve {widget_id} from database")

#     data: dict = json.loads(db_data)
#     return unpack(data)
