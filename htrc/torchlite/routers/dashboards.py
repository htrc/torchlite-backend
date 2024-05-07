from uuid import UUID

from authlib.oidc.core import UserInfo
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import ReturnDocument

from ..auth.auth import get_current_user
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


@router.get("/", description="Retrieve the available dashboards for a user", response_model_exclude_defaults=True)
async def list_dashboards(owner: UUID | None = None,
                          user: UserInfo | None = Depends(get_current_user)) -> list[DashboardSummary]:
#    print("list dashboards")
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
#    print("create dashboard")
#    print(dashboard_create)
    user_id = UUID(user.get("htrc-guid", user.sub)) if user else None
    owner = owner or user_id

    if user_id != owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

#    print("workset id")
#    print(dashboard_create.imported_id)
    await workset_manager.get_public_worksets()
    if not workset_manager.is_valid_workset(dashboard_create.imported_id):
#        print("imported id not in public worksets")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown imported id {dashboard_create.imported_id}"
        )

    # dashboard = DashboardSummary.model_construct(**dashboard_create.model_dump(exclude_defaults=True), owner=owner)
    dashboard = DashboardSummary(**(dashboard_create.model_dump(exclude_defaults=True)), owner=owner)
    await mongo_client.db["dashboards"].insert_one(dashboard.to_mongo(exclude_unset=False))

    return dashboard


@router.get("/{dashboard_id}", description="Retrieve a dashboard", response_model_exclude_defaults=True)
async def get_dashboard(dashboard_id: UUID,
                        user: UserInfo | None = Depends(get_current_user)) -> DashboardSummary:
#    print("get dashboard")
#    print(dashboard_id)
#    print(user)
    user_id = UUID(user.get("htrc-guid", user.sub)) if user else None
    dashboard = await DashboardSummary.from_mongo(
        mongo_client.db["dashboards"].find_one({"_id": dashboard_id, "$or": [{"isShared": True}, {"owner": user_id}]})
    )
#    print("dashboard")
#    print(dashboard)
    if dashboard:
#        print("returning")
        return dashboard
    else:
        dashboard = await DashboardSummary.from_mongo(mongo_client.db["dashboards"].find_one({"_id": dashboard_id}))
        if not dashboard:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.patch("/{dashboard_id}", description="Update a dashboard", response_model_exclude_defaults=True)
async def update_dashboard(dashboard_id: UUID,
                           dashboard_patch: DashboardPatch,
                           workset_manager: WorksetManager,
                           user: UserInfo | None = Depends(get_current_user)) -> DashboardSummary:
#    print("update dashboard")
#    print(dashboard_id)
#    print(dashboard_patch)
    await workset_manager.get_public_worksets()
    if dashboard_patch.imported_id and not workset_manager.is_valid_workset(dashboard_patch.imported_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown workset id {dashboard_patch.imported_id}"
        )

    user_id = UUID(user.get("htrc-guid", user.sub)) if user else None
    # dashboard_patch_update = DashboardPatchUpdate.model_construct(**dashboard_patch.model_dump(exclude_defaults=True))
    dashboard_patch_update = DashboardPatchUpdate(**dashboard_patch.model_dump(exclude_defaults=True))
    dashboard = await DashboardSummary.from_mongo(
        mongo_client.db["dashboards"].find_one_and_update(
            filter={"_id": dashboard_id, "owner": user_id},
            update={"$set": dashboard_patch_update.to_mongo(exclude_unset=False)},
            return_document=ReturnDocument.AFTER
        )
    )
    if dashboard:
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
async def get_widget_data(dashboard_id: UUID, widget_type: str,
                          user: UserInfo | None = Depends(get_current_user)):
    dashboard = await get_dashboard(dashboard_id, user)
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

        case _:
            raise TorchliteError(f"Unsupported widget data type {widget.data_type}")

    filtered_volumes = apply_filters(volumes, filters=dashboard.filters)
    return await widget.get_data(filtered_volumes)
