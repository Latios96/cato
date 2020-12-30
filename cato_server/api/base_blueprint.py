from flask import Blueprint, current_app


class BaseBlueprint(Blueprint):
    def json_response(self, json_str: str):
        return current_app.response_class(
            json_str + "\n",
            mimetype=current_app.config["JSONIFY_MIMETYPE"],
        )
