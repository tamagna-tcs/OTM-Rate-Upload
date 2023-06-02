from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    def get_success_url(self):
        self.request.session["logged_in_from_url"] = self.request.get_full_path()
        return super().get_success_url()