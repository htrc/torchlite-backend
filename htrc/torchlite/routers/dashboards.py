from uuid import UUID

from authlib.oidc.core import UserInfo
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache
from pymongo import ReturnDocument
from starlette.requests import Request
from starlette.responses import Response

from ..auth.auth import get_current_user, get_user_access_token
from ..config import config
from ..data import apply_filters
from ..database import mongo_client
from ..ef.api import ef_api
from ..errors import TorchliteError
from ..managers.workset_manager import WorksetManager
from ..models.dashboard import DashboardSummary, DashboardPatch, DashboardCreate, DashboardPatchUpdate
from ..models.workset import WorksetIdMapping
from ..widgets.base import WidgetDataTypes

router = APIRouter(
    prefix="/dashboards",
    tags=["dashboards"],
)

def request_key_builder(func, namespace: str = "", *, request: Request = None, response: Response = None, args, **kwargs,):
    try:
        return request.url.path
    except AttributeError:
        return f"/dashboards/{args[0]}"

@router.get("/", description="Retrieve the available dashboards for a user", response_model_exclude_defaults=True)
@cache()
async def list_dashboards(owner: UUID | None = None,
                          user: UserInfo | None = Depends(get_current_user)) -> list[DashboardSummary]:
    if owner == config.TORCHLITE_UID:
        return await DashboardSummary.from_mongo(
            mongo_client.db["dashboards"].find({"owner": config.TORCHLITE_UID, "isShared": True}).to_list(1000)
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = UUID(user.get("htrc-guid", user.sub))
    owner = owner or user_id

    if user_id != owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await DashboardSummary.from_mongo(
        mongo_client.db["dashboards"].find({"owner": owner}).to_list(1000)
    )


@router.post("/", description="Create a new dashboard", response_model_exclude_defaults=True)
async def create_dashboard(dashboard_create: DashboardCreate,
                           workset_manager: WorksetManager,
                           owner: UUID | None = None,
                           user: UserInfo | None = Depends(get_current_user)) -> DashboardSummary:
    user_id = UUID(user.get("htrc-guid", user.sub)) if user else None
    owner = owner or user_id

    if user_id != owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await workset_manager.get_public_worksets()
    if not workset_manager.is_valid_workset(dashboard_create.imported_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown imported id {dashboard_create.imported_id}"
        )

    dashboard = DashboardSummary(**(dashboard_create.model_dump(exclude_defaults=True)), owner=owner)
    await mongo_client.db["dashboards"].insert_one(dashboard.to_mongo(exclude_unset=False))

    return dashboard


@router.get("/{dashboard_id}", description="Retrieve a dashboard", response_model_exclude_defaults=True)
@cache(key_builder=request_key_builder)
async def get_dashboard(dashboard_id: UUID,
                        user: UserInfo | None = Depends(get_current_user)) -> DashboardSummary:
    user_id = UUID(user.get("htrc-guid", user.sub)) if user else None
    dashboard = await DashboardSummary.from_mongo(
        mongo_client.db["dashboards"].find_one({"_id": dashboard_id, "$or": [{"isShared": True}, {"owner": user_id}]})
    )
    print(dashboard)
    if dashboard:
        print("A")
        return dashboard
    else:
        print("B")
        dashboard = await DashboardSummary.from_mongo(mongo_client.db["dashboards"].find_one({"_id": dashboard_id}))
        if not dashboard:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.patch("/{dashboard_id}", description="Update a dashboard", response_model_exclude_defaults=True)
async def update_dashboard(dashboard_id: UUID,
                           dashboard_patch: DashboardPatch,
                           workset_manager: WorksetManager,
                           user_access_token: UserInfo | None = Depends(get_user_access_token)) -> DashboardSummary:
    user = await get_current_user(user_access_token)
    await workset_manager.get_public_worksets()
    if (user_access_token):
        await workset_manager.get_user_worksets(user_access_token)

    if dashboard_patch.imported_id and not workset_manager.is_valid_workset(dashboard_patch.imported_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown workset id {dashboard_patch.imported_id}"
        )

    user_id = UUID(user.get("htrc-guid", user.sub)) if user else None
    dashboard_patch_update = DashboardPatchUpdate(**dashboard_patch.model_dump(exclude_defaults=True))
    dashboard = await DashboardSummary.from_mongo(
        mongo_client.db["dashboards"].find_one_and_update(
            filter={"_id": dashboard_id, "owner": user_id},
            update={"$set": dashboard_patch_update.to_mongo(exclude_unset=False)},
            return_document=ReturnDocument.AFTER
        )
    )
    if dashboard:
        try:
            for w in dashboard.widgets:
                await FastAPICache.clear(namespace=None,key=f"/dashboards/{dashboard_id}/widgets/{w.type}/data")
            await FastAPICache.clear(namespace=None,key=f"/dashboards/{dashboard_id}")
        except Exception as e:
            print(f"Error Clearing Cache: {e}")
        return dashboard
    else:
        dashboard = await DashboardSummary.from_mongo(mongo_client.db["dashboards"].find_one({"_id": dashboard_id}))
        if not dashboard:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        elif dashboard.owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{dashboard_id}/widgets/{widget_type}/data", description="Retrieve widget data")
@cache(key_builder=request_key_builder)
async def get_widget_data(dashboard_id: UUID, widget_type: str,
                          user: UserInfo | None = Depends(get_current_user)):
    dashboard = await get_dashboard(dashboard_id, user)

    # fastapi_cache doesn't seem to preserve pydantic models and instead returns dicts, so converting
    # dashboard to the expected model type if it is just a dict, so that dashboard.widgets doesn't
    # throw an error.
    # This is happening only when an endpoint calls another method that is cached. Direct calls to
    # endpoints that return pydantic models are not affected.
    if isinstance(dashboard, dict):
        dashboard = DashboardSummary.model_validate(dashboard)
        
    widget = next((w for w in dashboard.widgets if w.type == widget_type), None)
    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Widget type {widget_type} not part of dashboard {dashboard_id}"
        )
    imported_id_mapping = (await WorksetIdMapping.from_mongo(mongo_client.db["id-mappings"].find({"importedId": dashboard.imported_id}).to_list(1000)))[0]

    match widget.data_type:
        case WidgetDataTypes.metadata_only:
            volumes = await ef_api.get_workset_metadata(imported_id_mapping.workset_id)

        case WidgetDataTypes.vols_with_pos:
            volumes = await ef_api.get_workset_volumes(imported_id_mapping.workset_id, include_pos=True)

        case WidgetDataTypes.vols_no_pos:
            volumes = await ef_api.get_workset_volumes(imported_id_mapping.workset_id, include_pos=False)

        case WidgetDataTypes.agg_vols_no_pos:
            volumes = await ef_api.get_aggregated_workset_volumes(imported_id_mapping.workset_id)

        case _:
            raise TorchliteError(f"Unsupported widget data type {widget.data_type}")

    filtered_volumes = apply_filters(volumes, filters=dashboard.filters)
    return await widget.get_data(filtered_volumes)


@router.get("/{dashboard_id}/{data_type}", description="Retrieve meta data")
async def get_workset_data(dashboard_id: UUID, data_type: str,
    filtered: bool = False, user: UserInfo | None = Depends(get_current_user)):
    dashboard = await get_dashboard(dashboard_id, user)
    print('get_workset_data')
    print(dashboard)
    
    imported_id_mapping = (await WorksetIdMapping.from_mongo(mongo_client.db["id-mappings"].find({"importedId": dashboard.imported_id}).to_list(1000)))[0]

    ef_wsid = imported_id_mapping.workset_id

    match data_type:
        case "metadata":
            volumes = await ef_api.get_workset_metadata(ef_wsid)
        case "data":
            volumes = await ef_api.get_workset_volumes(ef_wsid, include_pos=True)
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid data_type '{data_type}'. Expected 'data' or 'metadata'."
            )
    if filtered:
        volumes = apply_filters(volumes, filters=dashboard.filters)

    return volumes

    #return await widget.get_data(filtered_volumes)
