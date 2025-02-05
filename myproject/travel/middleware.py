from django.shortcuts import redirect

class ClickCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        click_count = int(c('click_count', 0))

        # Avoid infinite redirect loops
        if click_count >= 2 and request.path != "/login/":
            return redirect("login")  

        click_count += 1

        response = self.get_response(request)

        # Set the cookie with an expiration time
        response.set_cookie("click_count", click_count, max_age=3600)  # 1 hour expiry

        return response
