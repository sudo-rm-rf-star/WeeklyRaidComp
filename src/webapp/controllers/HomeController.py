from .AbstractController import AbstractController


class HomeController(AbstractController):
    def __init__(self, *args, **kwargs):
        super(HomeController, self).__init__(*args, **kwargs)

    def home(self):
        if self.is_auth():
            return self.view('home')
        else:
            return self.view('guest')

