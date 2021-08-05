import logging
from http.client import BAD_REQUEST

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_server.api.validators.project_validators import CreateProjectValidator
from cato_common.domain.project import Project
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.project_repository import ProjectRepository

logger = logging.getLogger(__name__)


class ProjectsBlueprint(APIRouter):
    def __init__(
        self, project_repository: ProjectRepository, object_mapper: ObjectMapper
    ):
        super(ProjectsBlueprint, self).__init__()
        self._project_repository = project_repository
        self._object_mapper = object_mapper

        self.get("/projects")(self.get_projects)
        self.get("/projects/{project_id}")(self.get_project)
        self.get("/projects/name/{project_name}")(self.get_project_by_name)
        self.post("/projects")(self.create_project)

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

        project = Project(id=0, name=project_name)
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
