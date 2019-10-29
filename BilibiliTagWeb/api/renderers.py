from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'status': 0,
            'data': data,
            'errors': [],
            'message': 'success',
        }

        getattr(renderer_context.get('view').get_serializer().Meta,
                'resource_name', 'objects')

        # call super to render the response
        response = super(CustomJSONRenderer, self).render(
            response_data, accepted_media_type, renderer_context)

        return response
