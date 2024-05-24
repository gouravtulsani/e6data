# This is to hide the models are the bottom of the Swagger doc
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "e6-blogs Swagger documentation",
        "description": "API <style>.models {display: none !important}</style>",
        "version": "1.0.0"
    },
    "schemes": ["http"],
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
}
