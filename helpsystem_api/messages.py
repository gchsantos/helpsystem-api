from rest_framework.response import Response
from rest_framework import status


class ReturnBaseMessage():

    def __init__(self, success=True, detail='', code=status.HTTP_200_OK) -> None:
        self.success = success
        self.detail = detail
        self.code = code
        self.message = self.make_message()

    def make_message(self) -> dict:
        if not self.success:
            if not self.detail:
                self.detail = 'Falha Geral'
            if not self.code:
                self.code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(
            {'success': self.success, 'detail': self.detail},
            self.code)
