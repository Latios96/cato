import logging
from http.client import BAD_REQUEST

from fastapi import APIRouter, UploadFile, File
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_server.api.validators.project_validators import CreateProjectValidator
from cato_common.domain.project import Project, ProjectStatus
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.usecases.create_project_image import CreateProjectImage

logger = logging.getLogger(__name__)


class ProjectsBlueprint(APIRouter):
    def __init__(
        self,
        project_repository: ProjectRepository,
        object_mapper: ObjectMapper,
        create_project_image: CreateProjectImage,
    ):
        super(ProjectsBlueprint, self).__init__()
        self._project_repository = project_repository
        self._object_mapper = object_mapper
        self._create_project_image = create_project_image

        self.get("/projects")(self.get_projects)
        self.get("/projects/{project_id}")(self.get_project)
        self.get("/projects/name/{project_name}")(self.get_project_by_name)
        self.post("/projects")(self.create_project)
        self.post("/projects/{project_id}/status/active")(self.activate_project)
        self.post("/projects/{project_id}/status/archived")(self.archive_project)
        self.post("/projects/{project_id}/uploadImage")(self.upload_image)

    def get_projects(self) -> Response:
        projects = self._project_repository.find_all()
        return JSONResponse(content=self._object_mapper.many_to_dict(projects))

    def get_project(self, project_id: int) -> Response:
        project = self._project_repository.find_by_id(project_id)
        if not project:
            return Response(status_code=404)
        return JSONResponse(content=self._object_mapper.to_dict(project))

    async def create_project(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateProjectValidator(self._project_repository).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        project_name = request_json["name"]

        project = Project(id=0, name=project_name, status=ProjectStatus.ACTIVE)
        project = self._project_repository.save(project)
        logger.info("Created project %s", project)
        return JSONResponse(
            content=self._object_mapper.to_dict(project), status_code=201
        )

    def get_project_by_name(self, project_name: str) -> Response:
        project = self._project_repository.find_by_name(project_name)
        if not project:
            return Response(status_code=404)
        return JSONResponse(content=self._object_mapper.to_dict(project))

    def activate_project(self, project_id: int) -> Response:
        project = self._project_repository.find_by_id(project_id)

        if not project:
            return Response(status_code=404)

        project.status = ProjectStatus.ACTIVE
        self._project_repository.save(project)

        return JSONResponse(content=self._object_mapper.to_dict(project))

    def archive_project(self, project_id: int) -> Response:
        project = self._project_repository.find_by_id(project_id)

        if not project:
            return Response(status_code=404)

        project.status = ProjectStatus.ARCHIVED
        self._project_repository.save(project)

        return JSONResponse(content=self._object_mapper.to_dict(project))

    def upload_image(self, project_id: int, file: UploadFile = File(...)) -> Response:
        project = self._project_repository.find_by_id(project_id)

        if not project:
            return Response(status_code=404)

        project = self._create_project_image.create_project_image(
            project, file.file, file.filename
        )

        return JSONResponse(
            content=self._object_mapper.to_dict(project), status_code=201
        )
